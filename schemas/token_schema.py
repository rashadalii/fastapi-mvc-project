from pydantic import BaseModel, Field
from typing import Optional

class Token(BaseModel):
    """
    Pydantic model for authentication token response.
    
    Attributes:
        access_token: JWT token string
        token_type: Type of token (bearer)
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")

class TokenData(BaseModel):
    """
    Pydantic model for decoded token data.
    
    Attributes:
        user_id: User ID extracted from token
        email: User email extracted from token
    """
    user_id: Optional[int] = None
    email: Optional[str] = None