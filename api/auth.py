"""
JWT Authentication Module for FluxPad
Production-ready JWT implementation with auto-generated secrets
"""

import os
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from fastapi import HTTPException, status


class JWTManager:
    """Production JWT Manager with auto-generated secrets"""
    
    def __init__(self):
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 60 * 24 * 7  # 7 days
        self.refresh_token_expire_days = 30  # 30 days
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Initialize or load JWT secret
        self.secret_key = self._get_or_create_secret()
    
    def _get_or_create_secret(self) -> str:
        """Get existing JWT secret or create a new one"""
        secret_file = Path(".jwt_secret")
        
        if secret_file.exists():
            # Load existing secret
            with open(secret_file, "r") as f:
                return f.read().strip()
        else:
            # Generate new cryptographically secure secret
            secret = secrets.token_urlsafe(64)  # 512 bits of entropy
            
            # Save secret securely
            with open(secret_file, "w") as f:
                f.write(secret)
            
            # Secure file permissions (Unix/Linux)
            try:
                os.chmod(secret_file, 0o600)  # Read/write for owner only
            except (OSError, AttributeError):
                pass  # Windows doesn't support chmod
            
            print(f"✅ Generated new JWT secret key: {secret_file}")
            return secret
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, data: dict) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        })
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str, token_type: str = "access") -> dict:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Verify token type
            if payload.get("type") != token_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Invalid token type. Expected {token_type}"
                )
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    def hash_password(self, password: str) -> str:
        """Hash password with bcrypt"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """Generate new access token from refresh token"""
        payload = self.verify_token(refresh_token, "refresh")
        
        # Create new access token with same user data
        new_payload = {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "user_id": payload.get("user_id")
        }
        
        return self.create_access_token(new_payload)


# Global JWT manager instance
jwt_manager = JWTManager()