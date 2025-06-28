# Smart SEO Assistant (ACE-Powered)

This is a small-scale but scalable project that applies **Automatic Context Engineering (ACE)** to SEO content generation. It accepts a keyword and returns a content brief powered by AI + context intelligence.

## 🚀 Tech Stack

- **Frontend:** React (TypeScript), Tailwind CSS
- **Backend:** FastAPI, Python 3.10+
- **LLM Integration (Next):** OpenAI / Claude / Gemini
- **Future:** LangChain, Vector DB (Qdrant), RAG

## 🧠 Features

- Accepts keyword as input
- Builds basic SEO brief dynamically
- Easy to extend into full SEO content engine

## 📦 Getting Started

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
