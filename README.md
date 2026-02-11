# FastAPI CRUD DB Auth

Repo: [https://github.com/iceyisaak/fastapi-crud-db-auth](https://github.com/iceyisaak/fastapi-crud-db-auth)


This is an experiemental project.

A modern, production-ready FastAPI application implementing CRUD operations with database integration and JWT authentication.

The project demonstrates:

- Full CRUD Operations
- Postgresql DB Connection
- Alembic DB Migrations
- SQL Relationships
  - One-to-Many / Many-to-One
  - Many-to-Many
- JWT Authentication
- The use of different layers:
    - models
    - schemas
    - services
    - routes


## To be added:
  
  - Middlewares
  - Custom Errors
  - User verification via Email
  - Password Reset


## Features

- 🚀 **FastAPI Framework** - High-performance, async Python web framework
- 🔐 **JWT Authentication** - Secure token-based authentication system
- 💾 **Database Integration** - SQLAlchemy ORM for database operations
- ✨ **CRUD Operations** - Complete Create, Read, Update, Delete functionality
- 📝 **Pydantic Schemas** - Type-safe request/response validation
- 🔧 **Modern Tooling** - Uses `uv` for fast, reliable dependency management
- 📚 **Auto-generated API Docs** - Interactive Swagger UI and ReDoc

## Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip
- Postgresql 16 or later

## Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/iceyisaak/fastapi-crud-db-auth.git
cd fastapi-crud-db-auth

# Install dependencies
uv sync

# Run the application
uv run main.py
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/iceyisaak/fastapi-crud-db-auth.git
cd fastapi-crud-db-auth

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload
```

## Environment Setup

Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
DATABASE_URL=sqlite:///./app.db  # Or your preferred database URL

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
DEBUG=True
```

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Project Structure

# FastAPI CRUD Database Authentication Project Structure

This is a well-organized FastAPI application following a **modular, feature-based architecture** with authentication, database operations, and API endpoints for managing books and reviews.

## High-Level Architecture

The project uses a **layered architecture** with clear separation of concerns:
- **Routes Layer**: HTTP endpoints and request handling
- **Services Layer**: Business logic
- **Models Layer**: Database schema definitions
- **Schemas Layer**: Data validation and serialization (Pydantic)

## Directory Breakdown

### `/src/auth/` - Authentication Module
Core authentication and authorization functionality:
- **`models.py`**: User database model (SQLAlchemy ORM)
- **`routes.py`**: Auth endpoints (login, register, refresh tokens)
- **`schemas.py`**: Request/response validation (Pydantic models)
- **`services.py`**: Auth business logic (user creation, token generation)
- **`dependencies.py`**: FastAPI dependency injection (e.g., `get_current_user`)
- **`utils.py`**: Helper functions (password hashing, JWT utilities)

### `/src/book/` - Books Module
CRUD operations for books:
- **`models.py`**: Book database model
- **`routes.py`**: Book API endpoints (GET, POST, PUT, DELETE)
- **`schemas.py`**: Book request/response validation
- **`services.py`**: Book business logic (queries, updates)

### `/src/reviews/` - Reviews Module
Review management functionality:
- **`models.py`**: Review database model (likely linked to books/users)
- **`routes.py`**: Review API endpoints
- **`schemas.py`**: Review validation schemas
- **`services.py`**: Review business logic

### `/src/db/` - Database Configuration
Database connection and session management:
- **`main.py`**: Database initialization, session factory (SQLAlchemy engine/session)
- **`redis.py`**: Redis connection setup (likely for caching or session storage)

### Root `/src/` Files
Cross-cutting concerns:
- **`config.py`**: Application configuration (environment variables, settings)
- **`email.py`**: Email service (password reset, notifications)
- **`errors.py`**: Custom exception handlers
- **`middlewares.py`**: Custom middleware (CORS, logging, error handling)

### `/main.py` (Root)
Application entry point that:
- Creates the FastAPI app instance
- Registers all route modules
- Applies middleware
- Configures startup/shutdown events

## Design Patterns

**Modular Feature Organization**: Each feature (auth, books, reviews) is self-contained with its own routes, models, schemas, and services.

**Dependency Injection**: The `dependencies.py` pattern allows reusable authentication and authorization checks across routes.

**Separation of Concerns**: Clear boundaries between routing, business logic, and data access layers.

**Schema Validation**: Pydantic schemas ensure type safety and automatic API documentation.

This structure scales well, makes testing easier, and keeps related code grouped together.



## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token
- `POST /auth/refresh` - Refresh access token

### CRUD Operations

- `GET /items` - List all items
- `GET /items/{id}` - Get specific item
- `POST /items` - Create new item (requires authentication)
- `PUT /items/{id}` - Update item (requires authentication)
- `DELETE /items/{id}` - Delete item (requires authentication)

## Usage Examples

### Register a New User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

### Create Item (Authenticated)

```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "My Item",
    "description": "Item description"
  }'
```

## Development

### Running Tests

```bash
# Using uv
uv run pytest

# Using pip
pytest
```

### Code Formatting

```bash
# Format code
uv run black .

# Check linting
uv run ruff check .
```

## Technologies Used

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - SQL toolkit and ORM
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation using Python type hints
- **[python-jose](https://python-jose.readthedocs.io/)** - JWT implementation
- **[passlib](https://passlib.readthedocs.io/)** - Password hashing
- **[uvicorn](https://www.uvicorn.org/)** - ASGI server
- **[uv](https://github.com/astral-sh/uv)** - Fast Python package installer

## Security

- Passwords are hashed using bcrypt
- JWT tokens for stateless authentication
- Environment variables for sensitive configuration
- CORS middleware for cross-origin requests
- Input validation using Pydantic models

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Inspired by modern API development best practices
- Thanks to the Python community for excellent tools and libraries

## Contact

Project Link: [https://github.com/iceyisaak/fastapi-crud-db-auth](https://github.com/iceyisaak/fastapi-crud-db-auth)

---

Made with ❤️ using FastAPI

