"""
Smart SEO Assistant Backend API
FastAPI backend server integrating the SEO pipeline for web application
"""

import sys
import os
from pathlib import Path

# Add the ml_pipeline to Python path
ml_pipeline_path = Path(__file__).parent.parent / "ml_pipeline" / "src"
sys.path.append(str(ml_pipeline_path))

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging
import asyncio
import json
from datetime import datetime
import uuid

# Import our SEO pipeline
from smart_seo_assistant_ace import (
    SEOAssistantPipeline, 
    ConfigurationManager,
    SEOContext,
    ContentBrief,
    FullArticle,
    ContentCalendar
)

# Database and storage
from database import DatabaseManager
from models import (
    ProjectCreate, ProjectResponse, ProjectUpdate,
    KeywordAnalysisRequest, KeywordAnalysisResponse,
    ContentBriefRequest, ContentBriefResponse,
    BulkProcessRequest, BulkProcessResponse,
    ContentCalendarRequest, ContentCalendarResponse,
    UserCreate, UserResponse, TokenResponse
)
from auth import AuthManager
from storage import StorageManager

# Initialize FastAPI app
app = FastAPI(
    title="Smart SEO Assistant API",
    description="AI-powered SEO content planning and generation backend",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React/Vite dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Global instances
pipeline: Optional[SEOAssistantPipeline] = None
db_manager: Optional[DatabaseManager] = None
auth_manager: Optional[AuthManager] = None
storage_manager: Optional[StorageManager] = None

# Background tasks storage
background_tasks_store = {}


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global pipeline, db_manager, auth_manager, storage_manager
    
    try:
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger(__name__)
        
        # Initialize database
        db_manager = DatabaseManager()
        await db_manager.initialize()
        
        # Initialize authentication
        auth_manager = AuthManager(db_manager)
        
        # Initialize storage
        storage_manager = StorageManager()
        
        # Initialize SEO pipeline
        config_manager = ConfigurationManager()
        config = config_manager.get_pipeline_config()
        
        if not config.gemini_api_key:
            logger.error("❌ GEMINI_API_KEY not found! Set it as environment variable.")
            raise ValueError("GEMINI_API_KEY is required")
        
        pipeline = SEOAssistantPipeline(config)
        logger.info("✅ SEO Assistant Backend initialized successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize backend: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global pipeline, db_manager
    
    if db_manager:
        await db_manager.close()
    
    pipeline = None


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if pipeline else "unhealthy",
        "message": "SEO Assistant Backend is running" if pipeline else "Pipeline not initialized",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0"
    }


# SEO Analysis endpoints
@app.post("/seo/analyze")
async def analyze_keyword(request: dict):
    """Analyze a keyword and return SEO insights"""
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    try:
        keyword = request.get("keyword", "")
        goal = request.get("goal", "")
        
        if not keyword:
            raise HTTPException(status_code=400, detail="Keyword is required")
        
        # Get SEO context using our pipeline
        context = pipeline.retrieve_context(keyword, goal)
        
        # Prepare response data
        analysis_data = {
            "keyword": context.keyword,
            "search_intent": context.search_intent,
            "related_keywords": context.related_keywords[:20],
            "content_opportunities": context.content_opportunities[:15],
            "user_questions": context.user_questions[:15],
            "wikipedia_sources": [
                {
                    "title": data.title,
                    "url": data.url,
                    "relevance_score": data.relevance_score
                } for data in context.wikipedia_data[:10]
            ]
        }
        
        return analysis_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/seo/brief")
async def generate_content_brief(request: dict):
    """Generate SEO-optimized content brief"""
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    try:
        keyword = request.get("keyword", "")
        goal = request.get("goal", "")
        
        if not keyword:
            raise HTTPException(status_code=400, detail="Keyword is required")
        
        # Generate content brief using our pipeline
        brief = pipeline.generate_content_brief(keyword, goal)
        
        # Convert to response format
        brief_data = {
            "title": brief.title,
            "meta_description": brief.meta_description,
            "content_type": brief.content_type.value if hasattr(brief.content_type, 'value') else str(brief.content_type),
            "word_count_target": brief.word_count_target,
            "outline": brief.outline,
            "call_to_action": brief.call_to_action,
            "created_at": datetime.utcnow().isoformat()
        }
        
        return brief_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Brief generation failed: {str(e)}")


@app.post("/seo/article")
async def generate_full_article(request: dict, background_tasks: BackgroundTasks):
    """Generate full SEO article (background task)"""
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    keyword = request.get("keyword", "")
    goal = request.get("goal", "")
    
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword is required")
    
    # Create background task
    task_id = str(uuid.uuid4())
    
    background_tasks.add_task(
        generate_article_task,
        task_id,
        keyword,
        goal
    )
    
    return {
        "task_id": task_id,
        "message": f"Article generation started for '{keyword}'",
        "status": "processing"
    }


@app.post("/seo/bulk")
async def bulk_process_keywords(request: dict):
    """Process multiple keywords in bulk"""
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    keywords = request.get("keywords", [])
    goal = request.get("goal", "")
    
    if not keywords:
        raise HTTPException(status_code=400, detail="Keywords list is required")
    
    if len(keywords) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 keywords allowed")
    
    try:
        # Process keywords using our pipeline
        results = pipeline.bulk_process_keywords(keywords, goal)
        
        # Calculate summary
        successful = sum(1 for r in results if r["status"] == "success")
        failed = len(results) - successful
        
        summary = {
            "total_keywords": len(keywords),
            "successful": successful,
            "failed": failed,
            "success_rate": successful / len(results) * 100 if results else 0
        }
        
        return {
            "summary": summary,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk processing failed: {str(e)}")


@app.post("/seo/calendar")
async def create_content_calendar(request: dict):
    """Create content calendar for keywords"""
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    keywords = request.get("keywords", [])
    goal = request.get("goal", "")
    timeframe_weeks = request.get("timeframe_weeks", 4)
    
    if not keywords:
        raise HTTPException(status_code=400, detail="Keywords list is required")
    
    if len(keywords) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 keywords allowed for calendar")
    
    try:
        # Generate calendar using our pipeline
        calendar = pipeline.plan_content_calendar(keywords, timeframe_weeks)
        
        # Convert to response format
        calendar_data = {
            "timeframe_weeks": calendar.timeframe_weeks,
            "total_keywords": calendar.total_keywords,
            "items": [
                {
                    "keyword": item.keyword,
                    "title": item.title,
                    "content_type": item.content_type.value if hasattr(item.content_type, 'value') else str(item.content_type),
                    "priority_score": item.priority_score,
                    "target_week": item.target_week,
                    "estimated_difficulty": item.estimated_difficulty
                } for item in calendar.items
            ],
            "created_at": datetime.utcnow().isoformat()
        }
        
        return calendar_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calendar creation failed: {str(e)}")


# Task status endpoints
@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get background task status"""
    if task_id in background_tasks_store:
        return background_tasks_store[task_id]
    else:
        raise HTTPException(status_code=404, detail="Task not found")


# Statistics and analytics
@app.get("/stats")
async def get_pipeline_stats():
    """Get pipeline statistics"""
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    try:
        stats = pipeline.get_pipeline_stats()
        performance_report = pipeline.get_performance_report()
        
        return {
            "pipeline_stats": stats,
            "performance_report": performance_report,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


# Background task functions
async def generate_article_task(task_id: str, keyword: str, goal: str):
    """Background task for generating full articles"""
    global background_tasks_store
    
    try:
        # Update task status
        background_tasks_store[task_id] = {
            "status": "processing",
            "progress": 0,
            "message": f"Starting article generation for '{keyword}'"
        }
        
        # Generate article using pipeline
        article = pipeline.generate_full_article(keyword, goal)
        
        # Convert to storage format
        article_data = {
            "title": article.title,
            "meta_description": article.meta_description,
            "total_word_count": article.total_word_count,
            "sections": [
                {
                    "heading": section.heading,
                    "content": section.content,
                    "word_count": section.word_count
                } for section in article.sections
            ],
            "keyword": keyword,
            "goal": goal,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Update task status
        background_tasks_store[task_id] = {
            "status": "completed",
            "progress": 100,
            "message": f"Article generated successfully for '{keyword}'",
            "result": article_data
        }
        
    except Exception as e:
        background_tasks_store[task_id] = {
            "status": "failed",
            "progress": 0,
            "message": f"Article generation failed: {str(e)}",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

