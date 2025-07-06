"""
FastAPI Web Interface for SEO Assistant Pipeline
Provides REST API endpoints for SEO content generation

Usage:
    uvicorn smart_seo_assistant_ace.api:app --reload
    
Endpoints:
    GET /health - Health check
    POST /analyze - Analyze keyword
    POST /brief - Generate content brief
    POST /article - Generate full article
    POST /bulk - Process multiple keywords
    POST /calendar - Create content calendar
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import asyncio
from pathlib import Path
import json

from .config.configuration import ConfigurationManager
from .pipeline.seo_pipeline import SEOAssistantPipeline
from .entity import PipelineConfig

# Initialize FastAPI app
app = FastAPI(
    title="Smart SEO Assistant API",
    description="AI-powered SEO content planning and generation API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global pipeline instance
pipeline: Optional[SEOAssistantPipeline] = None


# Pydantic models for API requests/responses
class KeywordAnalysisRequest(BaseModel):
    keyword: str
    goal: Optional[str] = ""


class ContentBriefRequest(BaseModel):
    keyword: str
    goal: Optional[str] = ""


class FullArticleRequest(BaseModel):
    keyword: str
    goal: Optional[str] = ""


class BulkProcessRequest(BaseModel):
    keywords: List[str]
    goal: Optional[str] = ""


class ContentCalendarRequest(BaseModel):
    keywords: List[str]
    goal: Optional[str] = ""
    timeframe_weeks: Optional[int] = 4


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize pipeline on startup"""
    global pipeline
    
    try:
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        # Initialize configuration
        config_manager = ConfigurationManager()
        config = config_manager.get_pipeline_config()
        
        if not config.gemini_api_key:
            logger.error("❌ GEMINI_API_KEY not found! Set it as environment variable.")
            raise ValueError("GEMINI_API_KEY is required")
        
        # Initialize pipeline
        pipeline = SEOAssistantPipeline(config)
        logger.info("✅ SEO Assistant Pipeline initialized successfully!")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize pipeline: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global pipeline
    pipeline = None


# API endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global pipeline
    
    return {
        "status": "healthy" if pipeline else "unhealthy",
        "message": "SEO Assistant API is running" if pipeline else "Pipeline not initialized",
        "pipeline_stats": pipeline.get_pipeline_stats() if pipeline else None
    }


@app.post("/analyze", response_model=ApiResponse)
async def analyze_keyword(request: KeywordAnalysisRequest):
    """Analyze a keyword and return insights"""
    global pipeline
    
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    try:
        # Get context
        context = pipeline.retrieve_context(request.keyword, request.goal)
        
        # Prepare response data
        analysis_data = {
            "keyword": context.keyword,
            "search_intent": context.search_intent,
            "related_keywords": context.related_keywords[:15],
            "content_opportunities": context.content_opportunities[:10],
            "user_questions": context.user_questions[:10],
            "wikipedia_sources": [
                {
                    "title": data.title,
                    "url": data.url,
                    "relevance_score": data.relevance_score
                } for data in context.wikipedia_data[:5]
            ]
        }
        
        return ApiResponse(
            success=True,
            message=f"Keyword analysis completed for '{request.keyword}'",
            data=analysis_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/brief", response_model=ApiResponse)
async def generate_content_brief(request: ContentBriefRequest):
    """Generate content brief for a keyword"""
    global pipeline
    
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    try:
        # Generate brief
        brief = pipeline.generate_content_brief(request.keyword, request.goal)
        
        return ApiResponse(
            success=True,
            message=f"Content brief generated for '{request.keyword}'",
            data=brief.to_dict()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Brief generation failed: {str(e)}")


@app.post("/article", response_model=ApiResponse)
async def generate_full_article(request: FullArticleRequest):
    """Generate full article for a keyword"""
    global pipeline
    
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    try:
        # Generate article
        article = pipeline.generate_full_article(request.keyword, request.goal)
        
        return ApiResponse(
            success=True,
            message=f"Full article generated for '{request.keyword}'",
            data=article.to_dict()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Article generation failed: {str(e)}")


@app.post("/bulk", response_model=ApiResponse)
async def bulk_process_keywords(request: BulkProcessRequest):
    """Process multiple keywords in bulk"""
    global pipeline
    
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    if len(request.keywords) > 50:  # Limit bulk processing
        raise HTTPException(status_code=400, detail="Maximum 50 keywords allowed")
    
    try:
        # Process keywords
        results = pipeline.bulk_process_keywords(request.keywords, request.goal)
        
        # Calculate summary
        successful = sum(1 for r in results if r["status"] == "success")
        failed = len(results) - successful
        
        summary = {
            "total_keywords": len(request.keywords),
            "successful": successful,
            "failed": failed,
            "success_rate": successful / len(results) * 100 if results else 0
        }
        
        return ApiResponse(
            success=True,
            message=f"Bulk processing completed: {successful}/{len(request.keywords)} successful",
            data={
                "summary": summary,
                "results": results
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk processing failed: {str(e)}")


@app.post("/calendar", response_model=ApiResponse)
async def create_content_calendar(request: ContentCalendarRequest):
    """Create content calendar for keywords"""
    global pipeline
    
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    if len(request.keywords) > 100:  # Limit calendar size
        raise HTTPException(status_code=400, detail="Maximum 100 keywords allowed for calendar")
    
    try:
        # Generate calendar
        calendar = pipeline.plan_content_calendar(
            request.keywords, 
            request.timeframe_weeks
        )
        
        return ApiResponse(
            success=True,
            message=f"Content calendar created for {len(request.keywords)} keywords over {request.timeframe_weeks} weeks",
            data=calendar.to_dict()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calendar creation failed: {str(e)}")


@app.get("/stats")
async def get_pipeline_stats():
    """Get pipeline performance statistics"""
    global pipeline
    
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    try:
        stats = pipeline.get_pipeline_stats()
        performance_report = pipeline.get_performance_report()
        
        return {
            "pipeline_stats": stats,
            "performance_report": performance_report
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


# Background task endpoints
@app.post("/bulk-async")
async def bulk_process_async(request: BulkProcessRequest, background_tasks: BackgroundTasks):
    """Process keywords in background (for large batches)"""
    global pipeline
    
    if not pipeline:
        raise HTTPException(status_code=500, detail="Pipeline not initialized")
    
    if len(request.keywords) > 200:
        raise HTTPException(status_code=400, detail="Maximum 200 keywords allowed for async processing")
    
    # Generate task ID
    task_id = f"bulk_{len(request.keywords)}_{int(asyncio.get_event_loop().time())}"
    
    # Add background task
    background_tasks.add_task(
        process_keywords_background,
        task_id,
        request.keywords,
        request.goal
    )
    
    return {
        "task_id": task_id,
        "message": f"Background processing started for {len(request.keywords)} keywords",
        "status": "processing"
    }


async def process_keywords_background(task_id: str, keywords: List[str], goal: str):
    """Background task for processing keywords"""
    global pipeline
    
    try:
        results = pipeline.bulk_process_keywords(keywords, goal)
        
        # Save results to file
        output_file = f"bulk_results_{task_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "task_id": task_id,
                "keywords": keywords,
                "goal": goal,
                "results": results,
                "completed_at": str(asyncio.get_event_loop().time())
            }, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Background task {task_id} completed successfully")
        
    except Exception as e:
        logging.error(f"Background task {task_id} failed: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
