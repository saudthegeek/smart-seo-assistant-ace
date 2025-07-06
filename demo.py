#!/usr/bin/env python3
"""
Demo script to test the Smart SEO Assistant Full Stack Application
"""

import time
import requests
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

def check_backend_health():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_keyword_analysis():
    """Test keyword analysis endpoint"""
    console.print("\n🔍 Testing Keyword Analysis...", style="bold blue")
    
    data = {
        "keyword": "machine learning tutorials",
        "goal": "Educational content for beginners"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/seo/analyze", json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            
            # Display results in a nice table
            table = Table(title="Keyword Analysis Results")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Keyword", result.get("keyword", "N/A"))
            table.add_row("Search Intent", result.get("search_intent", "N/A"))
            table.add_row("Related Keywords", str(len(result.get("related_keywords", []))))
            table.add_row("Content Opportunities", str(len(result.get("content_opportunities", []))))
            table.add_row("User Questions", str(len(result.get("user_questions", []))))
            table.add_row("Wikipedia Sources", str(len(result.get("wikipedia_sources", []))))
            
            console.print(table)
            return True
        else:
            console.print(f"❌ Analysis failed with status: {response.status_code}", style="red")
            return False
    except Exception as e:
        console.print(f"❌ Analysis error: {e}", style="red")
        return False

def test_content_brief():
    """Test content brief generation"""
    console.print("\n📝 Testing Content Brief Generation...", style="bold green")
    
    data = {
        "keyword": "python web development",
        "goal": "Comprehensive tutorial series"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/seo/brief", json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            
            console.print(Panel(
                f"[bold]Title:[/bold] {result.get('title', 'N/A')}\n\n"
                f"[bold]Meta Description:[/bold] {result.get('meta_description', 'N/A')}\n\n"
                f"[bold]Content Type:[/bold] {result.get('content_type', 'N/A')}\n"
                f"[bold]Word Count Target:[/bold] {result.get('word_count_target', 'N/A')} words\n\n"
                f"[bold]Outline:[/bold]\n" + "\n".join([f"• {item}" for item in result.get('outline', [])[:5]]),
                title="Content Brief",
                border_style="green"
            ))
            return True
        else:
            console.print(f"❌ Brief generation failed with status: {response.status_code}", style="red")
            return False
    except Exception as e:
        console.print(f"❌ Brief generation error: {e}", style="red")
        return False

def test_bulk_processing():
    """Test bulk keyword processing"""
    console.print("\n📊 Testing Bulk Processing...", style="bold orange3")
    
    data = {
        "keywords": ["AI basics", "machine learning", "deep learning"],
        "goal": "Educational content series"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/seo/bulk", json=data, timeout=45)
        if response.status_code == 200:
            result = response.json()
            summary = result.get("summary", {})
            
            table = Table(title="Bulk Processing Results")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="yellow")
            
            table.add_row("Total Keywords", str(summary.get("total_keywords", 0)))
            table.add_row("Successful", str(summary.get("successful", 0)))
            table.add_row("Failed", str(summary.get("failed", 0)))
            table.add_row("Success Rate", f"{summary.get('success_rate', 0):.1f}%")
            
            console.print(table)
            return True
        else:
            console.print(f"❌ Bulk processing failed with status: {response.status_code}", style="red")
            return False
    except Exception as e:
        console.print(f"❌ Bulk processing error: {e}", style="red")
        return False

def test_content_calendar():
    """Test content calendar creation"""
    console.print("\n📅 Testing Content Calendar...", style="bold purple")
    
    data = {
        "keywords": ["python basics", "web development", "database design", "API development"],
        "goal": "Comprehensive web development course",
        "timeframe_weeks": 4
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/seo/calendar", json=data, timeout=45)
        if response.status_code == 200:
            result = response.json()
            
            console.print(Panel(
                f"[bold]Calendar Overview:[/bold]\n"
                f"• Total Keywords: {result.get('total_keywords', 0)}\n"
                f"• Timeframe: {result.get('timeframe_weeks', 0)} weeks\n"
                f"• Content Items: {len(result.get('items', []))}\n\n"
                f"[bold]Sample Items:[/bold]\n" + 
                "\n".join([f"Week {item.get('target_week', 0)}: {item.get('title', 'N/A')}" 
                          for item in result.get('items', [])[:3]]),
                title="Content Calendar",
                border_style="purple"
            ))
            return True
        else:
            console.print(f"❌ Calendar creation failed with status: {response.status_code}", style="red")
            return False
    except Exception as e:
        console.print(f"❌ Calendar creation error: {e}", style="red")
        return False

def main():
    """Main demo function"""
    console.print(Panel(
        Text("🚀 Smart SEO Assistant Demo", justify="center", style="bold white"),
        title="Full Stack Application Test",
        border_style="blue"
    ))
    
    # Check backend health
    console.print("\n🏥 Checking Backend Health...", style="bold")
    if check_backend_health():
        console.print("✅ Backend is running and healthy!", style="green")
    else:
        console.print("❌ Backend is not running! Please start the backend first:", style="red")
        console.print("   cd backend && python start_server.py", style="yellow")
        return
    
    # Run tests
    tests = [
        ("Keyword Analysis", test_keyword_analysis),
        ("Content Brief", test_content_brief),
        ("Bulk Processing", test_bulk_processing),
        ("Content Calendar", test_content_calendar)
    ]
    
    results = []
    for test_name, test_func in tests:
        success = test_func()
        results.append((test_name, success))
        time.sleep(1)  # Small delay between tests
    
    # Summary
    console.print("\n" + "="*50, style="bold")
    console.print("📋 Test Summary:", style="bold cyan")
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        console.print(f"  {test_name}: {status}")
    
    console.print(f"\nOverall: {passed_tests}/{total_tests} tests passed", style="bold")
    
    if passed_tests == total_tests:
        console.print("\n🎉 All tests passed! The Smart SEO Assistant is working perfectly!", style="bold green")
        console.print(f"\n🌐 Frontend URL: {FRONTEND_URL}", style="blue")
        console.print(f"📚 API Docs: {BACKEND_URL}/docs", style="blue")
    else:
        console.print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Check the backend logs for details.", style="yellow")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n👋 Demo interrupted by user", style="yellow")
    except Exception as e:
        console.print(f"\n❌ Demo error: {e}", style="red")
