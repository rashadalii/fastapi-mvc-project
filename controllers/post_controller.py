from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.user_model import User
from app.schemas.post_schema import Post, PostCreate, PostDelete
from app.services.post_service import PostService
from app.dependencies.auth_dependency import get_current_user
from app.utils.validator import validate_payload_size

# Create router
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.post("/add", response_model=Post, status_code=status.HTTP_201_CREATED)
async def add_post(
    request: Request,
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Post:
    """
    Create a new post for the authenticated user.
    
    Args:
        request: FastAPI request object for payload validation
        post_data: Post creation data
        db: Database session
        current_user: Authenticated user from token
        
    Returns:
        Post: Created post
    """
    # Validate payload size
    await validate_payload_size(request)
    
    # Create post
    return PostService.create_post(db, post_data, current_user)

@router.get("/", response_model=List[Post])
async def get_posts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[Post]:
    """
    Get all posts for the authenticated user.
    
    Args:
        db: Database session
        current_user: Authenticated user from token
        
    Returns:
        List[Post]: List of user's posts
    """
    return PostService.get_user_posts(db, current_user)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_data: PostDelete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:
    """
    Delete a post belonging to the authenticated user.
    
    Args:
        post_data: Post deletion data with post ID
        db: Database session
        current_user: Authenticated user from token
    """
    PostService.delete_post(db, post_data.post_id, current_user)