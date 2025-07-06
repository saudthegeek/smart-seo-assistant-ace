#!/usr/bin/env python3
"""
Smart SEO Assistant CLI
Command line interface for the SEO Assistant Pipeline

Usage:
    python -m smart_seo_assistant_ace.cli analyze "machine learning"
    python -m smart_seo_assistant_ace.cli brief "python tutorial" --goal="beginner-friendly"
    python -m smart_seo_assistant_ace.cli article "data science" --output="output.json"
    python -m smart_seo_assistant_ace.cli bulk keywords.txt --calendar
"""

import argparse
import json
import sys
import logging
from pathlib import Path
from typing import List, Optional

from .config.configuration import ConfigurationManager
from .pipeline.seo_pipeline import SEOAssistantPipeline
from .entity import PipelineConfig
from .utils import setup_logging


class SEOAssistantCLI:
    """Command Line Interface for SEO Assistant Pipeline"""
    
    def __init__(self):
        """Initialize CLI"""
        self.setup_logging()
        self.config_manager = ConfigurationManager()
        self.pipeline = None
        
    def setup_logging(self):
        """Setup logging for CLI"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def initialize_pipeline(self) -> bool:
        """Initialize the SEO pipeline"""
        try:
            config = self.config_manager.get_pipeline_config()
            
            if not config.gemini_api_key:
                self.logger.error("❌ GEMINI_API_KEY not found!")
                self.logger.error("   Set it as environment variable or in .env file")
                self.logger.error("   Get your key from: https://aistudio.google.com/app/apikey")
                return False
            
            self.pipeline = SEOAssistantPipeline(config)
            self.logger.info("✅ SEO Assistant Pipeline initialized successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize pipeline: {e}")
            return False
    
    def analyze_keyword(self, keyword: str, goal: str = "") -> None:
        """Analyze a keyword and display insights"""
        if not self.pipeline:
            return
            
        try:
            self.logger.info(f"🔍 Analyzing keyword: '{keyword}'")
            
            # Get context
            context = self.pipeline.retrieve_context(keyword, goal)
            
            # Display analysis
            print("\n" + "="*60)
            print(f"🎯 KEYWORD ANALYSIS: {keyword}")
            print("="*60)
            
            print(f"\n📊 Search Intent: {context.search_intent}")
            
            print(f"\n🔗 Related Keywords ({len(context.related_keywords)}):")
            for i, kw in enumerate(context.related_keywords[:10], 1):
                print(f"  {i}. {kw}")
            
            print(f"\n💡 Content Opportunities ({len(context.content_opportunities)}):")
            for i, opp in enumerate(context.content_opportunities[:5], 1):
                print(f"  {i}. {opp}")
            
            print(f"\n❓ User Questions ({len(context.user_questions)}):")
            for i, q in enumerate(context.user_questions[:5], 1):
                print(f"  {i}. {q}")
            
            if context.wikipedia_data:
                print(f"\n📚 Wikipedia Sources ({len(context.wikipedia_data)}):")
                for i, data in enumerate(context.wikipedia_data[:3], 1):
                    print(f"  {i}. {data.title} (Relevance: {data.relevance_score:.2f})")
            
            print("\n✅ Analysis complete!")
            
        except Exception as e:
            self.logger.error(f"❌ Analysis failed: {e}")
    
    def generate_brief(self, keyword: str, goal: str = "", output_file: Optional[str] = None) -> None:
        """Generate content brief for a keyword"""
        if not self.pipeline:
            return
            
        try:
            self.logger.info(f"📝 Generating content brief for: '{keyword}'")
            
            # Generate brief
            brief = self.pipeline.generate_content_brief(keyword, goal)
            
            # Display brief
            print("\n" + "="*60)
            print(f"📝 CONTENT BRIEF: {keyword}")
            print("="*60)
            
            print(f"\n🏷️  Title: {brief.title}")
            print(f"📄 Meta Description: {brief.meta_description}")
            print(f"📊 Target Word Count: {brief.word_count_target}")
            print(f"🎯 Content Type: {brief.content_type}")
            
            print(f"\n📖 Content Outline:")
            for i, section in enumerate(brief.content_outline, 1):
                print(f"  {i}. {section}")
            
            print(f"\n🔍 SEO Keywords:")
            for i, kw in enumerate(brief.seo_keywords[:10], 1):
                print(f"  {i}. {kw}")
            
            print(f"\n📢 Call to Action: {brief.call_to_action}")
            
            # Save to file if requested
            if output_file:
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(brief.to_dict(), f, indent=2, ensure_ascii=False)
                
                print(f"\n💾 Brief saved to: {output_path}")
            
            print("\n✅ Content brief generated successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Brief generation failed: {e}")
    
    def generate_article(self, keyword: str, goal: str = "", output_file: Optional[str] = None) -> None:
        """Generate full article for a keyword"""
        if not self.pipeline:
            return
            
        try:
            self.logger.info(f"📚 Generating full article for: '{keyword}'")
            
            # Generate article
            article = self.pipeline.generate_full_article(keyword, goal)
            
            # Display article info
            print("\n" + "="*60)
            print(f"📚 FULL ARTICLE: {keyword}")
            print("="*60)
            
            print(f"\n🏷️  Title: {article.title}")
            print(f"📄 Meta Description: {article.meta_description}")
            print(f"📊 Total Words: {article.total_word_count}")
            
            print(f"\n📖 Article Structure:")
            for section in article.sections:
                print(f"  • {section.heading} ({section.word_count} words)")
            
            # Save to file if requested
            if output_file:
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(article.to_dict(), f, indent=2, ensure_ascii=False)
                
                print(f"\n💾 Article saved to: {output_path}")
            else:
                # Display first section as preview
                if article.sections:
                    print(f"\n📖 Preview (First Section):")
                    print(f"--- {article.sections[0].heading} ---")
                    preview = article.sections[0].content[:500]
                    print(f"{preview}...")
            
            print("\n✅ Full article generated successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Article generation failed: {e}")
    
    def bulk_process(self, keywords_file: str, goal: str = "", create_calendar: bool = False) -> None:
        """Process multiple keywords from file"""
        if not self.pipeline:
            return
            
        try:
            # Read keywords
            keywords_path = Path(keywords_file)
            if not keywords_path.exists():
                self.logger.error(f"❌ Keywords file not found: {keywords_file}")
                return
            
            with open(keywords_path, 'r', encoding='utf-8') as f:
                keywords = [line.strip() for line in f if line.strip()]
            
            if not keywords:
                self.logger.error("❌ No keywords found in file")
                return
            
            self.logger.info(f"📦 Processing {len(keywords)} keywords from {keywords_file}")
            
            # Process keywords
            results = self.pipeline.bulk_process_keywords(keywords, goal)
            
            # Display results
            print("\n" + "="*60)
            print(f"📦 BULK PROCESSING RESULTS")
            print("="*60)
            
            successful = sum(1 for r in results if r["status"] == "success")
            failed = len(results) - successful
            
            print(f"\n📊 Summary:")
            print(f"  ✅ Successful: {successful}")
            print(f"  ❌ Failed: {failed}")
            print(f"  📈 Success Rate: {successful/len(results)*100:.1f}%")
            
            print(f"\n📝 Generated Content Briefs:")
            for i, result in enumerate(results, 1):
                if result["status"] == "success":
                    print(f"  {i}. {result['keyword']} → {result['title']}")
                else:
                    print(f"  {i}. {result['keyword']} → ❌ {result['error']}")
            
            # Save results
            output_file = keywords_path.stem + "_results.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Results saved to: {output_file}")
            
            # Create content calendar if requested
            if create_calendar:
                self.create_calendar(keywords, goal)
            
            print("\n✅ Bulk processing completed!")
            
        except Exception as e:
            self.logger.error(f"❌ Bulk processing failed: {e}")
    
    def create_calendar(self, keywords: List[str], goal: str = "", weeks: int = 4) -> None:
        """Create content calendar"""
        if not self.pipeline:
            return
            
        try:
            self.logger.info(f"📅 Creating content calendar for {len(keywords)} keywords")
            
            # Generate calendar
            calendar = self.pipeline.plan_content_calendar(keywords, weeks)
            
            # Display calendar
            print("\n" + "="*60)
            print(f"📅 CONTENT CALENDAR ({weeks} weeks)")
            print("="*60)
            
            for week in range(1, weeks + 1):
                week_items = [item for item in calendar.items if item.target_week == week]
                
                if week_items:
                    print(f"\n📅 Week {week} ({len(week_items)} items):")
                    for item in week_items:
                        print(f"  • {item.title} ({item.content_type})")
                        print(f"    Keyword: {item.keyword}")
                        print(f"    Priority: {item.priority_score:.1f} | Difficulty: {item.estimated_difficulty}")
                        print()
            
            # Save calendar
            calendar_file = f"content_calendar_{weeks}weeks.json"
            with open(calendar_file, 'w', encoding='utf-8') as f:
                json.dump(calendar.to_dict(), f, indent=2, ensure_ascii=False)
            
            print(f"💾 Calendar saved to: {calendar_file}")
            print("\n✅ Content calendar created successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Calendar creation failed: {e}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Smart SEO Assistant - AI-powered content planning and generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m smart_seo_assistant_ace.cli analyze "machine learning"
  python -m smart_seo_assistant_ace.cli brief "python tutorial" --goal="beginner-friendly"
  python -m smart_seo_assistant_ace.cli article "data science" --output="article.json"
  python -m smart_seo_assistant_ace.cli bulk keywords.txt --calendar --weeks=8
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a keyword')
    analyze_parser.add_argument('keyword', help='Keyword to analyze')
    analyze_parser.add_argument('--goal', default='', help='User goal or context')
    
    # Brief command
    brief_parser = subparsers.add_parser('brief', help='Generate content brief')
    brief_parser.add_argument('keyword', help='Keyword for content brief')
    brief_parser.add_argument('--goal', default='', help='User goal or context')
    brief_parser.add_argument('--output', help='Output file path (JSON)')
    
    # Article command
    article_parser = subparsers.add_parser('article', help='Generate full article')
    article_parser.add_argument('keyword', help='Keyword for article')
    article_parser.add_argument('--goal', default='', help='User goal or context')
    article_parser.add_argument('--output', help='Output file path (JSON)')
    
    # Bulk command
    bulk_parser = subparsers.add_parser('bulk', help='Process multiple keywords')
    bulk_parser.add_argument('keywords_file', help='File containing keywords (one per line)')
    bulk_parser.add_argument('--goal', default='', help='User goal or context')
    bulk_parser.add_argument('--calendar', action='store_true', help='Create content calendar')
    bulk_parser.add_argument('--weeks', type=int, default=4, help='Calendar timeframe in weeks')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize CLI
    cli = SEOAssistantCLI()
    
    if not cli.initialize_pipeline():
        sys.exit(1)
    
    # Execute command
    try:
        if args.command == 'analyze':
            cli.analyze_keyword(args.keyword, args.goal)
        
        elif args.command == 'brief':
            cli.generate_brief(args.keyword, args.goal, args.output)
        
        elif args.command == 'article':
            cli.generate_article(args.keyword, args.goal, args.output)
        
        elif args.command == 'bulk':
            cli.bulk_process(args.keywords_file, args.goal, args.calendar)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
