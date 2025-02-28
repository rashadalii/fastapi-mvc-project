from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base

class Post(Base):
    """
    SQLAlchemy model for post data.
    
    Attributes:
        id: Unique identifier for the post
        text: Content of the post
        user_id: Foreign key referencing the user who created the post
        created_at: Timestamp when the post was created
        user: Relationship with the User model
    """
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    
    # Define relationship with User model
    user = relationship("User", backref="posts")
    
    def __repr__(self):
        return f"<Post(id={self.id}, user_id={self.user_id})>"