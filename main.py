from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import auth_controller, post_controller
from app.models.database import Base, engine

# Create tables in database
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="FastAPI MVC Application",
    description="A RESTful API with FastAPI using MVC design pattern",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handler for application exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for the application.
    
    Args:
        request: FastAPI request object
        exc: Exception raised
        
    Returns:
        JSONResponse: Error response
    """
    status_code = 500
    detail = str(exc)
    
    # Return JSON response with error details
    return JSONResponse(
        status_code=status_code,
        content={"detail": detail}
    )

# Include routers
app.include_router(auth_controller.router)
app.include_router(post_controller.router)

@app.get("/")
async def root():
    """
    Root endpoint for the API.
    
    Returns:
        dict: API information
    """
    return {
        "message": "Welcome to the FastAPI MVC Application API",
        "documentation": "/docs",
        "version": "1.0.0"
    }

# Run the application with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)