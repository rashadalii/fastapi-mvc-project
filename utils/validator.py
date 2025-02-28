from fastapi import HTTPException, Request
import sys

async def validate_payload_size(request: Request, max_size_mb: float = 1.0) -> None:
    """
    Validate that the request payload does not exceed the maximum size.
    
    Args:
        request: FastAPI request object
        max_size_mb: Maximum allowed payload size in megabytes
        
    Raises:
        HTTPException: If payload size exceeds the maximum allowed size
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    
    # Get content length from headers if available
    content_length = request.headers.get("content-length")
    
    if content_length and int(content_length) > max_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"Payload too large. Maximum allowed size is {max_size_mb} MB."
        )
        
    # If content length is not available, read and check the body
    body = await request.body()
    
    if sys.getsizeof(body) > max_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"Payload too large. Maximum allowed size is {max_size_mb} MB."
        )