# Smart SEO Assistant ACE Pipeline

A comprehensive AI-powered SEO content generation pipeline that implements the **ACE methodology**: **A**dvanced Retrieval → **C**ontext Design → **E**xecution.

## 🌟 Features

- **🔍 Advanced Keyword Analysis**: Extract related keywords, analyze search intent, and identify content opportunities
- **📝 Content Brief Generation**: Create detailed SEO-optimized content briefs with titles, outlines, and meta descriptions
- **📚 Full Article Generation**: Generate complete, structured articles with proper SEO optimization
- **📦 Bulk Processing**: Handle multiple keywords efficiently with batch processing
- **📅 Content Calendar Planning**: Create prioritized content calendars with intelligent scheduling
- **🖥️ Multiple Interfaces**: CLI, Web API, and Jupyter notebook integration
- **📊 Performance Tracking**: Monitor and analyze content performance metrics
- **🎯 Human-Friendly**: Clean, readable code with comprehensive documentation

## 🏗️ Architecture

The pipeline implements the **ACE methodology**:

### 🔍 A: Advanced Retrieval
- Wikipedia data extraction and relevance scoring
- Related keyword discovery using NLP techniques
- Content opportunity identification
- User question extraction and analysis

### 🧠 C: Context Design
- Context quality scoring and optimization
- Data structure optimization for AI processing
- Semantic clustering and prioritization
- Processing hint generation

### ⚡ E: Execution
- AI-powered content generation using Gemini
- SEO optimization and keyword integration
- Structured content creation with proper formatting
- Quality validation and error handling

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Google Gemini API Key** - Get yours from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd smart-seo-assistant-ace-1/ml_pipeline

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .

# Set up your API key
export GOOGLE_API_KEY=your_api_key_here
# Or create a .env file with: GOOGLE_API_KEY=your_api_key_here
```

### Quick Test

```bash
# Run the test suite
python test_pipeline.py

# Test basic functionality
python examples/basic_usage.py
```

## 📖 Usage Examples

### 1. Python API

```python
from smart_seo_assistant_ace import SEOAssistantPipeline, ConfigurationManager

# Initialize pipeline
config_manager = ConfigurationManager()
config = config_manager.get_pipeline_config()
pipeline = SEOAssistantPipeline(config)

# Analyze a keyword
context = pipeline.retrieve_context("machine learning tutorial")
print(f"Search Intent: {context.search_intent}")
print(f"Related Keywords: {context.related_keywords[:5]}")

# Generate content brief
brief = pipeline.generate_content_brief("python programming guide")
print(f"Title: {brief.title}")
print(f"Word Count Target: {brief.word_count_target}")

# Generate full article
article = pipeline.generate_full_article("data science introduction")
print(f"Total Words: {article.total_word_count}")
```

### 2. Command Line Interface

```bash
# Analyze a keyword
python -m smart_seo_assistant_ace.cli analyze "machine learning"

# Generate content brief
python -m smart_seo_assistant_ace.cli brief "python tutorial" --goal="beginner-friendly"

# Generate full article
python -m smart_seo_assistant_ace.cli article "web development" --output="article.json"

# Bulk process keywords
python -m smart_seo_assistant_ace.cli bulk examples/sample_keywords.txt --calendar
```

### 3. Web API

```bash
# Start the API server
uvicorn smart_seo_assistant_ace.api:app --reload

# Use the API
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "python tutorial", "goal": "educational content"}'
```

### 4. Jupyter Notebook Integration

```python
from examples.notebook_integration import NotebookSEOAssistant

# Initialize notebook assistant
assistant = NotebookSEOAssistant()

# Analyze keywords with visualizations
context = assistant.analyze_keyword_interactive("python machine learning")

# Bulk analysis with charts
keywords = ["python tutorial", "machine learning", "data science"]
df = assistant.bulk_analyze_with_visualization(keywords)

# Create content calendar
calendar, calendar_df = assistant.create_content_calendar_interactive(keywords, weeks=4)
```

## 📁 Project Structure

```
ml_pipeline/
├── src/smart-seo-assistant-ace/
│   ├── __init__.py                 # Package initialization and exports
│   ├── __main__.py                 # Module entry point
│   ├── cli.py                      # Command line interface
│   ├── api.py                      # FastAPI web interface
│   ├── constants/
│   │   └── __init__.py             # Configuration constants
│   ├── entity/
│   │   └── __init__.py             # Data structures and models
│   ├── config/
│   │   └── configuration.py       # Configuration management
│   ├── utils/
│   │   └── __init__.py             # Utility functions
│   ├── components/
│   │   ├── data_retrieval.py       # Data retrieval component
│   │   └── content_generation.py   # Content generation component
│   └── pipeline/
│       └── seo_pipeline.py         # Main pipeline orchestration
├── examples/
│   ├── basic_usage.py              # Basic usage example
│   ├── advanced_usage.py           # Advanced features example
│   ├── notebook_integration.py     # Jupyter notebook integration
│   ├── sample_keywords.txt         # Sample keywords for testing
│   └── README.md                   # Examples documentation
├── requirements.txt                # Python dependencies
├── setup.py                       # Package setup configuration
├── test_pipeline.py               # Comprehensive test suite
└── README.md                      # This file
```

## 🔧 Configuration

### Environment Variables

```bash
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional
GEMINI_MODEL=gemini-1.5-flash      # Default model
MAX_RETRIES=3                      # API retry attempts
TIMEOUT=30                         # Request timeout in seconds
CACHE_ENABLED=true                 # Enable context caching
CACHE_TTL=3600                     # Cache time-to-live in seconds
DEBUG_MODE=false                   # Enable debug logging
```

### Configuration File (config.yaml)

```yaml
gemini_model: "gemini-1.5-flash"
max_retries: 3
timeout: 30
cache_enabled: true
cache_ttl: 3600
debug_mode: false
```

## 📊 API Reference

### Core Classes

#### SEOAssistantPipeline
Main pipeline class that orchestrates the complete workflow.

```python
pipeline = SEOAssistantPipeline(config)

# Main methods
context = pipeline.retrieve_context(keyword, user_goal)
brief = pipeline.generate_content_brief(keyword, user_goal)
article = pipeline.generate_full_article(keyword, user_goal)
results = pipeline.bulk_process_keywords(keywords, user_goal)
calendar = pipeline.plan_content_calendar(keywords, weeks)
```

#### DataRetriever
Component for gathering context from various sources.

```python
retriever = DataRetriever()

# Methods
wikipedia_data = retriever.search_wikipedia(query, max_results)
keywords = retriever.extract_related_keywords(keyword)
opportunities = retriever.generate_content_opportunities(keyword)
questions = retriever.extract_user_questions(keyword)
```

#### ContentGenerator
Component for AI-powered content generation.

```python
generator = ContentGenerator(api_key, model_name)

# Methods
brief = generator.generate_content_brief(context)
article = generator.generate_full_article(context)
title = generator.generate_seo_title(context)
```

### Data Structures

#### SEOContext
```python
@dataclass
class SEOContext:
    keyword: str
    search_intent: str
    related_keywords: List[str]
    content_opportunities: List[str]
    user_questions: List[str]
    wikipedia_data: List[WikipediaResult]
```

#### ContentBrief
```python
@dataclass
class ContentBrief:
    title: str
    meta_description: str
    content_type: str
    word_count_target: int
    content_outline: List[str]
    seo_keywords: List[str]
    call_to_action: str
```

## 🌐 Web API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/analyze` | POST | Analyze keyword |
| `/brief` | POST | Generate content brief |
| `/article` | POST | Generate full article |
| `/bulk` | POST | Bulk process keywords |
| `/calendar` | POST | Create content calendar |
| `/stats` | GET | Pipeline statistics |

### Example API Usage

```bash
# Health check
curl http://localhost:8000/health

# Analyze keyword
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "python tutorial", "goal": "beginner-friendly"}'

# Generate content brief
curl -X POST "http://localhost:8000/brief" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "machine learning", "goal": "comprehensive guide"}'
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python test_pipeline.py

# Test specific components
python -c "from test_pipeline import test_imports; test_imports()"
python -c "from test_pipeline import test_data_retrieval; test_data_retrieval()"
```

## 🔍 Examples

### Basic Keyword Analysis
```python
from smart_seo_assistant_ace import SEOAssistantPipeline, ConfigurationManager

config_manager = ConfigurationManager()
config = config_manager.get_pipeline_config()
pipeline = SEOAssistantPipeline(config)

# Analyze keyword
context = pipeline.retrieve_context("machine learning for beginners")

print(f"Search Intent: {context.search_intent}")
print(f"Related Keywords: {context.related_keywords[:5]}")
print(f"Content Opportunities: {context.content_opportunities[:3]}")
```

### Bulk Content Planning
```python
# Define keywords
keywords = [
    "python tutorial",
    "machine learning basics", 
    "web development guide",
    "data science introduction"
]

# Bulk process
results = pipeline.bulk_process_keywords(keywords, "educational content")

# Create content calendar
calendar = pipeline.plan_content_calendar(keywords, timeframe_weeks=8)

print(f"Generated {len(results)} content briefs")
print(f"Planned {len(calendar.items)} calendar items")
```

## 📈 Performance & Optimization

### Caching
- Context caching reduces API calls for repeated keywords
- Configurable TTL (time-to-live) for cache entries
- Automatic cache cleanup to prevent memory issues

### Rate Limiting
- Built-in retry logic with exponential backoff
- Configurable timeout and retry settings
- Graceful handling of API rate limits

### Batch Processing
- Efficient bulk processing for multiple keywords
- Progress tracking and error handling
- Background processing for large datasets

## 🛠️ Customization

### Adding New Data Sources
```python
class CustomDataRetriever(DataRetriever):
    def get_custom_data(self, keyword):
        # Implement custom data source
        pass
    
    def get_comprehensive_context(self, keyword, user_goal=""):
        context = super().get_comprehensive_context(keyword, user_goal)
        # Add custom data to context
        return context
```

### Custom Content Types
```python
from smart_seo_assistant_ace.entity import ContentType

# Extend ContentType enum
class CustomContentType(ContentType):
    PRODUCT_REVIEW = "product_review"
    CASE_STUDY = "case_study"
```

### Custom Prompts
```python
class CustomContentGenerator(ContentGenerator):
    def generate_custom_content(self, context, content_type):
        # Implement custom content generation
        pass
```

## 🔒 Security & Best Practices

### API Key Management
- Never commit API keys to version control
- Use environment variables or secure configuration files
- Implement API key rotation procedures

### Data Privacy
- No user data is stored permanently
- Context caching is memory-only by default
- All API communications use HTTPS

### Error Handling
- Comprehensive error handling throughout the pipeline
- Graceful degradation when services are unavailable
- Detailed logging for debugging and monitoring

## 🚀 Deployment

### Production Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment variables
export GOOGLE_API_KEY=your_production_key
export CACHE_ENABLED=true
export DEBUG_MODE=false

# Start API server
uvicorn smart_seo_assistant_ace.api:app --host 0.0.0.0 --port 8000
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

EXPOSE 8000
CMD ["uvicorn", "smart_seo_assistant_ace.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone and setup
git clone <repo-url>
cd smart-seo-assistant-ace-1/ml_pipeline

# Install in development mode
pip install -e .
pip install -r requirements.txt

# Run tests
python test_pipeline.py

# Run examples
python examples/basic_usage.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powerful content generation
- Wikipedia for comprehensive knowledge base
- FastAPI for robust web API framework
- The open-source community for excellent tools and libraries

## 📞 Support

- 📖 Documentation: Check the `/examples` directory for detailed usage examples
- 🐛 Bug Reports: Open an issue on GitHub
- 💬 Questions: Start a discussion on GitHub
- 📧 Contact: saudsandhila786@gmail.com

## 🗺️ Roadmap

- [ ] **Enhanced Data Sources**: Google Custom Search, SerpAPI integration
- [ ] **Advanced NLP**: Sentiment analysis, topic modeling
- [ ] **Performance Monitoring**: SEO metrics tracking, SERP position monitoring
- [ ] **Team Collaboration**: Multi-user support, shared calendars
- [ ] **CMS Integration**: WordPress, Ghost, Webflow plugins
- [ ] **Advanced Analytics**: Content performance insights, ROI tracking
- [ ] **Multi-language Support**: Content generation in multiple languages
- [ ] **Visual Content**: Image suggestions, infographic generation

---

**Made with ❤️ for SEO professionals and content creators**
