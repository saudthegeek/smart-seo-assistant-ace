"""
Authentication module for the SEO Assistant Backend
"""

import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Security configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-insecure-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


class AuthManager:
    """Authentication manager for user auth and JWT tokens"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        if SECRET_KEY == "dev-insecure-change-me":
            logger.warning("JWT secret is using an insecure default. Set JWT_SECRET_KEY in environment for production.")
    
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create a new JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    async def authenticate_user(self, email: str, password: str):
        """Authenticate a user with email and password"""
        try:
            user = await self.db_manager.get_user_by_email(email)
            if not user:
                return False
            
            if not self.verify_password(password, user["password_hash"]):
                return False
            
            return user
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False
    
    async def create_user_account(self, email: str, password: str, full_name: str):
        """Create a new user account"""
        try:
            # Check if user already exists
            existing_user = await self.db_manager.get_user_by_email(email)
            if existing_user:
                raise ValueError("User with this email already exists")
            
            # Hash password and create user
            password_hash = self.hash_password(password)
            user_data = {
                "email": email,
                "password_hash": password_hash,
                "full_name": full_name,
                "is_active": True
            }
            
            user_id = await self.db_manager.create_user(user_data)
            return await self.db_manager.get_user(user_id)
            
        except Exception as e:
            logger.error(f"User creation error: {e}")
            raise


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get the current authenticated user from JWT token"""
    try:
        # Extract token
        token = credentials.credentials
        
        # Decode JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # For now, return a mock user. In production, you'd fetch from database
        return {
            "id": user_id,
            "email": payload.get("email", ""),
            "full_name": payload.get("full_name", ""),
            "is_active": True
        }
        
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_active_user(current_user = Depends(get_current_user)):
    """Get the current active user"""
    if not current_user.get("is_active", False):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
