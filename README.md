# 🚀 Smart SEO Assistant

A production-ready AI-powered SEO content planning and generation tool built with FastAPI, React, and Google Gemini AI.

## ✨ Status: PRODUCTION READY ✅

Full-stack application with comprehensive SEO features:

- ✅ Keyword analysis and competitive intelligence
- ✅ AI-powered content briefs and full articles
- ✅ Bulk processing for multiple keywords
- ✅ Content calendar generation
- ✅ Background task processing
- ✅ Modern React UI with TailwindCSS

## 🏗️ Architecture

```text
├── ml_pipeline/     # AI Pipeline (Google Gemini + LangChain)
├── backend/         # FastAPI REST API
└── frontend/        # React + TypeScript + TailwindCSS
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API Key

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
set GEMINI_API_KEY=your-api-key  # Windows
python start_server.py
```

Backend will be available at: <http://localhost:8000>

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: <http://localhost:5173>

## 🎯 Key Features

### 🔍 SEO Analysis

- Deep keyword research with competitive intelligence
- User intent mapping and content opportunities
- Wikipedia source analysis and relevance scoring

### 📝 Content Planning

- AI-generated content briefs with SEO optimization
- Automatic content type detection
- Data-driven word count recommendations

### 📄 Article Generation

- Complete SEO-optimized articles with proper structure
- Background processing for long-running tasks
- Section-by-section content with headings and flow

### 📊 Bulk Processing

- Process up to 50 keywords simultaneously
- Real-time monitoring and success tracking
- Detailed error reporting

### 📅 Content Calendar

- AI-powered content planning for up to 100 keywords
- Intelligent priority scoring
- Customizable timeframes (1-52 weeks)

## 📚 API Endpoints

- `POST /seo/analyze` - Keyword analysis and insights
- `POST /seo/brief` - Generate content brief
- `POST /seo/article` - Generate full article (background)
- `POST /seo/bulk` - Process multiple keywords
- `POST /seo/calendar` - Create content calendar
- `GET /tasks/{task_id}` - Check task status
- `GET /health` - Health check
- `GET /stats` - Pipeline statistics

## 🛠️ Technology Stack

**Backend:** FastAPI, Google Gemini AI, SQLite, JWT Auth  
**Frontend:** React 19, TypeScript, TailwindCSS, Vite  
**ML Pipeline:** LangChain, Sentence Transformers, FAISS, SpaCy

## 📋 Example Usage

```javascript
// Analyze a keyword
const response = await axios.post('http://localhost:8000/seo/analyze', {
  keyword: 'machine learning tutorials',
  goal: 'Educational content for beginners'
});

// Generate content brief
const brief = await axios.post('http://localhost:8000/seo/brief', {
  keyword: 'python data science',
  goal: 'Comprehensive guide'
});

// Bulk processing
const bulk = await axios.post('http://localhost:8000/seo/bulk', {
  keywords: ['AI tutorials', 'ML algorithms', 'data science'],
  goal: 'Educational content series'
});
```

## 🐛 Troubleshooting

**GEMINI_API_KEY not found:** Set environment variable `set GEMINI_API_KEY="your-key"`  
**Frontend build errors:** Ensure Node.js 16+ and run `npm install`  
**Backend import errors:** Check Python path and ensure correct directory

## 📖 Full Documentation

For comprehensive documentation, setup guides, and advanced features, see [README_FULL.md](README_FULL.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**🎯 Ready for production use with comprehensive SEO features!**
