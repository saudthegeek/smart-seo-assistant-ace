"""
Main SEO Assistant Pipeline
Orchestrates the complete workflow from keyword input to content generation
"""

import time
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..entity import (
    SEOContext, ContentBrief, FullArticle, ContentCalendar, 
    ContentCalendarItem, PerformanceMetrics, PipelineConfig, ContentType
)
from ..components.data_retrieval import DataRetriever
from ..components.content_generation import ContentGenerator
from ..utils import generate_cache_key, merge_dictionaries
from ..constants import CONTEXT_CACHE_TTL


class SEOAssistantPipeline:
    """
    Main SEO Assistant Pipeline that orchestrates the complete workflow
    Demonstrates ACE principles: Advanced Retrieval → Context Design → Execution
    """
    
    def __init__(self, config: PipelineConfig):
        """
        Initialize SEO Assistant Pipeline
        
        Args:
            config: Pipeline configuration
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.data_retriever = DataRetriever(
            timeout=config.timeout,
            max_retries=config.max_retries
        )
        
        self.content_generator = ContentGenerator(
            api_key=config.gemini_api_key,
            model_name=config.gemini_model
        )
        
        # Initialize cache if enabled
        self.context_cache = {} if config.cache_enabled else None
        self.performance_data = {}
        
        self.logger.info("SEO Assistant Pipeline initialized successfully")
    
    def _get_cached_context(self, keyword: str, user_goal: str = "") -> Optional[SEOContext]:
        """Get context from cache if available and not expired"""
        if not self.context_cache:
            return None
        
        cache_key = generate_cache_key(keyword, user_goal)
        cached_item = self.context_cache.get(cache_key)
        
        if cached_item:
            context, timestamp = cached_item
            if time.time() - timestamp < self.config.cache_ttl:
                self.logger.info(f"Using cached context for: {keyword}")
                return context
            else:
                # Remove expired cache
                del self.context_cache[cache_key]
        
        return None
    
    def _cache_context(self, context: SEOContext, user_goal: str = ""):
        """Cache context data"""
        if not self.context_cache:
            return
        
        cache_key = generate_cache_key(context.keyword, user_goal)
        self.context_cache[cache_key] = (context, time.time())
        
        # Cleanup old cache entries if too many
        if len(self.context_cache) > 100:  # Max cache size
            oldest_key = min(self.context_cache.keys(), 
                           key=lambda k: self.context_cache[k][1])
            del self.context_cache[oldest_key]
    
    # ===== A: ADVANCED RETRIEVAL =====
    
    def retrieve_context(self, keyword: str, user_goal: str = "") -> SEOContext:
        """
        Advanced retrieval phase - gather comprehensive context
        
        Args:
            keyword: Target keyword
            user_goal: User's specific goal or context
            
        Returns:
            SEOContext with comprehensive data
        """
        self.logger.info(f"🔍 PHASE A: Advanced Retrieval for '{keyword}'")
        
        # Check cache first
        cached_context = self._get_cached_context(keyword, user_goal)
        if cached_context:
            return cached_context
        
        start_time = time.time()
        
        # Use data retriever to get comprehensive context
        context = self.data_retriever.get_comprehensive_context(keyword, user_goal)
        
        # Cache the context
        self._cache_context(context, user_goal)
        
        retrieval_time = time.time() - start_time
        self.logger.info(f"✅ Advanced retrieval completed in {retrieval_time:.2f}s")
        
        return context
    
    # ===== C: CONTEXT DESIGN =====
    
    def design_context(self, context: SEOContext) -> Dict[str, Any]:
        """
        Context design phase - optimize context for AI processing
        
        Args:
            context: Raw SEO context
            
        Returns:
            Optimized context data
        """
        self.logger.info(f"🧠 PHASE C: Context Design for '{context.keyword}'")
        
        start_time = time.time()
        
        # Calculate context metrics
        context_metrics = {
            "keyword": context.keyword,
            "search_intent": context.search_intent,
            "data_sources": len(context.wikipedia_data),
            "related_keywords_count": len(context.related_keywords),
            "content_opportunities_count": len(context.content_opportunities),
            "user_questions_count": len(context.user_questions),
            "context_quality_score": self._calculate_context_quality(context)
        }
        
        # Optimize context data
        optimized_context = {
            "primary_data": context.to_dict(),
            "metrics": context_metrics,
            "processing_hints": {
                "focus_areas": context.content_opportunities[:3],
                "key_questions": context.user_questions[:3],
                "semantic_cluster": context.related_keywords[:5]
            }
        }
        
        design_time = time.time() - start_time
        self.logger.info(f"✅ Context design completed in {design_time:.2f}s")
        
        return optimized_context
    
    def _calculate_context_quality(self, context: SEOContext) -> float:
        """Calculate quality score for context data"""
        score = 0.0
        
        # Wikipedia data quality
        if context.wikipedia_data:
            avg_relevance = sum(r.relevance_score for r in context.wikipedia_data) / len(context.wikipedia_data)
            score += avg_relevance * 0.3
        
        # Related keywords richness
        score += min(len(context.related_keywords) / 10, 1.0) * 0.2
        
        # Content opportunities
        score += min(len(context.content_opportunities) / 8, 1.0) * 0.2
        
        # User questions coverage
        score += min(len(context.user_questions) / 8, 1.0) * 0.2
        
        # Search intent clarity
        if context.search_intent:
            score += 0.1
        
        return score
    
    # ===== E: EXECUTION =====
    
    def execute_content_generation(self, context: SEOContext) -> ContentBrief:
        """
        Execution phase - generate content using AI
        
        Args:
            context: SEO context
            
        Returns:
            Generated content brief
        """
        self.logger.info(f"⚡ PHASE E: Content Generation for '{context.keyword}'")
        
        start_time = time.time()
        
        # Generate content brief using content generator
        content_brief = self.content_generator.generate_content_brief(context)
        
        execution_time = time.time() - start_time
        self.logger.info(f"✅ Content generation completed in {execution_time:.2f}s")
        
        return content_brief
    
    # ===== MAIN PIPELINE METHODS =====
    
    def generate_content_brief(self, keyword: str, user_goal: str = "") -> ContentBrief:
        """
        Main pipeline method: Generate SEO content brief
        
        Args:
            keyword: Target keyword
            user_goal: User's specific goal
            
        Returns:
            Complete content brief
        """
        self.logger.info(f"🚀 Starting SEO content brief generation for: '{keyword}'")
        
        pipeline_start = time.time()
        
        try:
            # A: Advanced Retrieval
            context = self.retrieve_context(keyword, user_goal)
            
            # C: Context Design
            optimized_context = self.design_context(context)
            
            # E: Execution
            content_brief = self.execute_content_generation(context)
            
            pipeline_time = time.time() - pipeline_start
            
            self.logger.info(f"🎉 Pipeline completed successfully in {pipeline_time:.2f}s")
            self.logger.info(f"Generated: {content_brief.title}")
            
            return content_brief
            
        except Exception as e:
            self.logger.error(f"Pipeline failed for '{keyword}': {e}")
            raise
    
    def generate_full_article(self, keyword: str, user_goal: str = "") -> FullArticle:
        """
        Generate complete SEO article
        
        Args:
            keyword: Target keyword
            user_goal: User's specific goal
            
        Returns:
            Complete article
        """
        self.logger.info(f"📝 Generating full article for: '{keyword}'")
        
        # Get context
        context = self.retrieve_context(keyword, user_goal)
        
        # Generate full article
        article = self.content_generator.generate_full_article(context)
        
        self.logger.info(f"✅ Full article generated: {article.total_word_count} words")
        
        return article
    
    def bulk_process_keywords(self, keywords: List[str], user_goal: str = "") -> List[Dict[str, Any]]:
        """
        Process multiple keywords in bulk
        
        Args:
            keywords: List of keywords to process
            user_goal: Common user goal for all keywords
            
        Returns:
            List of results for each keyword
        """
        self.logger.info(f"📦 Bulk processing {len(keywords)} keywords")
        
        results = []
        start_time = time.time()
        
        for i, keyword in enumerate(keywords, 1):
            self.logger.info(f"Processing {i}/{len(keywords)}: '{keyword}'")
            
            try:
                content_brief = self.generate_content_brief(keyword, user_goal)
                
                results.append({
                    "keyword": keyword,
                    "status": "success",
                    "title": content_brief.title,
                    "word_count_target": content_brief.word_count_target,
                    "content_brief": content_brief.to_dict()
                })
                
            except Exception as e:
                self.logger.error(f"Failed to process '{keyword}': {e}")
                results.append({
                    "keyword": keyword,
                    "status": "failed",
                    "error": str(e)
                })
        
        total_time = time.time() - start_time
        successful = sum(1 for r in results if r["status"] == "success")
        
        self.logger.info(f"📊 Bulk processing completed: {successful}/{len(keywords)} successful in {total_time:.2f}s")
        
        return results
    
    def plan_content_calendar(self, keywords: List[str], timeframe_weeks: int = 4) -> ContentCalendar:
        """
        Plan content calendar for multiple keywords
        
        Args:
            keywords: List of keywords
            timeframe_weeks: Planning timeframe in weeks
            
        Returns:
            Content calendar
        """
        self.logger.info(f"📅 Planning content calendar for {len(keywords)} keywords over {timeframe_weeks} weeks")
        
        calendar = ContentCalendar(
            timeframe_weeks=timeframe_weeks,
            total_keywords=len(keywords)
        )
        
        # Analyze keywords and assign priorities
        keyword_items = []
        
        for keyword in keywords:
            try:
                # Get basic context for priority calculation
                context = self.retrieve_context(keyword)
                
                # Calculate priority score
                priority_score = self._calculate_keyword_priority(context)
                
                # Determine content type
                content_type = self._suggest_content_type(context)
                
                # Create calendar item
                item = ContentCalendarItem(
                    keyword=keyword,
                    title=f"Guide to {keyword.title()}",
                    content_type=content_type,
                    priority_score=priority_score,
                    estimated_difficulty="Medium",
                    target_week=1  # Will be reassigned based on priority
                )
                
                keyword_items.append(item)
                
            except Exception as e:
                self.logger.error(f"Failed to analyze keyword '{keyword}': {e}")
        
        # Sort by priority and assign to weeks
        keyword_items.sort(key=lambda x: x.priority_score, reverse=True)
        
        keywords_per_week = max(1, len(keyword_items) // timeframe_weeks)
        
        for i, item in enumerate(keyword_items):
            week = (i // keywords_per_week) + 1
            if week > timeframe_weeks:
                week = timeframe_weeks
            
            item.target_week = week
            calendar.add_item(item)
        
        self.logger.info(f"✅ Content calendar planned with {len(keyword_items)} items")
        
        return calendar
    
    def _calculate_keyword_priority(self, context: SEOContext) -> float:
        """Calculate priority score for keyword"""
        score = 0.0
        
        # Search intent scoring
        if "transactional" in context.search_intent.lower():
            score += 3.0
        elif "commercial" in context.search_intent.lower():
            score += 2.5
        elif "informational" in context.search_intent.lower():
            score += 2.0
        
        # Content richness
        score += len(context.content_opportunities) * 0.1
        score += len(context.related_keywords) * 0.05
        score += len(context.wikipedia_data) * 0.2
        
        return score
    
    def _suggest_content_type(self, context: SEOContext) -> ContentType:
        """Suggest content type based on context"""
        keyword_lower = context.keyword.lower()
        
        if "how to" in keyword_lower:
            return ContentType.HOW_TO
        elif "vs" in keyword_lower or "compare" in keyword_lower:
            return ContentType.COMPARISON
        elif "best" in keyword_lower or "top" in keyword_lower:
            return ContentType.LISTICLE
        elif "guide" in keyword_lower:
            return ContentType.GUIDE
        elif "tutorial" in keyword_lower:
            return ContentType.TUTORIAL
        else:
            return ContentType.BLOG_POST
    
    def track_performance(self, keyword: str, metrics: Dict[str, Any]) -> PerformanceMetrics:
        """
        Track performance metrics for a keyword
        
        Args:
            keyword: Keyword to track
            metrics: Performance metrics data
            
        Returns:
            PerformanceMetrics object
        """
        performance = PerformanceMetrics(
            keyword=keyword,
            impressions=metrics.get("impressions", 0),
            clicks=metrics.get("clicks", 0),
            position=metrics.get("position", 0.0),
            ctr=metrics.get("ctr", 0.0)
        )
        
        self.performance_data[keyword] = performance
        
        self.logger.info(f"📊 Performance tracked for '{keyword}': {metrics}")
        
        return performance
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report"""
        if not self.performance_data:
            return {"message": "No performance data available"}
        
        total_keywords = len(self.performance_data)
        total_clicks = sum(p.clicks for p in self.performance_data.values())
        total_impressions = sum(p.impressions for p in self.performance_data.values())
        avg_position = sum(p.position for p in self.performance_data.values()) / total_keywords
        
        # Top performers
        top_performers = sorted(
            self.performance_data.items(),
            key=lambda x: x[1].clicks,
            reverse=True
        )[:5]
        
        return {
            "summary": {
                "total_keywords_tracked": total_keywords,
                "total_clicks": total_clicks,
                "total_impressions": total_impressions,
                "average_position": round(avg_position, 1),
                "overall_ctr": round(total_clicks / total_impressions * 100, 2) if total_impressions > 0 else 0
            },
            "top_performers": [
                {
                    "keyword": kw,
                    "clicks": perf.clicks,
                    "position": perf.position,
                    "ctr": perf.ctr
                } for kw, perf in top_performers
            ]
        }
    
    def get_pipeline_stats(self) -> Dict[str, Any]:
        """Get pipeline performance statistics"""
        return {
            "cache_size": len(self.context_cache) if self.context_cache else 0,
            "performance_tracked_keywords": len(self.performance_data),
            "config": self.config.to_dict()
        }
