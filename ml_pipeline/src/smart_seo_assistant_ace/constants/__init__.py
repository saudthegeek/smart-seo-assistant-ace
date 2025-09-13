import os

# SEO Assistant Constants

# API Configuration
# Default to Gemini for current generator implementation; allow override via COMPLETION_MODEL
GEMINI_MODEL_NAME = os.getenv("COMPLETION_MODEL", "gemini-1.5-flash")
DEFAULT_TIMEOUT = 10
MAX_RETRIES = 3

# Content Configuration
DEFAULT_WORD_COUNT_TARGET = 1500
MIN_WORD_COUNT = 800
MAX_WORD_COUNT = 5000
META_DESCRIPTION_MAX_LENGTH = 155
TITLE_OPTIMAL_LENGTH = 60

# Context Configuration
MAX_CONTEXT_LENGTH = 8000
WIKIPEDIA_RESULTS_LIMIT = 5
RELATED_KEYWORDS_LIMIT = 10
CONTENT_OPPORTUNITIES_LIMIT = 8
USER_QUESTIONS_LIMIT = 8

# Search Intent Types
SEARCH_INTENTS = [
    "informational",
    "navigational", 
    "transactional",
    "commercial"
]

# Content Types
CONTENT_TYPES = [
    "blog_post",
    "guide",
    "tutorial",
    "comparison",
    "listicle",
    "how_to",
    "review"
]

# Cache Configuration
CONTEXT_CACHE_TTL = 3600  # 1 hour in seconds
MAX_CACHE_SIZE = 100

# Performance Metrics
PERFORMANCE_METRICS = [
    "impressions",
    "clicks", 
    "position",
    "ctr"
]
