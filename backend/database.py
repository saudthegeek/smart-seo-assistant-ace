"""
Simple Database Manager for SEO Assistant Backend
Using SQLite for simplicity - can be upgraded to PostgreSQL later
"""

import sqlite3
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


class DatabaseManager:
    """Simple SQLite database manager"""
    
    def __init__(self, db_path: str = "seo_assistant.db"):
        """Initialize database manager"""
        self.db_path = db_path
        self.connection = None
    
    async def initialize(self):
        """Initialize database and create tables"""
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row  # Enable dict-like access
        
        # Create tables
        await self._create_tables()
    
    async def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    async def _create_tables(self):
        """Create database tables"""
        cursor = self.connection.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            )
        """)
        
        # Projects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                website_url TEXT,
                target_audience TEXT,
                goals TEXT,  -- JSON array
                user_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Keyword analyses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS keyword_analyses (
                id TEXT PRIMARY KEY,
                project_id TEXT,
                user_id TEXT NOT NULL,
                keyword TEXT NOT NULL,
                analysis_data TEXT,  -- JSON
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Content briefs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content_briefs (
                id TEXT PRIMARY KEY,
                project_id TEXT,
                user_id TEXT NOT NULL,
                keyword TEXT NOT NULL,
                brief_data TEXT,  -- JSON
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Full articles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS full_articles (
                id TEXT PRIMARY KEY,
                project_id TEXT,
                user_id TEXT NOT NULL,
                keyword TEXT NOT NULL,
                article_data TEXT,  -- JSON
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Content calendars table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS content_calendars (
                id TEXT PRIMARY KEY,
                project_id TEXT,
                user_id TEXT NOT NULL,
                calendar_data TEXT,  -- JSON
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        self.connection.commit()
    
    async def create_user(self, user_data, password_hash: str) -> Dict[str, Any]:
        """Create a new user"""
        user_id = str(uuid.uuid4())
        cursor = self.connection.cursor()
        
        cursor.execute("""
            INSERT INTO users (id, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        """, (user_id, user_data.email, password_hash, user_data.full_name))
        
        self.connection.commit()
        
        return {
            "id": user_id,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "created_at": datetime.utcnow(),
            "is_active": True
        }
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None
    
    async def create_project(self, project_data, user_id: str) -> Dict[str, Any]:
        """Create a new project"""
        project_id = str(uuid.uuid4())
        cursor = self.connection.cursor()
        
        cursor.execute("""
            INSERT INTO projects (id, name, description, website_url, target_audience, goals, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            project_id,
            project_data.name,
            project_data.description,
            project_data.website_url,
            project_data.target_audience,
            json.dumps(project_data.goals or []),
            user_id
        ))
        
        self.connection.commit()
        
        return {
            "id": project_id,
            "name": project_data.name,
            "description": project_data.description,
            "website_url": project_data.website_url,
            "target_audience": project_data.target_audience,
            "goals": project_data.goals or [],
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    
    async def get_user_projects(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all projects for a user"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM projects WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        rows = cursor.fetchall()
        
        projects = []
        for row in rows:
            project = dict(row)
            project["goals"] = json.loads(project["goals"]) if project["goals"] else []
            projects.append(project)
        
        return projects
    
    async def save_keyword_analysis(self, project_id: str, user_id: str, analysis_data: Dict[str, Any]):
        """Save keyword analysis results"""
        analysis_id = str(uuid.uuid4())
        cursor = self.connection.cursor()
        
        cursor.execute("""
            INSERT INTO keyword_analyses (id, project_id, user_id, keyword, analysis_data)
            VALUES (?, ?, ?, ?, ?)
        """, (
            analysis_id,
            project_id,
            user_id,
            analysis_data["keyword"],
            json.dumps(analysis_data)
        ))
        
        self.connection.commit()
        return analysis_id
    
    async def save_content_brief(self, project_id: str, user_id: str, brief_data: Dict[str, Any]):
        """Save content brief"""
        brief_id = str(uuid.uuid4())
        cursor = self.connection.cursor()
        
        cursor.execute("""
            INSERT INTO content_briefs (id, project_id, user_id, keyword, brief_data)
            VALUES (?, ?, ?, ?, ?)
        """, (
            brief_id,
            project_id,
            user_id,
            brief_data.get("keyword", ""),
            json.dumps(brief_data)
        ))
        
        self.connection.commit()
        return brief_id
    
    async def save_full_article(self, project_id: str, user_id: str, article_data: Dict[str, Any]):
        """Save full article"""
        article_id = str(uuid.uuid4())
        cursor = self.connection.cursor()
        
        cursor.execute("""
            INSERT INTO full_articles (id, project_id, user_id, keyword, article_data)
            VALUES (?, ?, ?, ?, ?)
        """, (
            article_id,
            project_id,
            user_id,
            article_data.get("keyword", ""),
            json.dumps(article_data)
        ))
        
        self.connection.commit()
        return article_id
    
    async def save_content_calendar(self, project_id: str, user_id: str, calendar_data: Dict[str, Any]):
        """Save content calendar"""
        calendar_id = str(uuid.uuid4())
        cursor = self.connection.cursor()
        
        cursor.execute("""
            INSERT INTO content_calendars (id, project_id, user_id, calendar_data)
            VALUES (?, ?, ?, ?)
        """, (
            calendar_id,
            project_id,
            user_id,
            json.dumps(calendar_data)
        ))
        
        self.connection.commit()
        return calendar_id
    
    async def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics"""
        cursor = self.connection.cursor()
        
        # Count projects
        cursor.execute("SELECT COUNT(*) as count FROM projects WHERE user_id = ?", (user_id,))
        project_count = cursor.fetchone()["count"]
        
        # Count analyses
        cursor.execute("SELECT COUNT(*) as count FROM keyword_analyses WHERE user_id = ?", (user_id,))
        analysis_count = cursor.fetchone()["count"]
        
        # Count briefs
        cursor.execute("SELECT COUNT(*) as count FROM content_briefs WHERE user_id = ?", (user_id,))
        brief_count = cursor.fetchone()["count"]
        
        # Count articles
        cursor.execute("SELECT COUNT(*) as count FROM full_articles WHERE user_id = ?", (user_id,))
        article_count = cursor.fetchone()["count"]
        
        return {
            "projects": project_count,
            "keyword_analyses": analysis_count,
            "content_briefs": brief_count,
            "full_articles": article_count,
            "updated_at": datetime.utcnow().isoformat()
        }
