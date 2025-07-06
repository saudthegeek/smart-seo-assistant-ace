"""
Advanced Usage Example: Bulk Processing and Content Calendar
This example demonstrates bulk keyword processing and content calendar creation
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

from smart_seo_assistant_ace.config.configuration import ConfigurationManager
from smart_seo_assistant_ace.pipeline.seo_pipeline import SEOAssistantPipeline


def main():
    """Demonstrate advanced SEO Assistant Pipeline features"""
    
    print("🚀 Smart SEO Assistant - Advanced Usage Example")
    print("=" * 55)
    
    # Initialize pipeline
    print("\n📋 Initializing SEO Assistant Pipeline...")
    config_manager = ConfigurationManager()
    config = config_manager.get_pipeline_config()
    
    if not config.gemini_api_key:
        print("❌ ERROR: GEMINI_API_KEY not found!")
        return
    
    pipeline = SEOAssistantPipeline(config)
    print("✅ Pipeline initialized successfully!")
    
    # Example keywords for a tech blog
    tech_keywords = [
        "python programming tutorial",
        "machine learning basics",
        "web development guide",
        "data science introduction",
        "artificial intelligence explained",
        "javascript fundamentals",
        "cloud computing overview",
        "cybersecurity best practices"
    ]
    
    user_goal = "Educational tech blog for beginners"
    
    print(f"\n📦 Step 1: Bulk Processing {len(tech_keywords)} Keywords")
    print(f"Goal: {user_goal}")
    print("\nKeywords to process:")
    for i, kw in enumerate(tech_keywords, 1):
        print(f"   {i}. {kw}")
    
    # Bulk process keywords
    print("\n⚡ Processing keywords in bulk...")
    results = pipeline.bulk_process_keywords(tech_keywords, user_goal)
    
    # Analyze results
    successful = sum(1 for r in results if r["status"] == "success")
    failed = len(results) - successful
    
    print(f"\n📊 Bulk Processing Results:")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Success Rate: {successful/len(results)*100:.1f}%")
    
    # Display successful results
    print(f"\n📝 Generated Content Briefs:")
    for i, result in enumerate(results, 1):
        if result["status"] == "success":
            print(f"   {i}. {result['keyword']}")
            print(f"      → {result['title']}")
            print(f"      → Target: {result['word_count_target']} words")
        else:
            print(f"   {i}. {result['keyword']} → ❌ {result['error']}")
    
    # Save bulk results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"bulk_results_{timestamp}.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": timestamp,
            "goal": user_goal,
            "keywords": tech_keywords,
            "results": results,
            "summary": {
                "total": len(results),
                "successful": successful,
                "failed": failed,
                "success_rate": successful/len(results)*100
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    # Create content calendar
    print(f"\n📅 Step 2: Creating Content Calendar")
    successful_keywords = [r["keyword"] for r in results if r["status"] == "success"]
    
    if successful_keywords:
        print(f"Planning content for {len(successful_keywords)} successful keywords...")
        
        calendar = pipeline.plan_content_calendar(successful_keywords, timeframe_weeks=8)
        
        print(f"\n📅 Content Calendar (8 weeks):")
        print(f"   Total Items: {len(calendar.items)}")
        
        # Display calendar by week
        for week in range(1, 9):
            week_items = [item for item in calendar.items if item.target_week == week]
            
            if week_items:
                print(f"\n   📅 Week {week} ({len(week_items)} items):")
                for item in week_items:
                    print(f"      • {item.title}")
                    print(f"        Type: {item.content_type} | Priority: {item.priority_score:.1f}")
                    print(f"        Keyword: {item.keyword}")
                    print(f"        Difficulty: {item.estimated_difficulty}")
        
        # Save calendar
        calendar_file = f"content_calendar_{timestamp}.json"
        with open(calendar_file, 'w', encoding='utf-8') as f:
            json.dump(calendar.to_dict(), f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Calendar saved to: {calendar_file}")
    
    # Demonstrate individual article generation
    print(f"\n📚 Step 3: Generating Sample Full Article")
    if successful_keywords:
        sample_keyword = successful_keywords[0]
        print(f"Generating full article for: '{sample_keyword}'")
        
        try:
            article = pipeline.generate_full_article(sample_keyword, user_goal)
            
            print(f"\n✅ Full Article Generated:")
            print(f"   Title: {article.title}")
            print(f"   Total Words: {article.total_word_count}")
            print(f"   Sections: {len(article.sections)}")
            
            print(f"\n📖 Article Structure:")
            for i, section in enumerate(article.sections, 1):
                print(f"   {i}. {section.heading} ({section.word_count} words)")
            
            # Save article
            article_file = f"article_{sample_keyword.replace(' ', '_')}_{timestamp}.json"
            with open(article_file, 'w', encoding='utf-8') as f:
                json.dump(article.to_dict(), f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Article saved to: {article_file}")
            
        except Exception as e:
            print(f"❌ Article generation failed: {e}")
    
    # Show pipeline performance
    print(f"\n📈 Step 4: Pipeline Performance Statistics")
    stats = pipeline.get_pipeline_stats()
    performance_report = pipeline.get_performance_report()
    
    print(f"\n📊 Pipeline Stats:")
    for key, value in stats.items():
        if key != "config":
            print(f"   {key}: {value}")
    
    print(f"\n📈 Performance Report:")
    if performance_report.get("message"):
        print(f"   {performance_report['message']}")
    else:
        summary = performance_report.get("summary", {})
        for key, value in summary.items():
            print(f"   {key}: {value}")
    
    print(f"\n🎉 Advanced example completed successfully!")
    print(f"\nGenerated files:")
    print(f"   • {results_file} - Bulk processing results")
    if successful_keywords:
        print(f"   • {calendar_file} - Content calendar")
        if 'article_file' in locals():
            print(f"   • {article_file} - Sample full article")
    
    print(f"\nNext steps:")
    print(f"   • Use the CLI for interactive processing")
    print(f"   • Start the web API with: uvicorn smart_seo_assistant_ace.api:app --reload")
    print(f"   • Integrate with your content management workflow")


if __name__ == "__main__":
    main()
