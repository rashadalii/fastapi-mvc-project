from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.schemas.token_schema import Token
from app.utils.auth import verify_password, get_password_hash, create_access_token
from app.config import get_settings

settings = get_settings()

class AuthService:
    """Service for handling user authentication operations."""
    
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        """
        Register a new user.
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            User: Created user object
            
        Raises:
            HTTPException: If email already exists
        """
        # Check if user with this email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        # Save to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.
        
        Args:
            db: Database session
            email: User's email
            password: User's password
            
        Returns:
            User: Authenticated user or None if authentication fails
        """
        # Get user by email
        user = db.query(User).filter(User.email == email).first()
        
        # Check if user exists and password is correct
        if not user or not verify_password(password, user.hashed_password):
            return None
            
        return user
    
    @staticmethod
    def create_user_token(user: User) -> Token:
        """
        Create authentication token for a user.
        
        Args:
            user: User to create token for
            
        Returns:
            Token: Authentication token
        """
        # Create token with user ID and email
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")