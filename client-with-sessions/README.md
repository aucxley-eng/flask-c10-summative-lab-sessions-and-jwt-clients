# Notes API - Session Version (Backend Only)

A secure Flask REST API with session-based authentication.

## Description
This is a standalone backend implementation for the Notes productivity app. It uses Flask sessions for user authentication and provides full CRUD capabilities for notes.

## Architecture
- **Models**: User (Auth), Note (Resource)
- **Security**: Flask-Bcrypt for password hashing
- **Auth**: Flask-Sessions  
- **Resource**: User-owned notes with pagination

## Installation (Python 3.14)
1. Install dependencies:
   ```bash
   cd client-with-sessions
   source .venv/bin/activate
   pipenv install --skip-lock
   ```
   OR use the existing venv:
   ```bash
   source .venv/bin/activate
   ```

2. Seed the database (optional):
   ```bash
   python seed.py
   ```

## Run Instructions
```bash
python run.py
```
The server will run on `http://localhost:5556`.

## API Endpoints
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/signup` | No | Register a new user |
| POST | `/login` | No | Login and start session |
| GET | `/check_session` | No* | Validate current session |
| DELETE | `/logout` | No | End session |
| GET | `/notes` | Yes | Get own notes (paginated) |
| POST | `/notes` | Yes | Create a new note |
| GET | `/notes/<id>` | Yes | View specific note |
| PATCH | `/notes/<id>` | Yes | Update specific note |
| DELETE | `/notes/<id>` | Yes | Delete specific note |

Pagination: `/notes?page=1&per_page=10`

## Test Users (after seeding)
- Password for all test users: `password123`
