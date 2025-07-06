#!/usr/bin/env python3
"""
SEO Assistant Pipeline Test Suite
Comprehensive testing to verify all components work correctly

Run this script to test the entire pipeline:
    python test_pipeline.py
"""

import os
import sys
import traceback
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root / "src"))

def test_imports():
    """Test that all imports work correctly"""
    print("🧪 Testing imports...")
    
    try:
        # Test core imports
        from smart_seo_assistant_ace import (
            SEOAssistantPipeline, ConfigurationManager,
            SEOContext, ContentBrief, FullArticle
        )
        
        # Test component imports
        from smart_seo_assistant_ace.components.data_retrieval import DataRetriever
        from smart_seo_assistant_ace.components.content_generation import ContentGenerator
        
        # Test utility imports
        from smart_seo_assistant_ace.utils import setup_logging, clean_text
        
        print("✅ All imports successful")
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False


def test_configuration():
    """Test configuration loading"""
    print("\n🧪 Testing configuration...")
    
    try:
        from smart_seo_assistant_ace import ConfigurationManager
        
        # Test configuration manager
        config_manager = ConfigurationManager()
        
        # Check if API key is available
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠️  GOOGLE_API_KEY not found in environment")
            print("   This is expected if you haven't set up the API key yet")
            print("   Get your key from: https://aistudio.google.com/app/apikey")
            return False
        
        # Test getting pipeline config
        config = config_manager.get_pipeline_config()
        print(f"✅ Configuration loaded successfully")
        print(f"   Model: {config.gemini_model}")
        print(f"   Max retries: {config.max_retries}")
        print(f"   Timeout: {config.timeout}")
        print(f"   Cache enabled: {config.cache_enabled}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        traceback.print_exc()
        return False


def test_data_retrieval():
    """Test data retrieval component"""
    print("\n🧪 Testing data retrieval...")
    
    try:
        from smart_seo_assistant_ace.components.data_retrieval import DataRetriever
        
        # Initialize data retriever
        retriever = DataRetriever()
        
        # Test Wikipedia search
        print("   Testing Wikipedia search...")
        results = retriever.fetch_wikipedia_data("machine learning", limit=2)
        
        if results:
            print(f"✅ Wikipedia search successful ({len(results)} results)")
            for result in results[:2]:
                print(f"   - {result.title} (Score: {result.relevance_score:.2f})")
        else:
            print("⚠️  No Wikipedia results found")
        
        # Test keyword extraction
        print("   Testing keyword extraction...")
        keywords = retriever.extract_related_keywords("python programming", results)
        
        if keywords:
            print(f"✅ Keyword extraction successful ({len(keywords)} keywords)")
            print(f"   Sample keywords: {keywords[:5]}")
        else:
            print("⚠️  No keywords extracted")
        
        return True
        
    except Exception as e:
        print(f"❌ Data retrieval test failed: {e}")
        traceback.print_exc()
        return False


def test_content_generation():
    """Test content generation component"""
    print("\n🧪 Testing content generation...")
    
    try:
        # Check API key first
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠️  GOOGLE_API_KEY not found - skipping content generation test")
            return False
        
        from smart_seo_assistant_ace.components.content_generation import ContentGenerator
        from smart_seo_assistant_ace.entity import SEOContext
        
        # Initialize content generator
        generator = ContentGenerator(api_key)
        
        # Create a simple test context
        test_context = SEOContext(
            keyword="python tutorial",
            search_intent="informational",
            related_keywords=["python programming", "python basics", "learn python"],
            content_opportunities=["beginner guide", "step by step tutorial"],
            user_questions=["how to learn python", "python tutorial for beginners"],
            wikipedia_data=[]
        )
        
        print("   Testing content brief generation...")
        brief = generator.generate_content_brief(test_context)
        
        if brief and brief.title:
            print(f"✅ Content brief generated successfully")
            print(f"   Title: {brief.title[:80]}...")
            print(f"   Word count target: {brief.word_count_target}")
            print(f"   Sections: {len(brief.outline)}")
        else:
            print("❌ Content brief generation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Content generation test failed: {e}")
        traceback.print_exc()
        return False


def test_full_pipeline():
    """Test the complete pipeline"""
    print("\n🧪 Testing full pipeline...")
    
    try:
        # Check API key first
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠️  GOOGLE_API_KEY not found - skipping full pipeline test")
            return False
        
        from smart_seo_assistant_ace import SEOAssistantPipeline, ConfigurationManager
        
        # Initialize pipeline
        config_manager = ConfigurationManager()
        config = config_manager.get_pipeline_config()
        pipeline = SEOAssistantPipeline(config)
        
        print("   Testing keyword analysis...")
        test_keyword = "machine learning basics"
        
        # Test context retrieval
        context = pipeline.retrieve_context(test_keyword)
        
        print(f"✅ Context retrieved for '{test_keyword}'")
        print(f"   Search intent: {context.search_intent}")
        print(f"   Related keywords: {len(context.related_keywords)}")
        print(f"   Content opportunities: {len(context.content_opportunities)}")
        
        # Test content brief generation
        print("   Testing content brief generation...")
        brief = pipeline.generate_content_brief(test_keyword)
        
        if brief and brief.title:
            print(f"✅ Content brief generated successfully")
            print(f"   Title: {brief.title[:80]}...")
            print(f"   Content type: {brief.content_type}")
            print(f"   Outline sections: {len(brief.outline)}")
        else:
            print("❌ Content brief generation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Full pipeline test failed: {e}")
        traceback.print_exc()
        return False


def test_cli_availability():
    """Test CLI module availability"""
    print("\n🧪 Testing CLI availability...")
    
    try:
        from smart_seo_assistant_ace.cli import SEOAssistantCLI
        
        # Try to initialize CLI (without API key dependency)
        cli = SEOAssistantCLI()
        
        print("✅ CLI module available")
        print("   Use: python -m smart_seo_assistant_ace.cli --help")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        traceback.print_exc()
        return False


def test_api_availability():
    """Test API module availability"""
    print("\n🧪 Testing API availability...")
    
    try:
        from smart_seo_assistant_ace.api import app
        
        print("✅ API module available")
        print("   Use: uvicorn smart_seo_assistant_ace.api:app --reload")
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 Smart SEO Assistant Pipeline Test Suite")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Data Retrieval", test_data_retrieval),
        ("Content Generation", test_content_generation),
        ("Full Pipeline", test_full_pipeline),
        ("CLI Availability", test_cli_availability),
        ("API Availability", test_api_availability),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Pipeline is ready to use.")
        print("\nQuick start commands:")
        print("   python -m smart_seo_assistant_ace.cli analyze 'your keyword'")
        print("   python examples/basic_usage.py")
        print("   uvicorn smart_seo_assistant_ace.api:app --reload")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above for details.")
        
        if not os.getenv("GOOGLE_API_KEY"):
            print("\n💡 Missing API Key:")
            print("   Many tests require GOOGLE_API_KEY environment variable")
            print("   Get your key from: https://aistudio.google.com/app/apikey")
            print("   Set it with: export GOOGLE_API_KEY=your_key_here")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
