"""
Notebook Integration Example
Demonstrates how to integrate the SEO Assistant Pipeline with Jupyter notebooks
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root / "src"))

import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

from smart_seo_assistant_ace.config.configuration import ConfigurationManager
from smart_seo_assistant_ace.pipeline.seo_pipeline import SEOAssistantPipeline


class NotebookSEOAssistant:
    """
    Jupyter Notebook-friendly wrapper for SEO Assistant Pipeline
    Provides enhanced visualization and interactive features
    """
    
    def __init__(self):
        """Initialize the notebook SEO assistant"""
        self.config_manager = ConfigurationManager()
        self.config = self.config_manager.get_pipeline_config()
        
        if not self.config.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found! Please set it as environment variable.")
        
        self.pipeline = SEOAssistantPipeline(self.config)
        self.results_history = []
        
        print("🚀 Notebook SEO Assistant initialized successfully!")
    
    def analyze_keyword_interactive(self, keyword: str, goal: str = "", show_plots: bool = True):
        """
        Interactive keyword analysis with visualizations
        """
        print(f"🔍 Analyzing keyword: '{keyword}'")
        
        # Get context
        context = self.pipeline.retrieve_context(keyword, goal)
        
        # Create analysis data
        analysis_data = {
            "keyword": keyword,
            "search_intent": context.search_intent,
            "related_keywords_count": len(context.related_keywords),
            "content_opportunities_count": len(context.content_opportunities),
            "user_questions_count": len(context.user_questions),
            "wikipedia_sources_count": len(context.wikipedia_data),
            "timestamp": datetime.now().isoformat()
        }
        
        # Store in history
        self.results_history.append(analysis_data)
        
        # Display results
        self._display_keyword_analysis(context)
        
        # Show visualizations
        if show_plots:
            self._plot_keyword_metrics(analysis_data)
        
        return context
    
    def generate_brief_interactive(self, keyword: str, goal: str = "", show_details: bool = True):
        """
        Interactive content brief generation
        """
        print(f"📝 Generating content brief for: '{keyword}'")
        
        # Generate brief
        brief = self.pipeline.generate_content_brief(keyword, goal)
        
        # Display results
        if show_details:
            self._display_content_brief(brief)
        
        return brief
    
    def bulk_analyze_with_visualization(self, keywords: list, goal: str = ""):
        """
        Bulk analyze keywords with comprehensive visualizations
        """
        print(f"📦 Bulk analyzing {len(keywords)} keywords...")
        
        results = []
        
        for keyword in keywords:
            try:
                context = self.pipeline.retrieve_context(keyword, goal)
                
                result = {
                    "keyword": keyword,
                    "search_intent": context.search_intent,
                    "related_keywords": len(context.related_keywords),
                    "content_opportunities": len(context.content_opportunities),
                    "user_questions": len(context.user_questions),
                    "wikipedia_sources": len(context.wikipedia_data),
                    "status": "success"
                }
                
            except Exception as e:
                result = {
                    "keyword": keyword,
                    "status": "failed",
                    "error": str(e)
                }
            
            results.append(result)
        
        # Create DataFrame for analysis
        df = pd.DataFrame(results)
        
        # Display summary
        successful = df[df['status'] == 'success']
        print(f"\n📊 Analysis Summary:")
        print(f"   ✅ Successful: {len(successful)}")
        print(f"   ❌ Failed: {len(df) - len(successful)}")
        
        if len(successful) > 0:
            # Create visualizations
            self._create_bulk_visualizations(successful)
        
        return df
    
    def create_content_calendar_interactive(self, keywords: list, weeks: int = 4, goal: str = ""):
        """
        Create interactive content calendar with visualizations
        """
        print(f"📅 Creating content calendar for {len(keywords)} keywords over {weeks} weeks...")
        
        # Generate calendar
        calendar = self.pipeline.plan_content_calendar(keywords, weeks)
        
        # Convert to DataFrame for analysis
        calendar_data = []
        for item in calendar.items:
            calendar_data.append({
                "keyword": item.keyword,
                "title": item.title,
                "content_type": item.content_type,
                "priority_score": item.priority_score,
                "target_week": item.target_week,
                "estimated_difficulty": item.estimated_difficulty
            })
        
        df = pd.DataFrame(calendar_data)
        
        # Display calendar
        self._display_calendar_summary(df, weeks)
        
        # Create visualizations
        self._create_calendar_visualizations(df)
        
        return calendar, df
    
    def _display_keyword_analysis(self, context):
        """Display keyword analysis results"""
        print(f"\n🎯 KEYWORD ANALYSIS: {context.keyword}")
        print("=" * 60)
        
        print(f"\n📊 Search Intent: {context.search_intent}")
        
        print(f"\n🔗 Related Keywords ({len(context.related_keywords)}):")
        for i, kw in enumerate(context.related_keywords[:10], 1):
            print(f"   {i}. {kw}")
        
        print(f"\n💡 Content Opportunities ({len(context.content_opportunities)}):")
        for i, opp in enumerate(context.content_opportunities[:5], 1):
            print(f"   {i}. {opp}")
        
        print(f"\n❓ User Questions ({len(context.user_questions)}):")
        for i, q in enumerate(context.user_questions[:5], 1):
            print(f"   {i}. {q}")
    
    def _display_content_brief(self, brief):
        """Display content brief results"""
        print(f"\n📝 CONTENT BRIEF")
        print("=" * 60)
        
        print(f"\n🏷️  Title: {brief.title}")
        print(f"📄 Meta Description: {brief.meta_description}")
        print(f"📊 Target Word Count: {brief.word_count_target}")
        print(f"🎯 Content Type: {brief.content_type}")
        
        print(f"\n📖 Content Outline:")
        for i, section in enumerate(brief.content_outline[:8], 1):
            print(f"   {i}. {section}")
        
        print(f"\n🔍 SEO Keywords:")
        for i, kw in enumerate(brief.seo_keywords[:10], 1):
            print(f"   {i}. {kw}")
    
    def _plot_keyword_metrics(self, analysis_data):
        """Create visualizations for keyword metrics"""
        plt.figure(figsize=(12, 8))
        
        # Create subplot for metrics
        plt.subplot(2, 2, 1)
        metrics = [
            analysis_data['related_keywords_count'],
            analysis_data['content_opportunities_count'],
            analysis_data['user_questions_count'],
            analysis_data['wikipedia_sources_count']
        ]
        labels = ['Related\nKeywords', 'Content\nOpportunities', 'User\nQuestions', 'Wikipedia\nSources']
        
        plt.bar(labels, metrics, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
        plt.title(f"Keyword Metrics: {analysis_data['keyword']}")
        plt.ylabel('Count')
        
        # Search intent pie chart
        plt.subplot(2, 2, 2)
        intent_colors = {
            'informational': '#4ECDC4',
            'transactional': '#FF6B6B',
            'commercial': '#FFA07A',
            'navigational': '#45B7D1'
        }
        intent = analysis_data['search_intent'].lower()
        plt.pie([1], labels=[intent.title()], colors=[intent_colors.get(intent, '#gray')], autopct='100%')
        plt.title('Search Intent')
        
        plt.tight_layout()
        plt.show()
    
    def _create_bulk_visualizations(self, df):
        """Create visualizations for bulk analysis"""
        plt.figure(figsize=(15, 10))
        
        # Search intent distribution
        plt.subplot(2, 3, 1)
        intent_counts = df['search_intent'].value_counts()
        plt.pie(intent_counts.values, labels=intent_counts.index, autopct='%1.1f%%')
        plt.title('Search Intent Distribution')
        
        # Metrics comparison
        plt.subplot(2, 3, 2)
        metrics_cols = ['related_keywords', 'content_opportunities', 'user_questions', 'wikipedia_sources']
        df[metrics_cols].mean().plot(kind='bar')
        plt.title('Average Metrics per Keyword')
        plt.xticks(rotation=45)
        
        # Top keywords by total metrics
        plt.subplot(2, 3, 3)
        df['total_metrics'] = df[metrics_cols].sum(axis=1)
        top_keywords = df.nlargest(5, 'total_metrics')
        plt.barh(top_keywords['keyword'], top_keywords['total_metrics'])
        plt.title('Top Keywords by Total Metrics')
        
        # Correlation heatmap
        plt.subplot(2, 3, 4)
        correlation = df[metrics_cols].corr()
        sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
        plt.title('Metrics Correlation')
        
        # Metrics distribution
        plt.subplot(2, 3, 5)
        df['related_keywords'].hist(alpha=0.7, label='Related Keywords')
        df['content_opportunities'].hist(alpha=0.7, label='Content Opportunities')
        plt.legend()
        plt.title('Metrics Distribution')
        
        plt.tight_layout()
        plt.show()
    
    def _display_calendar_summary(self, df, weeks):
        """Display calendar summary"""
        print(f"\n📅 CONTENT CALENDAR SUMMARY ({weeks} weeks)")
        print("=" * 60)
        
        for week in range(1, weeks + 1):
            week_items = df[df['target_week'] == week]
            
            if len(week_items) > 0:
                print(f"\n📅 Week {week} ({len(week_items)} items):")
                for _, item in week_items.iterrows():
                    print(f"   • {item['title']}")
                    print(f"     Type: {item['content_type']} | Priority: {item['priority_score']:.1f}")
    
    def _create_calendar_visualizations(self, df):
        """Create visualizations for content calendar"""
        plt.figure(figsize=(15, 10))
        
        # Content distribution by week
        plt.subplot(2, 3, 1)
        week_counts = df['target_week'].value_counts().sort_index()
        plt.bar(week_counts.index, week_counts.values)
        plt.title('Content Distribution by Week')
        plt.xlabel('Week')
        plt.ylabel('Number of Items')
        
        # Content type distribution
        plt.subplot(2, 3, 2)
        content_type_counts = df['content_type'].value_counts()
        plt.pie(content_type_counts.values, labels=content_type_counts.index, autopct='%1.1f%%')
        plt.title('Content Type Distribution')
        
        # Priority score distribution
        plt.subplot(2, 3, 3)
        plt.hist(df['priority_score'], bins=10, alpha=0.7)
        plt.title('Priority Score Distribution')
        plt.xlabel('Priority Score')
        plt.ylabel('Frequency')
        
        # Difficulty distribution
        plt.subplot(2, 3, 4)
        difficulty_counts = df['estimated_difficulty'].value_counts()
        plt.bar(difficulty_counts.index, difficulty_counts.values)
        plt.title('Estimated Difficulty Distribution')
        
        # Priority vs Week
        plt.subplot(2, 3, 5)
        plt.scatter(df['target_week'], df['priority_score'], alpha=0.7)
        plt.title('Priority Score vs Target Week')
        plt.xlabel('Target Week')
        plt.ylabel('Priority Score')
        
        plt.tight_layout()
        plt.show()
    
    def export_results(self, filename: str = None):
        """Export analysis results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"seo_analysis_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results_history, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results exported to: {filename}")
        return filename
    
    def get_insights_summary(self):
        """Get summary insights from analysis history"""
        if not self.results_history:
            print("No analysis history available")
            return
        
        df = pd.DataFrame(self.results_history)
        
        print("📈 INSIGHTS SUMMARY")
        print("=" * 40)
        print(f"Total keywords analyzed: {len(df)}")
        print(f"Average related keywords: {df['related_keywords_count'].mean():.1f}")
        print(f"Average content opportunities: {df['content_opportunities_count'].mean():.1f}")
        print(f"Average user questions: {df['user_questions_count'].mean():.1f}")
        
        # Most common search intents
        print(f"\nMost common search intents:")
        intent_counts = df['search_intent'].value_counts()
        for intent, count in intent_counts.head(3).items():
            print(f"   {intent}: {count}")
        
        return df


# Example usage function for notebooks
def notebook_example():
    """
    Example function demonstrating notebook usage
    Run this in a Jupyter notebook cell
    """
    # Initialize assistant
    assistant = NotebookSEOAssistant()
    
    # Analyze a single keyword
    context = assistant.analyze_keyword_interactive("python machine learning tutorial", "educational content")
    
    # Generate content brief
    brief = assistant.generate_brief_interactive("python machine learning tutorial", "educational content")
    
    # Bulk analysis with visualization
    keywords = [
        "python tutorial",
        "machine learning basics",
        "data science guide",
        "web development introduction"
    ]
    
    df = assistant.bulk_analyze_with_visualization(keywords)
    
    # Create content calendar
    calendar, calendar_df = assistant.create_content_calendar_interactive(keywords, weeks=4)
    
    # Export results
    assistant.export_results()
    
    # Get insights
    assistant.get_insights_summary()
    
    return assistant


if __name__ == "__main__":
    print("🚀 SEO Assistant Notebook Integration Example")
    print("=" * 50)
    print("This script demonstrates notebook integration features.")
    print("For full interactive experience, run in Jupyter notebook:")
    print("   assistant = notebook_example()")
