"""
Storage module for the SEO Assistant Backend
Handles file storage for articles, analyses, and other content
"""

import os
import json
import aiofiles
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class StorageManager:
    """Manages file storage for SEO Assistant content"""
    
    def __init__(self, storage_dir: str = "storage"):
        self.storage_dir = Path(storage_dir)
        self.articles_dir = self.storage_dir / "articles"
        self.analyses_dir = self.storage_dir / "analyses" 
        self.briefs_dir = self.storage_dir / "briefs"
        self.calendars_dir = self.storage_dir / "calendars"
        self.uploads_dir = self.storage_dir / "uploads"
        
        # Create directories if they don't exist
        self._create_directories()
    
    def _create_directories(self):
        """Create storage directories"""
        for directory in [
            self.storage_dir,
            self.articles_dir,
            self.analyses_dir,
            self.briefs_dir,
            self.calendars_dir,
            self.uploads_dir
        ]:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Storage directory ready: {directory}")
    
    async def save_article(self, article_data: Dict[str, Any], user_id: str, project_id: str = None) -> str:
        """Save a generated article to storage"""
        try:
            # Generate unique filename
            article_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{article_id}.json"
            
            # Add metadata
            article_data.update({
                "id": article_id,
                "user_id": user_id,
                "project_id": project_id,
                "saved_at": datetime.utcnow().isoformat(),
                "type": "article"
            })
            
            # Save to file
            file_path = self.articles_dir / filename
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(article_data, indent=2, ensure_ascii=False))
            
            logger.info(f"Article saved: {file_path}")
            return article_id
            
        except Exception as e:
            logger.error(f"Failed to save article: {e}")
            raise
    
    async def save_analysis(self, analysis_data: Dict[str, Any], user_id: str, project_id: str = None) -> str:
        """Save SEO analysis to storage"""
        try:
            # Generate unique filename
            analysis_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{analysis_id}.json"
            
            # Add metadata
            analysis_data.update({
                "id": analysis_id,
                "user_id": user_id,
                "project_id": project_id,
                "saved_at": datetime.utcnow().isoformat(),
                "type": "analysis"
            })
            
            # Save to file
            file_path = self.analyses_dir / filename
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(analysis_data, indent=2, ensure_ascii=False))
            
            logger.info(f"Analysis saved: {file_path}")
            return analysis_id
            
        except Exception as e:
            logger.error(f"Failed to save analysis: {e}")
            raise
    
    async def save_brief(self, brief_data: Dict[str, Any], user_id: str, project_id: str = None) -> str:
        """Save content brief to storage"""
        try:
            # Generate unique filename
            brief_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{brief_id}.json"
            
            # Add metadata
            brief_data.update({
                "id": brief_id,
                "user_id": user_id,
                "project_id": project_id,
                "saved_at": datetime.utcnow().isoformat(),
                "type": "brief"
            })
            
            # Save to file
            file_path = self.briefs_dir / filename
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(brief_data, indent=2, ensure_ascii=False))
            
            logger.info(f"Brief saved: {file_path}")
            return brief_id
            
        except Exception as e:
            logger.error(f"Failed to save brief: {e}")
            raise
    
    async def save_calendar(self, calendar_data: Dict[str, Any], user_id: str, project_id: str = None) -> str:
        """Save content calendar to storage"""
        try:
            # Generate unique filename
            calendar_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{calendar_id}.json"
            
            # Add metadata
            calendar_data.update({
                "id": calendar_id,
                "user_id": user_id,
                "project_id": project_id,
                "saved_at": datetime.utcnow().isoformat(),
                "type": "calendar"
            })
            
            # Save to file
            file_path = self.calendars_dir / filename
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(calendar_data, indent=2, ensure_ascii=False))
            
            logger.info(f"Calendar saved: {file_path}")
            return calendar_id
            
        except Exception as e:
            logger.error(f"Failed to save calendar: {e}")
            raise
    
    async def load_content(self, content_id: str, content_type: str) -> Optional[Dict[str, Any]]:
        """Load content by ID and type"""
        try:
            # Determine directory based on content type
            if content_type == "article":
                search_dir = self.articles_dir
            elif content_type == "analysis":
                search_dir = self.analyses_dir
            elif content_type == "brief":
                search_dir = self.briefs_dir
            elif content_type == "calendar":
                search_dir = self.calendars_dir
            else:
                raise ValueError(f"Unknown content type: {content_type}")
            
            # Search for file with content_id
            for file_path in search_dir.glob("*.json"):
                async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                    content = json.loads(await f.read())
                    if content.get("id") == content_id:
                        return content
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to load content {content_id}: {e}")
            return None
    
    async def list_user_content(self, user_id: str, content_type: str, project_id: str = None) -> List[Dict[str, Any]]:
        """List all content for a user"""
        try:
            # Determine directory based on content type
            if content_type == "article":
                search_dir = self.articles_dir
            elif content_type == "analysis":
                search_dir = self.analyses_dir
            elif content_type == "brief":
                search_dir = self.briefs_dir
            elif content_type == "calendar":
                search_dir = self.calendars_dir
            else:
                raise ValueError(f"Unknown content type: {content_type}")
            
            content_list = []
            
            # Search through files
            for file_path in search_dir.glob("*.json"):
                try:
                    async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                        content = json.loads(await f.read())
                        
                        # Filter by user_id and optionally project_id
                        if content.get("user_id") == user_id:
                            if project_id is None or content.get("project_id") == project_id:
                                content_list.append(content)
                                
                except Exception as e:
                    logger.warning(f"Failed to load file {file_path}: {e}")
                    continue
            
            # Sort by saved_at (newest first)
            content_list.sort(key=lambda x: x.get("saved_at", ""), reverse=True)
            return content_list
            
        except Exception as e:
            logger.error(f"Failed to list user content: {e}")
            return []
    
    async def delete_content(self, content_id: str, content_type: str, user_id: str) -> bool:
        """Delete content by ID (with user ownership check)"""
        try:
            # Load content first to verify ownership
            content = await self.load_content(content_id, content_type)
            if not content:
                return False
            
            # Check ownership
            if content.get("user_id") != user_id:
                logger.warning(f"User {user_id} tried to delete content owned by {content.get('user_id')}")
                return False
            
            # Determine directory and find file to delete
            if content_type == "article":
                search_dir = self.articles_dir
            elif content_type == "analysis":
                search_dir = self.analyses_dir
            elif content_type == "brief":
                search_dir = self.briefs_dir
            elif content_type == "calendar":
                search_dir = self.calendars_dir
            else:
                return False
            
            # Find and delete the file
            for file_path in search_dir.glob("*.json"):
                try:
                    async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                        file_content = json.loads(await f.read())
                        if file_content.get("id") == content_id:
                            os.remove(file_path)
                            logger.info(f"Deleted content: {file_path}")
                            return True
                except Exception as e:
                    logger.warning(f"Failed to check file {file_path}: {e}")
                    continue
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete content {content_id}: {e}")
            return False
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        try:
            stats = {
                "storage_dir": str(self.storage_dir),
                "total_articles": len(list(self.articles_dir.glob("*.json"))),
                "total_analyses": len(list(self.analyses_dir.glob("*.json"))),
                "total_briefs": len(list(self.briefs_dir.glob("*.json"))),
                "total_calendars": len(list(self.calendars_dir.glob("*.json"))),
                "directories": {
                    "articles": str(self.articles_dir),
                    "analyses": str(self.analyses_dir),
                    "briefs": str(self.briefs_dir),
                    "calendars": str(self.calendars_dir),
                    "uploads": str(self.uploads_dir)
                }
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get storage stats: {e}")
            return {}
