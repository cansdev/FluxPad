"""
CRUD (Create, Read, Update, Delete) operations for FluxPad database
Database operations for users, datasets, and queries
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import Optional
from datetime import datetime

from database import User, Dataset, Query
from auth import jwt_manager


class UserCRUD:
    """User database operations"""
    
    @staticmethod
    async def create_user(
        db: AsyncSession,
        email: str,
        password: str,
        full_name: str
    ) -> Optional[User]:
        """Create a new user"""
        try:
            # Hash password
            hashed_password = jwt_manager.hash_password(password)
            
            # Create user object
            user = User(
                email=email,
                full_name=full_name,
                hashed_password=hashed_password,
                created_at=datetime.utcnow(),
                is_active=True
            )
            
            # Add to database
            db.add(user)
            await db.commit()
            await db.refresh(user)
            
            return user
            
        except IntegrityError:
            # Email already exists
            await db.rollback()
            return None
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email address"""
        result = await db.execute(
            select(User).where(User.email == email, User.is_active == True)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
        """Get user by user ID"""
        result = await db.execute(
            select(User).where(User.user_id == user_id, User.is_active == True)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        email: str,
        password: str
    ) -> Optional[User]:
        """Authenticate user with email and password"""
        user = await UserCRUD.get_user_by_email(db, email)
        
        if not user:
            return None
        
        if not jwt_manager.verify_password(password, user.hashed_password):
            return None
        
        return user
    
    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: str,
        full_name: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Optional[User]:
        """Update user information"""
        user = await UserCRUD.get_user_by_id(db, user_id)
        
        if not user:
            return None
        
        if full_name is not None:
            user.full_name = full_name
        
        if is_active is not None:
            user.is_active = is_active
        
        user.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(user)
        
        return user
    
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: str) -> bool:
        """Soft delete user (set is_active to False)"""
        user = await UserCRUD.get_user_by_id(db, user_id)
        
        if not user:
            return False
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        
        await db.commit()
        return True


class DatasetCRUD:
    """Dataset database operations"""
    
    @staticmethod
    async def create_dataset(
        db: AsyncSession,
        user_id: str,
        name: str,
        file_name: str,
        file_size: int,
        description: Optional[str] = None,
        columns_info: Optional[str] = None,
        row_count: int = 0
    ) -> Dataset:
        """Create a new dataset"""
        dataset = Dataset(
            user_id=user_id,
            name=name,
            description=description,
            file_name=file_name,
            file_size=file_size,
            columns_info=columns_info,
            row_count=row_count,
            created_at=datetime.utcnow(),
            is_active=True
        )
        
        db.add(dataset)
        await db.commit()
        await db.refresh(dataset)
        
        return dataset
    
    @staticmethod
    async def get_user_datasets(
        db: AsyncSession,
        user_id: str,
        active_only: bool = True
    ) -> list[Dataset]:
        """Get all datasets for a user"""
        query = select(Dataset).where(Dataset.user_id == user_id)
        
        if active_only:
            query = query.where(Dataset.is_active == True)
        
        query = query.order_by(Dataset.created_at.desc())
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_dataset_by_id(
        db: AsyncSession,
        dataset_id: str,
        user_id: Optional[str] = None
    ) -> Optional[Dataset]:
        """Get dataset by ID, optionally filtered by user"""
        query = select(Dataset).where(
            Dataset.dataset_id == dataset_id,
            Dataset.is_active == True
        )
        
        if user_id:
            query = query.where(Dataset.user_id == user_id)
        
        result = await db.execute(query)
        return result.scalar_one_or_none()


class QueryCRUD:
    """Query database operations"""
    
    @staticmethod
    async def create_query(
        db: AsyncSession,
        user_id: str,
        dataset_id: str,
        natural_language_query: str,
        generated_sql: Optional[str] = None,
        result_data: Optional[str] = None
    ) -> Query:
        """Create a new query record"""
        query = Query(
            user_id=user_id,
            dataset_id=dataset_id,
            natural_language_query=natural_language_query,
            generated_sql=generated_sql,
            result_data=result_data,
            created_at=datetime.utcnow()
        )
        
        db.add(query)
        await db.commit()
        await db.refresh(query)
        
        return query
    
    @staticmethod
    async def get_user_queries(
        db: AsyncSession,
        user_id: str,
        dataset_id: Optional[str] = None,
        limit: int = 50
    ) -> list[Query]:
        """Get user's query history"""
        query = select(Query).where(Query.user_id == user_id)
        
        if dataset_id:
            query = query.where(Query.dataset_id == dataset_id)
        
        query = query.order_by(Query.created_at.desc()).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()