#!/usr/bin/env python3
"""
Test environment setup for Smart SEO Assistant
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def main():
    print("🔧 Environment Setup Check")
    print("=" * 50)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check current directory
    print(f"Current directory: {os.getcwd()}")
    
    # Load .env file
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ .env file found and loaded")
    else:
        print("⚠️  .env file not found")
    
    # Check if we're in the right directory
    backend_path = Path("backend")
    frontend_path = Path("frontend")
    ml_pipeline_path = Path("ml_pipeline")
    
    print(f"Backend directory exists: {backend_path.exists()}")
    print(f"Frontend directory exists: {frontend_path.exists()}")
    print(f"ML Pipeline directory exists: {ml_pipeline_path.exists()}")
    
    # Check environment variables
    print("\n📋 Environment Variables:")
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        print(f"✅ GEMINI_API_KEY: {gemini_key[:8]}...")
        print("🔑 API Key is properly configured!")
    else:
        print("❌ GEMINI_API_KEY: Not set")
        print("⚠️  Please set your Google Gemini API key in .env file")
    
    jwt_secret = os.getenv("JWT_SECRET_KEY")
    if jwt_secret:
        print(f"✅ JWT_SECRET_KEY: Set")
    else:
        print("⚠️ JWT_SECRET_KEY: Not set (will use default)")
    
    print("\n✅ Environment check complete!")
    
    if gemini_key and gemini_key.startswith("AIzaSy"):
        print("\n🚀 Ready to start the application:")
        print("1. Backend: cd backend && python start_server.py")
        print("2. Frontend: cd frontend && npm run dev")
        print("3. Demo: python demo.py")
        print("\n🎯 Status: READY FOR USE! ✅")
    else:
        print("\n⚠️  Please configure GEMINI_API_KEY in .env file first")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
