from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime

from auth import jwt_manager

app = FastAPI(title="FluxPad API", description="Backend API for FluxPad data interaction platform")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# In-memory user storage (we'll replace this with a database later)
# Structure: {user_id: {email, full_name, hashed_password, created_at, is_active}}
users_db = {}
# Email to user_id mapping for quick lookup
email_to_user_id = {}

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

# Utility functions
def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email address"""
    user_id = email_to_user_id.get(email)
    if not user_id or user_id not in users_db:
        return None
    
    user_data = users_db[user_id]
    return User(
        user_id=user_id,
        email=user_data["email"],
        full_name=user_data["full_name"],
        created_at=user_data["created_at"],
        is_active=user_data["is_active"]
    )

def get_user_by_id(user_id: str) -> Optional[User]:
    """Get user by user ID"""
    if user_id not in users_db:
        return None
    
    user_data = users_db[user_id]
    return User(
        user_id=user_id,
        email=user_data["email"],
        full_name=user_data["full_name"],
        created_at=user_data["created_at"],
        is_active=user_data["is_active"]
    )

def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    user_id = email_to_user_id.get(email)
    if not user_id or user_id not in users_db:
        return None
    
    user_data = users_db[user_id]
    if not jwt_manager.verify_password(password, user_data["hashed_password"]):
        return None
    
    return get_user_by_id(user_id)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user from JWT token"""
    payload = jwt_manager.verify_token(credentials.credentials, "access")
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

# Routes
@app.get("/ping")
async def ping():
    return {"status": "pong"}

@app.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserRegister):
    """Register new user"""
    # Check if email already exists
    if get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = jwt_manager.hash_password(user_data.password)
    
    # Store user data
    users_db[user_id] = {
        "email": user_data.email,
        "full_name": user_data.full_name,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow(),
        "is_active": True,
    }
    email_to_user_id[user_data.email] = user_id
    
    # Generate tokens
    token_data = {
        "user_id": user_id,
        "email": user_data.email,
        "sub": user_data.email  # Standard JWT claim
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
async def login(user_data: UserLogin):
    """Login user"""
    # Authenticate user
    user = authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate tokens
    token_data = {
        "user_id": user.user_id,
        "email": user.email,
        "sub": user.email  # Standard JWT claim
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