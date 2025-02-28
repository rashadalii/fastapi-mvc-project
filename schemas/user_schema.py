from pydantic import BaseModel, EmailStr, Field, validator
import re

class UserBase(BaseModel):
    """
    Base Pydantic model for user data.
    
    Attributes:
        email: User's email address
    """
    email: EmailStr = Field(..., description="User email address")
    
    @validator('email')
    def email_must_be_valid(cls, v):
        """Validate email format"""
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", v):
            raise ValueError('Invalid email format')
        return v

class UserCreate(UserBase):
    """
    Pydantic model for user creation requests.
    
    Attributes:
        email: User's email address
        password: User's password
    """
    password: str = Field(..., min_length=8, max_length=100, description="User password")
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

class UserLogin(UserBase):
    """
    Pydantic model for user login requests.
    
    Attributes:
        email: User's email address
        password: User's password
    """
    password: str = Field(..., min_length=1, description="User password")

class UserInDB(UserBase):
    """
    Pydantic model for user data from database.
    
    Attributes:
        id: User's unique identifier
        email: User's email address
        hashed_password: Hashed version of the user's password
    """
    id: int
    hashed_password: str
    
    class Config:
        orm_mode = True

class User(UserBase):
    """
    Pydantic model for user data in responses.
    
    Attributes:
        id: User's unique identifier
        email: User's email address
    """
    id: int
    
    class Config:
        orm_mode = True