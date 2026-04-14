# Flask Notes API

A secure Flask REST API with session-based authentication for a notes productivity application.

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

Session-based authentication (Flask sessions).

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

3. Seed the database (optional):
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

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup` | Register a new user |
| POST | `/login` | Login with username and password |
| GET | `/check_session` | Check if user is logged in |
| DELETE | `/logout` | Logout current user |

### Notes (Protected Routes)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notes` | Get all notes (paginated) |
| POST | `/notes` | Create a new note |
| GET | `/notes/<id>` | Get a specific note |
| PATCH | `/notes/<id>` | Update a note |
| DELETE | `/notes/<id>` | Delete a note |

## Authentication Flow

The frontend expects session-based authentication:

### Register
```
POST /signup
Body: {
    'username': 'string',
    'password': 'string',
    'password_confirmation': 'string'
}
Response: {
    'user': {'id': 1, 'username': 'string'}
}
```

### Login
```
POST /login
Body: {
    'username': 'string',
    'password': 'string'
}
Response: {
    'user': {'id': 1, 'username': 'string'}
}
```

### Check Session
```
GET /check_session
Response (logged in): {'id': 1, 'username': 'string'}
Response (not logged in): {}
```

### Logout
```
DELETE /logout
Response: {}
```

### Get Notes (with pagination)
```
GET /notes?page=1&per_page=10
```

### Create Note
```
POST /notes
Body: {
    'title': 'string',
    'content': 'string'
}
```