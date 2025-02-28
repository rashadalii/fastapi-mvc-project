# FastAPI MVC Application

A RESTful API built with FastAPI following the MVC design pattern. This application demonstrates user authentication, post management, and implements various best practices including field validation, dependency injection, and caching.

## Features

- **MVC Architecture**: Clear separation of Models, Views (via Schemas), and Controllers
- **Authentication**: JWT-based token authentication
- **Database**: MySQL with SQLAlchemy ORM
- **Validation**: Pydantic models with extensive type validation
- **Caching**: In-memory caching for improved performance
- **Dependency Injection**: Clean implementation of FastAPI dependencies

## Endpoints

### Authentication

- `POST /auth/signup`: Register a new user
- `POST /auth/login`: Authenticate and get a token

### Posts

- `POST /posts/add`: Create a new post (authenticated)
- `GET /posts/`: Get all posts for authenticated user (cached)
- `DELETE /posts/delete`: Delete a post (authenticated)

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── controllers/       # Handles routing and request/response
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic models for validation
│   ├── services/          # Business logic layer
│   ├── utils/             # Utility functions
│   ├── dependencies/      # FastAPI dependencies
│   ├── config.py          # Application configuration
├── requirements.txt
├── README.md
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your MySQL database and update the connection string in `app/config.py` or use environment variables.

4. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

5. Access the API documentation:
   ```
   http://localhost:8000/docs
   ```

## Authentication Flow

1. Register a user via `/auth/signup` endpoint
2. Login via `/auth/login` endpoint to get a token
3. Use the token in the Authorization header for protected endpoints:
   ```
   Authorization: Bearer <your-token>
   ```

## Requirements Checklist

- [x] MVC design pattern
- [x] MySQL database with SQLAlchemy ORM
- [x] Field validation with Pydantic models
- [x] Dependency injection
- [x] Token-based authentication
- [x] Request validation (payload size limitation)
- [x] In-memory caching
- [x] Comprehensive documentation and comments
