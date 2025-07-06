"""
Pydantic models for the SEO Assistant Backend API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# User management models
class UserCreate(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    full_name: str = Field(..., description="User full name")


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    created_at: datetime
    is_active: bool = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# Project management models
class ProjectCreate(BaseModel):
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    website_url: Optional[str] = Field(None, description="Target website URL")
    target_audience: Optional[str] = Field(None, description="Target audience")
    goals: Optional[List[str]] = Field(default_factory=list, description="Project goals")


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    target_audience: Optional[str] = None
    goals: Optional[List[str]] = None


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    website_url: Optional[str]
    target_audience: Optional[str]
    goals: List[str]
    created_at: datetime
    updated_at: datetime
    user_id: str


# SEO analysis models
class KeywordAnalysisRequest(BaseModel):
    keyword: str = Field(..., description="Keyword to analyze")
    goal: Optional[str] = Field("", description="Specific goal or context")
    project_id: Optional[str] = Field(None, description="Associated project ID")


class WikipediaSource(BaseModel):
    title: str
    url: str
    relevance_score: float


class KeywordAnalysisResponse(BaseModel):
    keyword: str
    search_intent: str
    related_keywords: List[str]
    content_opportunities: List[str]
    user_questions: List[str]
    wikipedia_sources: List[WikipediaSource]


# Content brief models
class ContentBriefRequest(BaseModel):
    keyword: str = Field(..., description="Target keyword")
    goal: Optional[str] = Field("", description="Content goal or context")
    project_id: Optional[str] = Field(None, description="Associated project ID")


class ContentBriefResponse(BaseModel):
    title: str
    meta_description: str
    content_type: str
    word_count_target: int
    outline: List[str]
    call_to_action: str
    created_at: str


# Full article models
class ArticleSection(BaseModel):
    heading: str
    content: str
    word_count: int


class FullArticleResponse(BaseModel):
    title: str
    meta_description: str
    total_word_count: int
    sections: List[ArticleSection]
    keyword: str
    goal: str
    created_at: str


# Bulk processing models
class BulkProcessRequest(BaseModel):
    keywords: List[str] = Field(..., description="List of keywords to process")
    goal: Optional[str] = Field("", description="Common goal for all keywords")
    project_id: Optional[str] = Field(None, description="Associated project ID")


class BulkResultItem(BaseModel):
    keyword: str
    status: str
    title: Optional[str] = None
    word_count_target: Optional[int] = None
    error: Optional[str] = None


class BulkSummary(BaseModel):
    total_keywords: int
    successful: int
    failed: int
    success_rate: float


class BulkProcessResponse(BaseModel):
    summary: BulkSummary
    results: List[BulkResultItem]


# Content calendar models
class ContentCalendarRequest(BaseModel):
    keywords: List[str] = Field(..., description="Keywords for content calendar")
    goal: Optional[str] = Field("", description="Content goal or context")
    timeframe_weeks: int = Field(4, description="Calendar timeframe in weeks")
    project_id: Optional[str] = Field(None, description="Associated project ID")


class CalendarItem(BaseModel):
    keyword: str
    title: str
    content_type: str
    priority_score: float
    target_week: int
    estimated_difficulty: str


class ContentCalendarResponse(BaseModel):
    timeframe_weeks: int
    total_keywords: int
    items: List[CalendarItem]
    created_at: str


# Error models
class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: str


# Task models
class TaskResponse(BaseModel):
    task_id: str
    status: str  # processing, completed, failed
    progress: int  # 0-100
    message: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
