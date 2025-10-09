# Task Fly API

A FastAPI application for flight reservation system based on the provided SQL schema, using **Pydantic v2** for modern data validation and serialization.

## Features

- **Usuario Management**: Create, read, update, and delete users with CPF validation
- **Voo Management**: Manage flights with search and filtering capabilities
- **Reserva Management**: Handle flight reservations with status tracking
- **Authentication**: JWT-based authentication system
- **Soft Deletes**: All entities support soft deletion
- **Data Validation**: Comprehensive input validation using Pydantic v2
- **Environment Configuration**: Centralized settings management with .env support
- **Python Enums**: Type-safe enums stored as text in PostgreSQL

## Quick Start

### 1. Environment Setup

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/task_fly_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
```

### 2. Install Dependencies

```bash
poetry install
```

### 3. Run the Application

**Development mode:**
```bash
python run_dev.py
```

**Or with uvicorn directly:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

## Pydantic v2 Features

### Modern Configuration
- Uses `ConfigDict` instead of deprecated `Config` class
- `model_validate()` method for object validation
- Enhanced type hints and validation

### Environment Management
```python
from app.config.settings import settings

# Access configuration values
database_url = settings.database_url
debug_mode = settings.debug
cors_origins = settings.cors_origins
```

### Enum Handling
Python enums are used for type safety while storing as text in PostgreSQL:

```python
# In Python code
tier = TierPassagem.EXECUTIVA
status = StatusReserva.ATIVA

# Stored in database as strings
"executiva", "ativa"
```

## Database Schema

The API is based on three main entities:

### Usuario (User)
- UUID primary key
- Full name, CPF (Brazilian tax ID), birth date
- Gender, phone, email
- Password hash and registration origin
- Soft delete support

### Voo (Flight)
- Auto-incrementing ID
- Flight number, origin/destination airports
- Departure date, airline company
- Ticket tier (economy, business, first class)
- Soft delete support

### Reserva (Reservation)
- String-based reservation ID
- References to User and Flight
- Reservation date and status
- Soft delete support

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/token` - Login and get access token
- `GET /auth/me` - Get current user info

### Usuarios
- `GET /usuarios/` - List all users
- `POST /usuarios/` - Create new user
- `GET /usuarios/{usuario_id}` - Get user by ID
- `GET /usuarios/email/{email}` - Get user by email
- `PUT /usuarios/{usuario_id}` - Update user
- `DELETE /usuarios/{usuario_id}` - Delete user (soft)

### Voos
- `GET /voos/` - List flights (with filters)
- `POST /voos/` - Create new flight
- `GET /voos/{voo_id}` - Get flight by ID
- `GET /voos/numero/{numero_voo}` - Get flight by number
- `PUT /voos/{voo_id}` - Update flight
- `DELETE /voos/{voo_id}` - Delete flight (soft)

### Reservas
- `GET /reservas/` - List reservations (with filters)
- `POST /reservas/` - Create new reservation
- `GET /reservas/{reserva_id}` - Get reservation by ID
- `GET /reservas/usuario/{usuario_id}` - Get user's reservations
- `PUT /reservas/{reserva_id}` - Update reservation
- `DELETE /reservas/{reserva_id}` - Delete reservation (soft)
- `POST /reservas/{reserva_id}/cancel` - Cancel reservation
- `POST /reservas/{reserva_id}/confirm` - Confirm reservation

## Setup

1. Install dependencies (SQLAlchemy, FastAPI, Pydantic, etc.)
2. Configure database connection in `app/config/database.py`
3. Set environment variables for `DATABASE_URL` and `SECRET_KEY`
4. Run the application

## Features Implemented from Tinto Example

- Structured project layout with models, schemas, routes, and config
- Database session management
- Password hashing and JWT authentication
- Comprehensive error handling
- Input validation with custom validators
- Relationship handling between entities
- CORS middleware configuration
- Health check endpoint

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key for token generation