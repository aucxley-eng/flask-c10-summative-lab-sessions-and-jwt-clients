# Flask Notes API

A secure Flask REST API with dual authentication support (Sessions and JWT) for a notes productivity application.

## Description

This backend provides user authentication and CRUD operations for personal notes. It is designed to work seamlessly with both the `client-with-sessions` and `client-with-jwt` React frontends. Users can register, login, and manage their own notes securely.

## Architecture

The project follows a layered architecture:
- **Repositories**: Database operations (UserRepository, NoteRepository)
- **Services**: Business logic (AuthService, NoteService)
- **API Routes**: Request handlers (auth, notes)
- **Responses**: Standardized API responses
- **Utils**: Custom decorators for authentication (supports both Sessions and JWT)

## Auth Method

The API supports two authentication methods simultaneously:
1. **Session-based authentication**: Uses Flask sessions (cookies).
2. **JWT-based authentication**: Uses Bearer tokens in the `Authorization` header.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

3. Seed the database:
```bash
python seed.py
```

## Run Instructions

```bash
python run.py
```

The server will run on `http://localhost:5555`

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Type |
|--------|----------|-------------|-----------|
| POST | `/signup` | Register a new user | Public |
| POST | `/login` | Login with username and password | Public |
| GET | `/check_session` | Check if user is logged in (Sessions) | Session |
| GET | `/me` | Get current user (JWT) | JWT |
| DELETE | `/logout` | Logout current user | Session |

### Notes (Protected Routes)

All notes endpoints require either a valid session or a valid JWT Bearer token.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes` | Get all notes for the current user (paginated) |
| POST | `/notes` | Create a new note |
| GET | `/notes/<id>` | Get a specific note owned by the user |
| PATCH | `/notes/<id>` | Update a note owned by the user |
| DELETE | `/notes/<id>` | Delete a note owned by the user |

## Pagination

The `GET /notes` endpoint supports pagination via query parameters:
- `page`: The page number (default: 1)
- `per_page`: Number of items per page (default: 10)

Example: `GET /notes?page=1&per_page=5`

## Database Seeding

To populate the database with sample data, run:
```bash
python seed.py
```
This will create 3 sample users and 5 notes for each user.
