# Flask Notes API

A secure Flask REST API with session-based authentication for a notes productivity application.

## Description

This backend provides user authentication and CRUD operations for personal notes. Users can register, login, and manage their own notes. Each user can only access their own notes.

## Auth Method

Session-based authentication using Flask sessions.

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

## Request/Response Formats

### POST /signup
```json
Request: {"username": "string", "password": "string", "password_confirmation": "string"}
Response: {"id": 1, "username": "string"}
```

### POST /login
```json
Request: {"username": "string", "password": "string"}
Response: {"id": 1, "username": "string"}
```

### GET /check_session
```json
Response (logged in): {"id": 1, "username": "string"}
Response (not logged in): {}
```

### GET /notes (Pagination)
```
Query params: ?page=1&per_page=10
Response: {"notes": [...], "total": 50, "page": 1, "per_page": 10, "pages": 5}
```

### POST /notes
```json
Request: {"title": "string", "content": "string"}
Response: {"id": 1, "title": "string", "content": "string", "user_id": 1, ...}
```

### PATCH /notes/<id>
```json
Request: {"title": "string"} (partial update allowed)
Response: {"id": 1, "title": "string", "content": "string", ...}
```

### DELETE /notes/<id>
```json
Response: {}
```