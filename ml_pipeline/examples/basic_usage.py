"""
Basic Usage Example: Quick Start with SEO Assistant Pipeline
This example shows how to get started with the SEO Assistant Pipeline for keyword analysis and content generation
"""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

from smart_seo_assistant_ace.config.configuration import ConfigurationManager
from smart_seo_assistant_ace.pipeline.seo_pipeline import SEOAssistantPipeline


def main():
    """Demonstrate basic SEO Assistant Pipeline usage"""
    
    print("🚀 Smart SEO Assistant - Basic Usage Example")
    print("=" * 50)
    
    # Initialize configuration
    print("\n📋 Step 1: Initializing configuration...")
    config_manager = ConfigurationManager()
    config = config_manager.get_pipeline_config()
    
    if not config.gemini_api_key:
        print("❌ ERROR: GEMINI_API_KEY not found!")
        print("   Please set it as an environment variable or in .env file")
        print("   Get your key from: https://aistudio.google.com/app/apikey")
        return
    
    print(f"✅ Configuration loaded successfully")
    print(f"   Model: {config.gemini_model}")
    print(f"   Cache enabled: {config.cache_enabled}")
    
    # Initialize pipeline
    print("\n🔧 Step 2: Initializing SEO pipeline...")
    pipeline = SEOAssistantPipeline(config)
    print("✅ Pipeline initialized successfully!")
    
    # Example keyword for demonstration
    keyword = "machine learning for beginners"
    user_goal = "Create beginner-friendly educational content"
    
    print(f"\n🎯 Step 3: Analyzing keyword: '{keyword}'")
    print(f"   Goal: {user_goal}")
    
    # Analyze keyword (Advanced Retrieval)
    print("\n🔍 Phase A: Advanced Retrieval...")
    context = pipeline.retrieve_context(keyword, user_goal)
    
    print(f"✅ Context retrieved:")
    print(f"   Search Intent: {context.search_intent}")
    print(f"   Related Keywords: {len(context.related_keywords)}")
    print(f"   Content Opportunities: {len(context.content_opportunities)}")
    print(f"   User Questions: {len(context.user_questions)}")
    print(f"   Wikipedia Sources: {len(context.wikipedia_data)}")
    
    # Generate content brief (Context Design + Execution)
    print("\n📝 Step 4: Generating content brief...")
    content_brief = pipeline.generate_content_brief(keyword, user_goal)
    
    print(f"✅ Content brief generated:")
    print(f"   Title: {content_brief.title}")
    print(f"   Content Type: {content_brief.content_type}")
    print(f"   Target Word Count: {content_brief.word_count_target}")
    print(f"   SEO Keywords: {len(content_brief.outline)}")
    print(f"   Content Sections: {len(content_brief.outline)}")
    
    # Display sample insights
    print("\n📊 Sample Insights:")
    print("\n🔗 Top Related Keywords:")
    for i, kw in enumerate(context.related_keywords[:5], 1):
        print(f"   {i}. {kw}")
    
    print("\n💡 Content Opportunities:")
    for i, opp in enumerate(context.content_opportunities[:3], 1):
        print(f"   {i}. {opp}")
    
    print("\n❓ User Questions:")
    for i, q in enumerate(context.user_questions[:3], 1):
        print(f"   {i}. {q}")
    
    print("\n📖 Content Outline:")
    for i, section in enumerate(content_brief.outline[:5], 1):
        print(f"   {i}. {section}")
    
    # Show pipeline stats
    print(f"\n📈 Pipeline Statistics:")
    stats = pipeline.get_pipeline_stats()
    for key, value in stats.items():
        if key != "config":  # Skip config details for brevity
            print(f"   {key}: {value}")
    
    print("\n🎉 Basic example completed successfully!")
    print("\nNext steps:")
    print("   • Try bulk processing with multiple keywords")
    print("   • Generate full articles with pipeline.generate_full_article()")
    print("   • Create content calendars with pipeline.plan_content_calendar()")
    print("   • Use the CLI: python -m smart_seo_assistant_ace.cli --help")


if __name__ == "__main__":
    main()
