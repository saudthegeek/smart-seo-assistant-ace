"""
Utility functions for SEO Assistant Pipeline
Common helper functions used across the pipeline
"""

import time
import logging
import requests
from typing import Dict, List, Any, Optional
from functools import wraps
import hashlib
import json


def setup_logging(debug_mode: bool = False) -> logging.Logger:
    """
    Setup logging configuration
    
    Args:
        debug_mode: Enable debug level logging
        
    Returns:
        Logger instance
    """
    level = logging.DEBUG if debug_mode else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    return logging.getLogger(__name__)


def retry_with_backoff(max_retries: int = 3, backoff_factor: float = 1.0):
    """
    Decorator for retrying functions with exponential backoff
    
    Args:
        max_retries: Maximum number of retry attempts
        backoff_factor: Factor for exponential backoff
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    
                    if attempt == max_retries:
                        break
                    
                    # Calculate delay with exponential backoff
                    delay = backoff_factor * (2 ** attempt)
                    time.sleep(delay)
                    
            raise last_exception
        return wrapper
    return decorator


def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate simple text similarity score
    
    Args:
        text1: First text string
        text2: Second text string
        
    Returns:
        Similarity score between 0 and 1
    """
    if not text1 or not text2:
        return 0.0
    
    # Convert to lowercase and split into words
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    # Calculate Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return intersection / union if union > 0 else 0.0


def clean_text(text: str) -> str:
    """
    Clean and normalize text
    
    Args:
        text: Raw text string
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove HTML tags (basic)
    import re
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\!\?\-\:\;]', '', text)
    
    return text.strip()


def extract_keywords_from_text(text: str, min_length: int = 4) -> List[str]:
    """
    Extract potential keywords from text
    
    Args:
        text: Text to extract keywords from
        min_length: Minimum keyword length
        
    Returns:
        List of potential keywords
    """
    if not text:
        return []
    
    import re
    
    # Clean text first
    cleaned_text = clean_text(text)
    
    # Split into words
    words = cleaned_text.lower().split()
    
    # Filter words
    keywords = []
    for word in words:
        # Remove punctuation and check length
        clean_word = re.sub(r'[^\w]', '', word)
        if len(clean_word) >= min_length and clean_word.isalpha():
            keywords.append(clean_word.title())
    
    # Remove duplicates while preserving order
    seen = set()
    unique_keywords = []
    for keyword in keywords:
        if keyword not in seen:
            seen.add(keyword)
            unique_keywords.append(keyword)
    
    return unique_keywords


def generate_cache_key(keyword: str, user_goal: str = "") -> str:
    """
    Generate a cache key for storing context data
    
    Args:
        keyword: Primary keyword
        user_goal: User goal string
        
    Returns:
        Cache key string
    """
    # Combine keyword and user goal
    cache_input = f"{keyword.lower()}_{user_goal.lower()}"
    
    # Generate hash
    return hashlib.md5(cache_input.encode()).hexdigest()


def format_outline_as_html(outline: List[str]) -> str:
    """
    Format outline as HTML structure
    
    Args:
        outline: List of outline items
        
    Returns:
        HTML formatted outline
    """
    if not outline:
        return ""
    
    html_parts = ["<div class='content-outline'>"]
    
    for item in outline:
        # Determine heading level based on numbering/indentation
        if item.strip().startswith(('1.', '2.', '3.', '4.', '5.')):
            level = "h2"
        elif item.strip().startswith(('a.', 'b.', 'c.', '-', '•')):
            level = "h3"
        else:
            level = "h3"
        
        clean_item = item.strip().lstrip('1234567890.-•abcdefgh').strip()
        html_parts.append(f"<{level}>{clean_item}</{level}>")
    
    html_parts.append("</div>")
    return "\n".join(html_parts)


def validate_seo_elements(title: str, meta_description: str) -> Dict[str, Any]:
    """
    Validate SEO elements for best practices
    
    Args:
        title: Page title
        meta_description: Meta description
        
    Returns:
        Validation results with recommendations
    """
    results = {
        "title": {"valid": True, "issues": [], "score": 100},
        "meta_description": {"valid": True, "issues": [], "score": 100}
    }
    
    # Title validation
    title_length = len(title)
    if title_length < 30:
        results["title"]["issues"].append("Title too short (recommended: 30-60 characters)")
        results["title"]["score"] -= 20
    elif title_length > 60:
        results["title"]["issues"].append("Title too long (recommended: 30-60 characters)")
        results["title"]["score"] -= 10
    
    if not title:
        results["title"]["valid"] = False
        results["title"]["issues"].append("Title is required")
        results["title"]["score"] = 0
    
    # Meta description validation
    meta_length = len(meta_description)
    if meta_length < 120:
        results["meta_description"]["issues"].append("Meta description too short (recommended: 120-155 characters)")
        results["meta_description"]["score"] -= 15
    elif meta_length > 155:
        results["meta_description"]["issues"].append("Meta description too long (recommended: 120-155 characters)")
        results["meta_description"]["score"] -= 10
    
    if not meta_description:
        results["meta_description"]["valid"] = False
        results["meta_description"]["issues"].append("Meta description is required")
        results["meta_description"]["score"] = 0
    
    # Overall validation
    if results["title"]["issues"] or results["meta_description"]["issues"]:
        results["title"]["valid"] = results["title"]["score"] > 70
        results["meta_description"]["valid"] = results["meta_description"]["score"] > 70
    
    return results


def estimate_reading_time(word_count: int, wpm: int = 200) -> int:
    """
    Estimate reading time in minutes
    
    Args:
        word_count: Number of words
        wpm: Words per minute reading speed
        
    Returns:
        Estimated reading time in minutes
    """
    if word_count <= 0:
        return 0
    
    return max(1, round(word_count / wpm))


def generate_content_slug(title: str) -> str:
    """
    Generate URL-friendly slug from title
    
    Args:
        title: Article title
        
    Returns:
        URL slug
    """
    if not title:
        return ""
    
    import re
    
    # Convert to lowercase
    slug = title.lower()
    
    # Replace spaces and special characters with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_-]+', '-', slug)
    
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    # Limit length
    if len(slug) > 60:
        slug = slug[:60].rstrip('-')
    
    return slug


def safe_request(url: str, timeout: int = 10, **kwargs) -> Optional[requests.Response]:
    """
    Make a safe HTTP request with error handling
    
    Args:
        url: URL to request
        timeout: Request timeout in seconds
        **kwargs: Additional arguments for requests
        
    Returns:
        Response object or None if failed
    """
    try:
        response = requests.get(url, timeout=timeout, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.getLogger(__name__).error(f"Request failed for {url}: {e}")
        return None


def chunk_text(text: str, max_length: int = 2000, overlap: int = 100) -> List[str]:
    """
    Split text into chunks with overlap
    
    Args:
        text: Text to chunk
        max_length: Maximum chunk length
        overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    if not text or len(text) <= max_length:
        return [text] if text else []
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + max_length
        
        # Try to break at word boundary
        if end < len(text):
            # Find last space before the end
            last_space = text.rfind(' ', start, end)
            if last_space > start:
                end = last_space
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position with overlap
        start = max(start + 1, end - overlap)
    
    return chunks


def merge_dictionaries(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple dictionaries with conflict resolution
    
    Args:
        *dicts: Dictionaries to merge
        
    Returns:
        Merged dictionary
    """
    result = {}
    
    for d in dicts:
        for key, value in d.items():
            if key in result:
                # Handle conflicts - prioritize non-empty values
                if not result[key] and value:
                    result[key] = value
                elif isinstance(result[key], list) and isinstance(value, list):
                    result[key].extend(value)
                elif isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dictionaries(result[key], value)
            else:
                result[key] = value
    
    return result
