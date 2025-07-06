"""
AI Content Generation Component for SEO Assistant Pipeline
Handles content generation using Google Gemini API
"""

import time
import logging
from typing import Dict, List, Optional, Any

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from ..entity import SEOContext, ContentBrief, ContentSection, FullArticle, ContentType
from ..utils import retry_with_backoff, validate_seo_elements, estimate_reading_time
from ..constants import (
    GEMINI_MODEL_NAME, 
    DEFAULT_WORD_COUNT_TARGET, 
    MIN_WORD_COUNT, 
    MAX_WORD_COUNT,
    META_DESCRIPTION_MAX_LENGTH,
    TITLE_OPTIMAL_LENGTH
)


class ContentGenerator:
    """Generates SEO-optimized content using Google Gemini AI"""
    
    def __init__(self, api_key: str, model_name: str = GEMINI_MODEL_NAME):
        """
        Initialize content generator
        
        Args:
            api_key: Google Gemini API key
            model_name: Gemini model to use
        """
        self.api_key = api_key
        self.model_name = model_name
        self.logger = logging.getLogger(__name__)
        
        if not genai:
            raise ImportError("google-generativeai package not installed")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        self.logger.info(f"ContentGenerator initialized with model: {model_name}")
    
    def _format_context_for_prompt(self, context: SEOContext) -> str:
        """
        Format SEO context for AI prompts
        
        Args:
            context: SEO context data
            
        Returns:
            Formatted context string
        """
        wikipedia_summary = ""
        for i, result in enumerate(context.wikipedia_data[:3], 1):
            wikipedia_summary += f"\n{i}. {result.title}: {result.snippet[:200]}..."
        
        formatted_context = f"""
        === SEO CONTEXT FOR "{context.keyword.upper()}" ===
        
        PRIMARY KEYWORD: {context.keyword}
        USER GOAL: {context.user_goal or "Generate comprehensive SEO content"}
        SEARCH INTENT: {context.search_intent}
        
        KNOWLEDGE BASE:{wikipedia_summary}
        
        RELATED KEYWORDS: {', '.join(context.related_keywords[:8])}
        
        CONTENT OPPORTUNITIES:
        {chr(10).join([f"- {opp}" for opp in context.content_opportunities[:6]])}
        
        USER QUESTIONS:
        {chr(10).join([f"- {q}" for q in context.user_questions[:5]])}
        
        COMPETITIVE LANDSCAPE: {context.competitive_landscape}
        
        === END CONTEXT ===
        """
        
        return formatted_context
    
    @retry_with_backoff(max_retries=3)
    def generate_title(self, context: SEOContext) -> str:
        """
        Generate SEO-optimized title
        
        Args:
            context: SEO context
            
        Returns:
            Generated title
        """
        self.logger.info(f"Generating title for: {context.keyword}")
        
        formatted_context = self._format_context_for_prompt(context)
        
        prompt = f"""
        {formatted_context}
        
        Generate an SEO-optimized blog post title that:
        1. Includes the primary keyword naturally
        2. Is compelling and click-worthy
        3. Is {TITLE_OPTIMAL_LENGTH} characters or less
        4. Matches the search intent
        5. Stands out from competitors
        
        Consider the user goal and target audience.
        Respond with ONLY the title, no explanations or quotes.
        """
        
        try:
            response = self.model.generate_content(prompt)
            title = response.text.strip().replace('"', '').replace("'", "")
            
            # Ensure title length
            if len(title) > TITLE_OPTIMAL_LENGTH:
                title = title[:TITLE_OPTIMAL_LENGTH].rsplit(' ', 1)[0]
            
            self.logger.info(f"Generated title: {title}")
            return title
            
        except Exception as e:
            self.logger.error(f"Failed to generate title: {e}")
            return f"The Complete Guide to {context.keyword.title()}"
    
    @retry_with_backoff(max_retries=3)
    def generate_meta_description(self, context: SEOContext, title: str) -> str:
        """
        Generate SEO-optimized meta description
        
        Args:
            context: SEO context
            title: Article title
            
        Returns:
            Generated meta description
        """
        self.logger.info(f"Generating meta description for: {context.keyword}")
        
        formatted_context = self._format_context_for_prompt(context)
        
        prompt = f"""
        {formatted_context}
        
        Title: {title}
        
        Generate a meta description that:
        1. Is 120-{META_DESCRIPTION_MAX_LENGTH} characters
        2. Includes the primary keyword naturally
        3. Is compelling and action-oriented
        4. Summarizes the value proposition
        5. Encourages clicks
        
        Respond with ONLY the meta description, no explanations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            meta_desc = response.text.strip()
            
            # Ensure length constraints
            if len(meta_desc) > META_DESCRIPTION_MAX_LENGTH:
                meta_desc = meta_desc[:META_DESCRIPTION_MAX_LENGTH].rsplit(' ', 1)[0] + "..."
            
            self.logger.info(f"Generated meta description ({len(meta_desc)} chars)")
            return meta_desc
            
        except Exception as e:
            self.logger.error(f"Failed to generate meta description: {e}")
            return f"Learn everything about {context.keyword} in this comprehensive guide. Expert tips, best practices, and actionable insights."
    
    @retry_with_backoff(max_retries=3)
    def generate_outline(self, context: SEOContext, title: str) -> List[str]:
        """
        Generate detailed content outline
        
        Args:
            context: SEO context
            title: Article title
            
        Returns:
            List of outline items
        """
        self.logger.info(f"Generating outline for: {context.keyword}")
        
        formatted_context = self._format_context_for_prompt(context)
        
        prompt = f"""
        {formatted_context}
        
        Title: {title}
        
        Create a detailed blog post outline with:
        1. Introduction (hook, problem, preview)
        2. 5-7 main sections (H2 level)
        3. 2-3 subsections per main section (H3 level)
        4. Conclusion with CTA
        
        Make it logical, comprehensive, and SEO-friendly.
        Address the user questions and content opportunities.
        
        Format as a numbered list with clear hierarchy.
        Use "1.", "2." for main sections and "a.", "b." for subsections.
        """
        
        try:
            response = self.model.generate_content(prompt)
            outline_text = response.text.strip()
            
            # Parse outline into list
            outline_lines = [line.strip() for line in outline_text.split('\n') if line.strip()]
            
            # Clean up formatting
            cleaned_outline = []
            for line in outline_lines:
                if line and not line.startswith('#'):
                    cleaned_outline.append(line)
            
            self.logger.info(f"Generated outline with {len(cleaned_outline)} sections")
            return cleaned_outline
            
        except Exception as e:
            self.logger.error(f"Failed to generate outline: {e}")
            return [
                "1. Introduction",
                "2. What is " + context.keyword.title(),
                "3. Benefits and Importance",
                "4. Best Practices",
                "5. Common Mistakes to Avoid",
                "6. Tools and Resources",
                "7. Conclusion"
            ]
    
    @retry_with_backoff(max_retries=3)
    def determine_word_count(self, context: SEOContext) -> int:
        """
        Determine optimal word count for content
        
        Args:
            context: SEO context
            
        Returns:
            Recommended word count
        """
        self.logger.info(f"Determining word count for: {context.keyword}")
        
        formatted_context = self._format_context_for_prompt(context)
        
        prompt = f"""
        {formatted_context}
        
        Based on the search intent, topic complexity, and competitive landscape,
        what would be the optimal word count for this content?
        
        Consider:
        - Search intent type (informational content typically needs more depth)
        - Topic complexity and breadth
        - User expectations
        - Competitive requirements
        
        Respond with just a number between {MIN_WORD_COUNT} and {MAX_WORD_COUNT}.
        """
        
        try:
            response = self.model.generate_content(prompt)
            word_count_text = response.text.strip()
            
            # Extract number from response
            import re
            numbers = re.findall(r'\d+', word_count_text)
            if numbers:
                word_count = int(numbers[0])
                word_count = max(MIN_WORD_COUNT, min(MAX_WORD_COUNT, word_count))
            else:
                word_count = DEFAULT_WORD_COUNT_TARGET
            
            self.logger.info(f"Determined word count: {word_count}")
            return word_count
            
        except Exception as e:
            self.logger.error(f"Failed to determine word count: {e}")
            return DEFAULT_WORD_COUNT_TARGET
    
    def generate_internal_links(self, context: SEOContext) -> List[str]:
        """
        Generate internal linking suggestions
        
        Args:
            context: SEO context
            
        Returns:
            List of internal link suggestions
        """
        suggestions = []
        
        # Generate suggestions based on related keywords
        for keyword in context.related_keywords[:5]:
            suggestions.append(f"Link to comprehensive guide on '{keyword}'")
            suggestions.append(f"Internal link to '{keyword}' resources page")
        
        # Add general suggestions
        suggestions.extend([
            f"Link to {context.keyword} tutorials or how-to guides",
            f"Cross-reference to related {context.keyword} topics",
            f"Link to {context.keyword} tools and resources page"
        ])
        
        return suggestions[:6]
    
    def generate_cta_suggestions(self, context: SEOContext) -> List[str]:
        """
        Generate call-to-action suggestions
        
        Args:
            context: SEO context
            
        Returns:
            List of CTA suggestions
        """
        ctas = [
            f"Ready to master {context.keyword}? Start your journey today!",
            f"Download our free {context.keyword} checklist",
            f"Get expert {context.keyword} consultation",
            f"Join our {context.keyword} community",
            f"Subscribe for more {context.keyword} tips",
            f"Share this {context.keyword} guide with your team"
        ]
        
        return ctas[:4]
    
    def generate_optimization_tips(self, context: SEOContext) -> List[str]:
        """
        Generate SEO optimization tips
        
        Args:
            context: SEO context
            
        Returns:
            List of optimization tips
        """
        tips = [
            f"Include '{context.keyword}' in H1 and first paragraph",
            f"Use related keywords naturally: {', '.join(context.related_keywords[:3])}",
            "Add internal links to relevant pages",
            "Optimize images with descriptive alt text",
            "Include FAQ section for featured snippets",
            "Use structured data markup (JSON-LD)",
            "Ensure mobile-friendly responsive design",
            "Optimize page loading speed",
            "Add social sharing buttons",
            "Include author bio and expertise signals"
        ]
        
        return tips[:7]
    
    def generate_content_brief(self, context: SEOContext) -> ContentBrief:
        """
        Generate complete content brief
        
        Args:
            context: SEO context
            
        Returns:
            ContentBrief object
        """
        self.logger.info(f"Generating content brief for: {context.keyword}")
        
        start_time = time.time()
        
        # Generate all components
        title = self.generate_title(context)
        meta_description = self.generate_meta_description(context, title)
        outline = self.generate_outline(context, title)
        word_count = self.determine_word_count(context)
        internal_links = self.generate_internal_links(context)
        cta_suggestions = self.generate_cta_suggestions(context)
        optimization_tips = self.generate_optimization_tips(context)
        
        # Create content brief
        brief = ContentBrief(
            keyword=context.keyword,
            title=title,
            meta_description=meta_description,
            outline=outline,
            word_count_target=word_count,
            internal_links=internal_links,
            cta_suggestions=cta_suggestions,
            optimization_tips=optimization_tips,
            content_type=ContentType.BLOG_POST
        )
        
        generation_time = time.time() - start_time
        self.logger.info(f"Content brief generated in {generation_time:.2f} seconds")
        
        return brief
    
    @retry_with_backoff(max_retries=3)
    def generate_section_content(self, section_title: str, keyword: str, article_title: str, target_words: int = 300) -> str:
        """
        Generate content for a specific section
        
        Args:
            section_title: Title of the section
            keyword: Target keyword
            article_title: Main article title
            target_words: Target word count for section
            
        Returns:
            Generated section content
        """
        self.logger.info(f"Generating section: {section_title}")
        
        prompt = f"""
        Write a detailed section for an article titled "{article_title}".
        
        Section Title: {section_title}
        Target Keyword: {keyword}
        Target Length: {target_words} words
        
        Requirements:
        1. Provide actionable, valuable information
        2. Include the target keyword naturally (don't over-optimize)
        3. Use clear, engaging language
        4. Include specific examples where relevant
        5. Break up text with bullet points or numbered lists when appropriate
        6. Make it scannable and readable
        
        Write ONLY the section content, no title or heading.
        """
        
        try:
            response = self.model.generate_content(prompt)
            content = response.text.strip()
            
            self.logger.info(f"Generated section content ({len(content.split())} words)")
            return content
            
        except Exception as e:
            self.logger.error(f"Failed to generate section content: {e}")
            return f"Content for {section_title} section would be generated here. This section would cover key aspects of {keyword} related to {section_title.lower()}."
    
    def generate_full_article(self, context: SEOContext, content_brief: Optional[ContentBrief] = None) -> FullArticle:
        """
        Generate complete article from context
        
        Args:
            context: SEO context
            content_brief: Optional pre-generated content brief
            
        Returns:
            FullArticle object
        """
        self.logger.info(f"Generating full article for: {context.keyword}")
        
        start_time = time.time()
        
        # Generate content brief if not provided
        if not content_brief:
            content_brief = self.generate_content_brief(context)
        
        # Generate introduction
        intro_prompt = f"""
        Write an engaging introduction for an article titled "{content_brief.title}" about "{context.keyword}".
        
        Requirements:
        - 150-200 words
        - Hook the reader immediately  
        - Include the target keyword in the first sentence
        - Preview what the article will cover
        - Set clear expectations
        - Address the user's search intent: {context.search_intent}
        """
        
        try:
            intro_response = self.model.generate_content(intro_prompt)
            introduction = intro_response.text.strip()
        except Exception as e:
            self.logger.error(f"Failed to generate introduction: {e}")
            introduction = f"In this comprehensive guide, we'll explore everything you need to know about {context.keyword}. Whether you're a beginner or looking to advance your knowledge, this article will provide valuable insights and practical tips."
        
        # Generate sections (limit to first 6 for performance)
        sections = []
        target_section_words = content_brief.word_count_target // min(len(content_brief.outline), 6)
        
        for section_title in content_brief.outline[:6]:
            content = self.generate_section_content(
                section_title, 
                context.keyword, 
                content_brief.title,
                target_section_words
            )
            
            sections.append(ContentSection(
                heading=section_title,
                content=content
            ))
        
        # Generate conclusion
        conclusion_prompt = f"""
        Write a compelling conclusion for an article titled "{content_brief.title}" about "{context.keyword}".
        
        Requirements:
        - 150-200 words
        - Summarize key takeaways
        - Include a clear call-to-action
        - Reinforce the value provided
        - End with actionable next steps for the reader
        """
        
        try:
            conclusion_response = self.model.generate_content(conclusion_prompt)
            conclusion = conclusion_response.text.strip()
        except Exception as e:
            self.logger.error(f"Failed to generate conclusion: {e}")
            conclusion = f"Understanding {context.keyword} is essential for success in today's digital landscape. By implementing the strategies and best practices outlined in this guide, you'll be well-equipped to achieve your goals. Start applying these insights today and see the difference they can make."
        
        # Create full article
        article = FullArticle(
            keyword=context.keyword,
            title=content_brief.title,
            meta_description=content_brief.meta_description,
            introduction=introduction,
            sections=sections,
            conclusion=conclusion,
            content_brief=content_brief
        )
        
        generation_time = time.time() - start_time
        self.logger.info(f"Full article generated in {generation_time:.2f} seconds ({article.total_word_count} words)")
        
        return article
