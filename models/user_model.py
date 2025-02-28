from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.models.database import Base

class User(Base):
    """
    SQLAlchemy model for user data.
    
    Attributes:
        id: Unique identifier for the user
        email: User's email address (unique)
        hashed_password: Hashed version of the user's password
        created_at: Timestamp when the user was created
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"