from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from contextlib import asynccontextmanager

from auth import jwt_manager
from database import init_database, close_database, get_db, User as DBUser
from crud import UserCRUD
from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - handles startup and shutdown"""
    # Startup
    await init_database()
    yield
    # Shutdown
    await close_database()


app = FastAPI(
    title="FluxPad API", 
    description="Backend API for FluxPad data interaction platform",
    lifespan=lifespan
)

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://fluxpad-web-production.up.railway.app",  # Production frontend
        "https://*.up.railway.app"  # Any Railway subdomain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class User(BaseModel):
    user_id: str
    email: str
    full_name: str
    created_at: datetime
    is_active: bool = True

# Database-backed user authentication
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    payload = jwt_manager.verify_token(credentials.credentials, "access")
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    db_user = await UserCRUD.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Convert database user to Pydantic model
    return User(
        user_id=db_user.user_id,
        email=db_user.email,
        full_name=db_user.full_name,
        created_at=db_user.created_at,
        is_active=db_user.is_active
    )

# Routes
@app.get("/ping")
async def ping():
    return {"status": "pong"}

@app.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    """Register new user"""
    # Create new user in database
    db_user = await UserCRUD.create_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name
    )
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Generate tokens
    token_data = {
        "user_id": db_user.user_id,
        "email": db_user.email,
        "sub": db_user.email  # Standard JWT claim
    }
    
    access_token = jwt_manager.create_access_token(token_data)
    refresh_token = jwt_manager.create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=jwt_manager.access_token_expire_minutes * 60  # seconds
    )

@app.post("/auth/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login user"""
    # Authenticate user
    db_user = await UserCRUD.authenticate_user(
        db=db,
        email=user_data.email,
        password=user_data.password
    )
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate tokens
    token_data = {
        "user_id": db_user.user_id,
        "email": db_user.email,
        "sub": db_user.email  # Standard JWT claim
    }
    
    access_token = jwt_manager.create_access_token(token_data)
    refresh_token = jwt_manager.create_refresh_token(token_data)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=jwt_manager.access_token_expire_minutes * 60  # seconds
    )

@app.post("/auth/refresh", response_model=TokenResponse)
async def refresh_token(refresh_data: RefreshTokenRequest):
    """Refresh access token using refresh token"""
    try:
        # Verify refresh token and get new access token
        new_access_token = jwt_manager.refresh_access_token(refresh_data.refresh_token)
        
        # Decode to get user info for new refresh token
        payload = jwt_manager.verify_token(refresh_data.refresh_token, "refresh")
        token_data = {
            "user_id": payload.get("user_id"),
            "email": payload.get("email"),
            "sub": payload.get("email")
        }
        
        # Generate new refresh token
        new_refresh_token = jwt_manager.create_refresh_token(token_data)
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=jwt_manager.access_token_expire_minutes * 60
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@app.get("/auth/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user