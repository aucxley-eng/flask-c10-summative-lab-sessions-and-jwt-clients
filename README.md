# Flask Notes API

A secure Flask REST API with API key-based authentication for a notes productivity application.

## Description

This backend provides user authentication and CRUD operations for personal notes. Users can register, login, and manage their own notes. Each user can only access their own notes.

## Architecture

The project follows a layered architecture:
- **Repositories**: Database operations (UserRepository, NoteRepository)
- **Services**: Business logic (AuthService, NoteService)
- **API Routes**: Request handlers (auth, notes)
- **Responses**: Standardized API responses
- **Utils**: Custom decorators for authentication

## Auth Method

API Key-based authentication (not JWT or sessions).

## Installation

1. Install dependencies:
```bash
pipenv install
```

2. Initialize the database:
```bash
pipenv run flask db init
pipenv run flask db migrate
pipenv run flask db upgrade
```

3. Seed the database with sample data:
```bash
pipenv run python seed.py
```

## Run Instructions

```bash
pipenv run python app.py
```

The server will run on `http://localhost:5555`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login with email and password |
| GET | `/api/auth/me` | Get current authenticated user |
| POST | `/api/auth/refresh-key` | Generate new API key |

### Notes (Protected Routes)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notes` | Get all notes (paginated) |
| POST | `/api/notes` | Create a new note |
| GET | `/api/notes/<id>` | Get a specific note |
| PATCH | `/api/notes/<id>` | Update a note |
| DELETE | `/api/notes/<id>` | Delete a note |

## Authentication Flow

### Register
```
POST /api/auth/register
Body: {
    'username': 'string',
    'email': 'string',
    'password': 'string'
}
Response: {
    'user': {...},
    'api_key': 'string'
}
```

### Login
```
POST /api/auth/login
Body: {
    'email': 'string',
    'password': 'string'
}
Response: {
    'api_key': 'string',
    'user': {...}
}
```

### Using the API Key
For all protected endpoints, include the API key in the header:
- **Header Key**: `X-API-Key`
- **Header Value**: Your API key

### Get Notes (with pagination)
```
GET /api/notes?page=1&per_page=10
Headers: X-API-Key: <your_api_key>
```

### Create Note
```
POST /api/notes
Headers: X-API-Key: <your_api_key>
Body: {
    'title': 'string',
    'content': 'string'
}
```