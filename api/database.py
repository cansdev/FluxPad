"""
Database Configuration and Models for FluxPad
SQLite database with SQLAlchemy ORM for lightweight, fast data storage
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer
from datetime import datetime
import uuid
from pathlib import Path

# Database configuration
import os

# Railway database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./fluxpad.db")

# Handle Railway's PostgreSQL URL format if provided
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    future=True
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for all models
Base = declarative_base()


class User(Base):
    """User model for authentication and user management"""
    __tablename__ = "users"

    # Primary key - UUID as string
    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # User information
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<User(email='{self.email}', full_name='{self.full_name}')>"


class Dataset(Base):
    """Dataset model for uploaded CSV/Excel files"""
    __tablename__ = "datasets"

    # Primary key
    dataset_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign key to user
    user_id = Column(String, nullable=False, index=True)
    
    # Dataset information
    name = Column(String, nullable=False)
    description = Column(Text)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer)  # Size in bytes
    
    # Schema information
    columns_info = Column(Text)  # JSON string of column metadata
    row_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<Dataset(name='{self.name}', user_id='{self.user_id}')>"


class Query(Base):
    """Query model for storing user queries and results"""
    __tablename__ = "queries"

    # Primary key
    query_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign keys
    user_id = Column(String, nullable=False, index=True)
    dataset_id = Column(String, nullable=False, index=True)
    
    # Query information
    natural_language_query = Column(Text, nullable=False)
    generated_sql = Column(Text)
    result_data = Column(Text)  # JSON string of query results
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Query(user_id='{self.user_id}', dataset_id='{self.dataset_id}')>"


# Database utility functions
async def get_async_session():
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_database():
    """Initialize database and create tables"""
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database initialized: fluxpad.db")
    print(f"📁 Database location: {Path('./fluxpad.db').absolute()}")


async def close_database():
    """Close database connection"""
    await engine.dispose()
    print("🔒 Database connection closed")


# Database session dependency for FastAPI
async def get_db():
    """FastAPI dependency for database sessions"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()