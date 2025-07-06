"""
Entity classes for SEO Assistant Pipeline
Data structures for handling SEO content generation workflow
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class SearchIntent(Enum):
    """Search intent classifications"""
    INFORMATIONAL = "informational"
    NAVIGATIONAL = "navigational"
    TRANSACTIONAL = "transactional"
    COMMERCIAL = "commercial"


class ContentType(Enum):
    """Content type classifications"""
    BLOG_POST = "blog_post"
    GUIDE = "guide"
    TUTORIAL = "tutorial"
    COMPARISON = "comparison"
    LISTICLE = "listicle"
    HOW_TO = "how_to"
    REVIEW = "review"


@dataclass
class WikipediaResult:
    """Single Wikipedia search result"""
    title: str
    snippet: str
    url: str
    relevance_score: float = 0.0


@dataclass
class SEOContext:
    """Comprehensive context container for SEO data"""
    keyword: str
    user_goal: str = ""
    search_intent: str = ""
    related_keywords: List[str] = field(default_factory=list)
    wikipedia_data: List[WikipediaResult] = field(default_factory=list)
    content_opportunities: List[str] = field(default_factory=list)
    competitive_landscape: str = ""
    user_questions: List[str] = field(default_factory=list)
    retrieval_timestamp: float = field(default_factory=lambda: datetime.now().timestamp())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "keyword": self.keyword,
            "user_goal": self.user_goal,
            "search_intent": self.search_intent,
            "related_keywords": self.related_keywords,
            "wikipedia_data": [
                {
                    "title": w.title,
                    "snippet": w.snippet,
                    "url": w.url,
                    "relevance_score": w.relevance_score
                } for w in self.wikipedia_data
            ],
            "content_opportunities": self.content_opportunities,
            "competitive_landscape": self.competitive_landscape,
            "user_questions": self.user_questions,
            "retrieval_timestamp": self.retrieval_timestamp
        }


@dataclass
class ContentBrief:
    """Structured output for content briefs"""
    keyword: str
    title: str
    meta_description: str
    outline: List[str]
    word_count_target: int
    internal_links: List[str] = field(default_factory=list)
    cta_suggestions: List[str] = field(default_factory=list)
    optimization_tips: List[str] = field(default_factory=list)
    content_type: ContentType = ContentType.BLOG_POST
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "keyword": self.keyword,
            "title": self.title,
            "meta_description": self.meta_description,
            "outline": self.outline,
            "word_count_target": self.word_count_target,
            "internal_links": self.internal_links,
            "cta_suggestions": self.cta_suggestions,
            "optimization_tips": self.optimization_tips,
            "content_type": self.content_type.value,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class ContentSection:
    """Individual content section"""
    heading: str
    content: str
    word_count: int = 0
    
    def __post_init__(self):
        if self.word_count == 0:
            self.word_count = len(self.content.split())


@dataclass 
class FullArticle:
    """Complete article with all sections"""
    keyword: str
    title: str
    meta_description: str
    introduction: str
    sections: List[ContentSection]
    conclusion: str
    total_word_count: int = 0
    content_brief: Optional[ContentBrief] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if self.total_word_count == 0:
            intro_words = len(self.introduction.split())
            section_words = sum(section.word_count for section in self.sections)
            conclusion_words = len(self.conclusion.split())
            self.total_word_count = intro_words + section_words + conclusion_words
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "keyword": self.keyword,
            "title": self.title,
            "meta_description": self.meta_description,
            "introduction": self.introduction,
            "sections": [
                {
                    "heading": section.heading,
                    "content": section.content,
                    "word_count": section.word_count
                } for section in self.sections
            ],
            "conclusion": self.conclusion,
            "total_word_count": self.total_word_count,
            "content_brief": self.content_brief.to_dict() if self.content_brief else None,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class ContentCalendarItem:
    """Single item in content calendar"""
    keyword: str
    title: str
    content_type: ContentType
    priority_score: float
    estimated_difficulty: str
    target_week: int
    search_intent: SearchIntent = SearchIntent.INFORMATIONAL
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "keyword": self.keyword,
            "title": self.title,
            "content_type": self.content_type.value,
            "priority_score": self.priority_score,
            "estimated_difficulty": self.estimated_difficulty,
            "target_week": self.target_week,
            "search_intent": self.search_intent.value
        }


@dataclass
class ContentCalendar:
    """Content calendar for multiple keywords"""
    timeframe_weeks: int
    total_keywords: int
    schedule: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_item(self, item: ContentCalendarItem):
        """Add item to appropriate week"""
        week_data = None
        for week in self.schedule:
            if week["week"] == item.target_week:
                week_data = week
                break
        
        if not week_data:
            week_data = {
                "week": item.target_week,
                "items": [],
                "focus_keyword": "",
                "content_types": set()
            }
            self.schedule.append(week_data)
        
        week_data["items"].append(item.to_dict())
        week_data["content_types"].add(item.content_type.value)
        
        # Set focus keyword to highest priority item
        if not week_data["focus_keyword"] or item.priority_score > max(
            [i.get("priority_score", 0) for i in week_data["items"]]
        ):
            week_data["focus_keyword"] = item.keyword
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timeframe_weeks": self.timeframe_weeks,
            "total_keywords": self.total_keywords,
            "schedule": [
                {
                    **week,
                    "content_types": list(week["content_types"]) if isinstance(week["content_types"], set) else week["content_types"]
                } for week in self.schedule
            ],
            "created_at": self.created_at.isoformat()
        }


@dataclass
class PerformanceMetrics:
    """Performance tracking for keywords"""
    keyword: str
    impressions: int = 0
    clicks: int = 0
    position: float = 0.0
    ctr: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "keyword": self.keyword,
            "impressions": self.impressions,
            "clicks": self.clicks,
            "position": self.position,
            "ctr": self.ctr,
            "last_updated": self.last_updated.isoformat()
        }


@dataclass
class PipelineConfig:
    """Configuration for SEO pipeline"""
    gemini_api_key: str
    gemini_model: str = "gemini-1.5-flash"
    max_retries: int = 3
    timeout: int = 10
    cache_enabled: bool = True
    cache_ttl: int = 3600
    debug_mode: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "gemini_model": self.gemini_model,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "cache_enabled": self.cache_enabled,
            "cache_ttl": self.cache_ttl,
            "debug_mode": self.debug_mode
        }
