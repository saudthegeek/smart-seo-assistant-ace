"""
Data Retrieval Component for SEO Assistant Pipeline
Handles fetching data from various sources (Wikipedia, search APIs, etc.)
"""

import time
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote_plus

try:
    import requests
except ImportError:
    requests = None

from ..entity import SEOContext, WikipediaResult, SearchIntent
from ..utils import retry_with_backoff, calculate_text_similarity, clean_text, extract_keywords_from_text
from ..constants import WIKIPEDIA_RESULTS_LIMIT, DEFAULT_TIMEOUT, MAX_RETRIES


class DataRetriever:
    """Handles data retrieval from various sources for SEO content generation"""
    
    def __init__(self, timeout: int = DEFAULT_TIMEOUT, max_retries: int = MAX_RETRIES):
        """
        Initialize data retriever
        
        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts for failed requests
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)
        
        if not requests:
            self.logger.warning("Requests library not available, some features may be limited")
    
    @retry_with_backoff(max_retries=3)
    def fetch_wikipedia_data(self, keyword: str, limit: int = WIKIPEDIA_RESULTS_LIMIT) -> List[WikipediaResult]:
        """
        Fetch Wikipedia articles related to the keyword
        
        Args:
            keyword: Search keyword
            limit: Maximum number of results
            
        Returns:
            List of WikipediaResult objects
        """
        if not requests:
            self.logger.error("Cannot fetch Wikipedia data: requests library not available")
            return []
        
        self.logger.info(f"Fetching Wikipedia data for: {keyword}")
        
        try:
            # Use Wikipedia search API
            search_url = "https://en.wikipedia.org/w/api.php"
            search_params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": keyword,
                "srlimit": limit,
                "srprop": "snippet|titlesnippet"
            }
            
            response = requests.get(search_url, params=search_params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for page in data.get("query", {}).get("search", []):
                title = page.get("title", "")
                snippet = clean_text(page.get("snippet", ""))
                
                # Remove search highlight tags
                snippet = snippet.replace("<span class=\"searchmatch\">", "").replace("</span>", "")
                
                url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                
                # Calculate relevance score
                relevance_score = self._calculate_relevance_score(keyword, title, snippet)
                
                results.append(WikipediaResult(
                    title=title,
                    snippet=snippet,
                    url=url,
                    relevance_score=relevance_score
                ))
            
            # Sort by relevance score
            results.sort(key=lambda x: x.relevance_score, reverse=True)
            
            self.logger.info(f"Retrieved {len(results)} Wikipedia results")
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to fetch Wikipedia data: {e}")
            return []
    
    def _calculate_relevance_score(self, keyword: str, title: str, snippet: str) -> float:
        """
        Calculate relevance score for Wikipedia result
        
        Args:
            keyword: Search keyword
            title: Article title
            snippet: Article snippet
            
        Returns:
            Relevance score (0.0 to 1.0)
        """
        score = 0.0
        keyword_lower = keyword.lower()
        
        # Title relevance (weighted heavily)
        title_similarity = calculate_text_similarity(keyword_lower, title.lower())
        score += title_similarity * 0.6
        
        # Snippet relevance
        snippet_similarity = calculate_text_similarity(keyword_lower, snippet.lower())
        score += snippet_similarity * 0.3
        
        # Exact keyword matches
        exact_matches = title.lower().count(keyword_lower) + snippet.lower().count(keyword_lower)
        score += min(exact_matches * 0.1, 0.1)  # Cap at 0.1
        
        return min(score, 1.0)
    
    def extract_related_keywords(self, keyword: str, wikipedia_results: List[WikipediaResult], limit: int = 10) -> List[str]:
        """
        Extract related keywords from Wikipedia content
        
        Args:
            keyword: Primary keyword
            wikipedia_results: Wikipedia search results
            limit: Maximum number of related keywords
            
        Returns:
            List of related keywords
        """
        self.logger.info(f"Extracting related keywords for: {keyword}")
        
        all_text = f"{keyword} "
        
        # Combine all Wikipedia text
        for result in wikipedia_results:
            all_text += f"{result.title} {result.snippet} "
        
        # Extract keywords
        potential_keywords = extract_keywords_from_text(all_text, min_length=4)
        
        # Filter out the original keyword and common stop words
        stop_words = {
            'this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 'their',
            'said', 'each', 'which', 'what', 'where', 'when', 'more', 'very', 'some',
            'could', 'other', 'after', 'first', 'well', 'many', 'most', 'also'
        }
        
        keyword_lower = keyword.lower()
        related_keywords = []
        
        for kw in potential_keywords:
            kw_lower = kw.lower()
            if (kw_lower != keyword_lower and 
                kw_lower not in stop_words and 
                len(kw) > 3 and
                kw not in related_keywords):
                related_keywords.append(kw)
        
        # Sort by length and relevance (longer keywords first)
        related_keywords.sort(key=lambda x: (len(x), -all_text.lower().count(x.lower())), reverse=True)
        
        return related_keywords[:limit]
    
    def generate_content_opportunities(self, keyword: str, wikipedia_results: List[WikipediaResult], limit: int = 8) -> List[str]:
        """
        Generate content opportunities based on retrieved data
        
        Args:
            keyword: Primary keyword
            wikipedia_results: Wikipedia search results
            limit: Maximum number of opportunities
            
        Returns:
            List of content opportunity suggestions
        """
        self.logger.info(f"Generating content opportunities for: {keyword}")
        
        opportunities = []
        
        # Base content types
        base_opportunities = [
            f"The Complete Guide to {keyword.title()}",
            f"{keyword.title()} for Beginners: Everything You Need to Know",
            f"Best {keyword.title()} Practices in 2025",
            f"{keyword.title()} vs Alternatives: Comprehensive Comparison",
            f"Common {keyword.title()} Mistakes and How to Avoid Them"
        ]
        
        opportunities.extend(base_opportunities)
        
        # Wikipedia-based opportunities
        for result in wikipedia_results[:3]:  # Use top 3 results
            title = result.title
            opportunities.extend([
                f"How {title} Relates to {keyword.title()}",
                f"Understanding {title}: A {keyword.title()} Perspective",
                f"The Role of {title} in Modern {keyword.title()}"
            ])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_opportunities = []
        for opp in opportunities:
            if opp not in seen:
                seen.add(opp)
                unique_opportunities.append(opp)
        
        return unique_opportunities[:limit]
    
    def extract_user_questions(self, keyword: str, wikipedia_results: List[WikipediaResult], limit: int = 8) -> List[str]:
        """
        Extract and generate common user questions
        
        Args:
            keyword: Primary keyword
            wikipedia_results: Wikipedia search results
            limit: Maximum number of questions
            
        Returns:
            List of user questions
        """
        self.logger.info(f"Extracting user questions for: {keyword}")
        
        questions = []
        
        # Base question templates
        base_questions = [
            f"What is {keyword}?",
            f"How does {keyword} work?",
            f"Why is {keyword} important?",
            f"What are the benefits of {keyword}?",
            f"How to get started with {keyword}?",
            f"What are common {keyword} mistakes?",
            f"Best {keyword} tools and resources?",
            f"How to improve your {keyword} skills?"
        ]
        
        questions.extend(base_questions)
        
        # Generate questions based on Wikipedia content
        for result in wikipedia_results[:2]:
            title = result.title
            questions.extend([
                f"How is {title} related to {keyword}?",
                f"What role does {title} play in {keyword}?",
                f"Should I learn about {title} for {keyword}?"
            ])
        
        # Remove duplicates
        seen = set()
        unique_questions = []
        for q in questions:
            if q not in seen:
                seen.add(q)
                unique_questions.append(q)
        
        return unique_questions[:limit]
    
    def analyze_search_intent(self, keyword: str, context: str = "") -> Tuple[SearchIntent, str]:
        """
        Analyze search intent for the keyword
        
        Args:
            keyword: Keyword to analyze
            context: Additional context
            
        Returns:
            Tuple of (SearchIntent enum, explanation string)
        """
        self.logger.info(f"Analyzing search intent for: {keyword}")
        
        keyword_lower = keyword.lower()
        
        # Transactional indicators
        transactional_words = ['buy', 'purchase', 'order', 'price', 'cost', 'cheap', 'discount', 'deal']
        if any(word in keyword_lower for word in transactional_words):
            return SearchIntent.TRANSACTIONAL, "User appears to be ready to make a purchase or transaction"
        
        # Commercial investigation indicators
        commercial_words = ['best', 'top', 'review', 'compare', 'vs', 'alternative', 'recommendation']
        if any(word in keyword_lower for word in commercial_words):
            return SearchIntent.COMMERCIAL, "User is researching options before making a decision"
        
        # Navigational indicators
        if any(word in keyword_lower for word in ['login', 'sign in', 'website', 'official']):
            return SearchIntent.NAVIGATIONAL, "User is looking for a specific website or page"
        
        # How-to and tutorial indicators
        how_to_words = ['how to', 'tutorial', 'guide', 'learn', 'step by step']
        if any(word in keyword_lower for word in how_to_words):
            return SearchIntent.INFORMATIONAL, "User wants to learn how to do something"
        
        # Question indicators
        question_words = ['what', 'why', 'when', 'where', 'who', 'which', 'how']
        if any(keyword_lower.startswith(word) for word in question_words):
            return SearchIntent.INFORMATIONAL, "User is seeking information or answers"
        
        # Default to informational
        return SearchIntent.INFORMATIONAL, "General information seeking intent"
    
    def get_comprehensive_context(self, keyword: str, user_goal: str = "") -> SEOContext:
        """
        Get comprehensive context for a keyword
        
        Args:
            keyword: Primary keyword
            user_goal: User's goal or additional context
            
        Returns:
            SEOContext object with all retrieved data
        """
        self.logger.info(f"Building comprehensive context for: {keyword}")
        
        start_time = time.time()
        
        # Fetch Wikipedia data
        wikipedia_results = self.fetch_wikipedia_data(keyword)
        
        # Extract related information
        related_keywords = self.extract_related_keywords(keyword, wikipedia_results)
        content_opportunities = self.generate_content_opportunities(keyword, wikipedia_results)
        user_questions = self.extract_user_questions(keyword, wikipedia_results)
        
        # Analyze search intent
        search_intent, intent_explanation = self.analyze_search_intent(keyword, user_goal)
        
        # Build context
        context = SEOContext(
            keyword=keyword,
            user_goal=user_goal,
            search_intent=f"{search_intent.value}: {intent_explanation}",
            related_keywords=related_keywords,
            wikipedia_data=wikipedia_results,
            content_opportunities=content_opportunities,
            competitive_landscape="Medium difficulty - requires quality content and proper optimization",
            user_questions=user_questions,
            retrieval_timestamp=time.time()
        )
        
        processing_time = time.time() - start_time
        self.logger.info(f"Context building completed in {processing_time:.2f} seconds")
        
        return context
