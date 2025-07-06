"""
Smart SEO Assistant ACE Pipeline
Advanced Contextual Extraction for SEO Content Generation

This package provides a comprehensive AI-powered SEO content generation pipeline
that implements the ACE methodology:
- A: Advanced Retrieval - Gather comprehensive context from multiple sources
- C: Context Design - Optimize and structure context for AI processing  
- E: Execution - Generate high-quality SEO content using AI

Quick Start:
    from smart_seo_assistant_ace import SEOAssistantPipeline, ConfigurationManager
    
    # Initialize configuration
    config_manager = ConfigurationManager()
    config = config_manager.get_pipeline_config()
    
    # Create pipeline
    pipeline = SEOAssistantPipeline(config)
    
    # Generate content brief
    brief = pipeline.generate_content_brief("machine learning tutorial")
    
    # Generate full article
    article = pipeline.generate_full_article("python programming guide")

Features:
    - Keyword analysis and related keyword extraction
    - Content brief generation with SEO optimization
    - Full article generation with structured content
    - Bulk processing for multiple keywords
    - Content calendar planning and prioritization
    - Performance tracking and analytics
    - CLI and web API interfaces
    - Jupyter notebook integration
"""

__version__ = "1.0.0"
__author__ = "Smart SEO Assistant Team"
__email__ = "contact@smartseoassistant.com"

# Core imports for easy access
from .pipeline.seo_pipeline import SEOAssistantPipeline
from .config.configuration import ConfigurationManager
from .entity import (
    SEOContext, ContentBrief, FullArticle, ContentCalendar, 
    ContentCalendarItem, PerformanceMetrics, PipelineConfig,
    ContentType, SearchIntent
)
from .components.data_retrieval import DataRetriever
from .components.content_generation import ContentGenerator

# Utility imports
from .utils import setup_logging, clean_text

__all__ = [
    # Core classes
    "SEOAssistantPipeline",
    "ConfigurationManager",
    "DataRetriever", 
    "ContentGenerator",
    
    # Data structures
    "SEOContext",
    "ContentBrief", 
    "FullArticle",
    "ContentCalendar",
    "ContentCalendarItem",
    "PerformanceMetrics",
    "PipelineConfig",
    "ContentType",
    "SearchIntent",
    
    # Utilities
    "setup_logging",
    "clean_text",
    
    # Metadata
    "__version__",
    "__author__",
    "__email__"
]
