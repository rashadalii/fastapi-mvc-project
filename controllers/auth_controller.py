from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.schemas.user_schema import UserCreate
from app.schemas.token_schema import Token
from app.services.auth_service import AuthService

# Create router
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/signup", response_model=Token)
async def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> Token:
    """
    Register a new user and return an authentication token.
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        Token: Authentication token for the new user
    """
    # Register the user
    user = AuthService.register_user(db, user_data)
    
    # Create and return token
    return AuthService.create_user_token(user)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Token:
    """
    Authenticate a user and return an authentication token.
    
    Args:
        form_data: OAuth2 form data with username (email) and password
        db: Database session
        
    Returns:
        Token: Authentication token
        
    Raises:
        HTTPException: If authentication fails
    """
    # Authenticate user
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create and return token
    return AuthService.create_user_token(user)