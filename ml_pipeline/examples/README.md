# Smart SEO Assistant Examples

This directory contains practical examples demonstrating how to use the Smart SEO Assistant Pipeline for various SEO content generation tasks.

## 🚀 Quick Start

### Prerequisites

1. **Install Dependencies**
   ```bash
   cd ml_pipeline
   pip install -r requirements.txt
   pip install -e .
   ```

2. **Set up API Key**
   - Get your Gemini API key from: https://aistudio.google.com/app/apikey
   - Create a `.env` file in the project root:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```
   - Or set environment variable:
     ```bash
     export GEMINI_API_KEY=your_api_key_here
     ```

## 📁 Examples Overview

### 1. Basic Usage (`basic_usage.py`)
**Purpose**: Learn the fundamentals of the SEO Assistant Pipeline

**What it demonstrates**:
- Pipeline initialization and configuration
- Keyword analysis (Advanced Retrieval phase)
- Content brief generation (Context Design + Execution phases)
- Basic insights and statistics

**Run it**:
```bash
cd examples
python basic_usage.py
```

**Expected output**:
- Keyword analysis for "machine learning for beginners"
- Related keywords, content opportunities, and user questions
- Generated content brief with title, outline, and SEO keywords
- Pipeline performance statistics

### 2. Advanced Usage (`advanced_usage.py`)
**Purpose**: Explore bulk processing and content planning features

**What it demonstrates**:
- Bulk keyword processing
- Content calendar creation
- Full article generation
- Performance tracking and reporting
- File output and data persistence

**Run it**:
```bash
cd examples
python advanced_usage.py
```

**Expected output**:
- Bulk processing of 8 tech-related keywords
- 8-week content calendar with prioritized items
- Sample full article generation
- JSON files with results, calendar, and article data

### 3. Sample Keywords (`sample_keywords.txt`)
**Purpose**: Pre-defined keyword list for testing

**Usage**:
- Use with CLI bulk processing
- Test data for advanced examples
- Template for your own keyword lists

## 🖥️ Command Line Interface (CLI)

The pipeline includes a powerful CLI for interactive use:

### Basic Commands

```bash
# Analyze a single keyword
python -m smart_seo_assistant_ace.cli analyze "python tutorial"

# Generate content brief
python -m smart_seo_assistant_ace.cli brief "machine learning" --goal="beginner-friendly"

# Generate full article
python -m smart_seo_assistant_ace.cli article "web development" --output="article.json"

# Bulk process keywords from file
python -m smart_seo_assistant_ace.cli bulk examples/sample_keywords.txt

# Create content calendar
python -m smart_seo_assistant_ace.cli bulk examples/sample_keywords.txt --calendar --weeks=8
```

### CLI Examples

1. **Quick Keyword Analysis**:
   ```bash
   python -m smart_seo_assistant_ace.cli analyze "react hooks tutorial"
   ```

2. **Content Brief with Specific Goal**:
   ```bash
   python -m smart_seo_assistant_ace.cli brief "python data visualization" --goal="create comprehensive guide for data scientists"
   ```

3. **Bulk Processing with Calendar**:
   ```bash
   python -m smart_seo_assistant_ace.cli bulk examples/sample_keywords.txt --calendar --weeks=12
   ```

## 🌐 Web API

Start the FastAPI web server for REST API access:

```bash
# Start the API server
uvicorn smart_seo_assistant_ace.api:app --reload --host 0.0.0.0 --port 8000
```

### API Endpoints

- **Health Check**: `GET /health`
- **Keyword Analysis**: `POST /analyze`
- **Content Brief**: `POST /brief`
- **Full Article**: `POST /article`
- **Bulk Processing**: `POST /bulk`
- **Content Calendar**: `POST /calendar`
- **Pipeline Stats**: `GET /stats`

### API Examples

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

## 📊 Output Examples

### Keyword Analysis Output
```
🎯 KEYWORD ANALYSIS: machine learning for beginners
============================================================

📊 Search Intent: Informational

🔗 Related Keywords (15):
  1. machine learning basics
  2. ML tutorial for beginners
  3. introduction to machine learning
  ...

💡 Content Opportunities (10):
  1. Step-by-step beginner tutorial
  2. Common machine learning algorithms explained
  ...

❓ User Questions (10):
  1. What is machine learning in simple terms?
  2. How to start learning machine learning?
  ...
```

### Content Brief Output
```
📝 CONTENT BRIEF: machine learning for beginners
============================================================

🏷️  Title: Complete Machine Learning Guide for Beginners: Start Your AI Journey Today
📄 Meta Description: Learn machine learning from scratch with this comprehensive beginner guide. Discover algorithms, tools, and practical examples to kickstart your AI career.
📊 Target Word Count: 2500
🎯 Content Type: GUIDE

📖 Content Outline:
  1. What is Machine Learning? (Simple Explanation)
  2. Types of Machine Learning (Supervised, Unsupervised, Reinforcement)
  3. Essential Tools and Libraries for Beginners
  ...
```

## 🛠️ Customization

### Configuration Options

Create a `config.yaml` file to customize pipeline behavior:

```yaml
# config.yaml
gemini_model: "gemini-1.5-flash"
max_retries: 3
timeout: 30
cache_enabled: true
cache_ttl: 3600
debug_mode: false
```

### Environment Variables

```bash
# API Configuration
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# Pipeline Settings
MAX_RETRIES=3
TIMEOUT=30
CACHE_ENABLED=true
CACHE_TTL=3600
DEBUG_MODE=false
```

## 🚦 Error Handling

The pipeline includes robust error handling:

- **API Key Missing**: Clear instructions to set up Gemini API key
- **Network Issues**: Automatic retries with exponential backoff
- **Rate Limits**: Intelligent rate limiting and queue management
- **Invalid Input**: Validation and helpful error messages

## 📈 Performance Tips

1. **Enable Caching**: Speeds up repeated requests
2. **Batch Processing**: Use bulk operations for multiple keywords
3. **Async Processing**: Use background tasks for large datasets
4. **Resource Management**: Monitor API usage and rate limits

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   pip install -e .  # Install package in development mode
   ```

2. **API Key Issues**:
   ```bash
   echo $GEMINI_API_KEY  # Check if API key is set
   ```

3. **Permission Errors**:
   ```bash
   chmod +x examples/*.py  # Make scripts executable
   ```

## 📚 Next Steps

1. **Integrate with CMS**: Connect to WordPress, Ghost, or other platforms
2. **Custom Content Types**: Extend for specific industry needs
3. **Performance Monitoring**: Track SEO metrics and content performance
4. **Automation**: Set up scheduled content generation
5. **Team Collaboration**: Share calendars and briefs with team members

## 🤝 Contributing

See the main project README for contribution guidelines.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
