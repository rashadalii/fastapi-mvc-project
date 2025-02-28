from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    """
    Base Pydantic model for post data.
    
    Attributes:
        text: Content of the post
    """
    text: str = Field(..., min_length=1, description="Post content")
    
    @validator('text')
    def text_not_empty(cls, v):
        """Validate text is not empty"""
        if not v.strip():
            raise ValueError('Post text cannot be empty')
        return v

class PostCreate(PostBase):
    """
    Pydantic model for post creation requests.
    
    Attributes:
        text: Content of the post
    """
    pass

class PostInDB(PostBase):
    """
    Pydantic model for post data from database.
    
    Attributes:
        id: Post's unique identifier
        text: Content of the post
        user_id: ID of the user who created the post
        created_at: Timestamp when the post was created
    """
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class Post(PostBase):
    """
    Pydantic model for post data in responses.
    
    Attributes:
        id: Post's unique identifier
        text: Content of the post
        created_at: Timestamp when the post was created
    """
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class PostDelete(BaseModel):
    """
    Pydantic model for post deletion requests.
    
    Attributes:
        post_id: ID of the post to delete
    """
    post_id: int = Field(..., gt=0, description="ID of the post to delete")