#!/usr/bin/env python3
"""
Backend startup script for testing
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
current_dir = Path(__file__).parent
env_path = current_dir.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded environment variables from {env_path}")
else:
    print("⚠️  No .env file found, using system environment variables")

# Check if GEMINI_API_KEY is set
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    print(f"✅ GEMINI_API_KEY loaded: {gemini_key[:8]}...")
else:
    print("❌ GEMINI_API_KEY not found!")
    # Set a test key for development if none is found
    os.environ["GEMINI_API_KEY"] = "test-api-key-for-development"
    print("⚠️  Using test API key for development")

# Set JWT secret if not already set
if not os.getenv("JWT_SECRET_KEY"):
    os.environ["JWT_SECRET_KEY"] = "your-super-secret-jwt-key-change-in-production"

# Add the ml_pipeline to Python path
current_dir = Path(__file__).parent
ml_pipeline_path = current_dir.parent / "ml_pipeline" / "src"
sys.path.insert(0, str(ml_pipeline_path))

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Smart SEO Assistant Backend...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("📋 Health Check: http://localhost:8000/health")
    print("")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
