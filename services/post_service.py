from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.post_model import Post
from app.models.user_model import User
from app.schemas.post_schema import PostCreate
from app.services.cache_service import cache

class PostService:
    """Service for handling post operations."""
    
    @staticmethod
    def create_post(db: Session, post_data: PostCreate, user: User) -> Post:
        """
        Create a new post for a user.
        
        Args:
            db: Database session
            post_data: Post creation data
            user: User creating the post
            
        Returns:
            Post: Created post object
        """
        # Create new post
        new_post = Post(
            text=post_data.text,
            user_id=user.id
        )
        
        # Save to database
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        
        # Invalidate cache for user posts
        cache_key = f"user_posts_{user.id}"
        cache.delete(cache_key)
        
        return new_post
    
    @staticmethod
    def get_user_posts(db: Session, user: User) -> List[Post]:
        """
        Get all posts for a user with caching.
        
        Args:
            db: Database session
            user: User to get posts for
            
        Returns:
            List[Post]: List of user's posts
        """
        # Try to get from cache first
        cache_key = f"user_posts_{user.id}"
        cached_posts = cache.get(cache_key)
        
        if cached_posts is not None:
            return cached_posts
        
        # If not in cache, query database
        posts = db.query(Post).filter(Post.user_id == user.id).all()
        
        # Store in cache
        cache.set(cache_key, posts)
        
        return posts
    
    @staticmethod
    def delete_post(db: Session, post_id: int, user: User) -> bool:
        """
        Delete a post if it belongs to the user.
        
        Args:
            db: Database session
            post_id: ID of the post to delete
            user: User attempting to delete the post
            
        Returns:
            bool: True if deleted successfully
            
        Raises:
            HTTPException: If post not found or doesn't belong to user
        """
        # Get post by ID
        post = db.query(Post).filter(Post.id == post_id).first()
        
        # Check if post exists
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
            
        # Check if post belongs to user
        if post.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this post"
            )
        
        # Delete post
        db.delete(post)
        db.commit()
        
        # Invalidate cache for user posts
        cache_key = f"user_posts_{user.id}"
        cache.delete(cache_key)
        
        return True