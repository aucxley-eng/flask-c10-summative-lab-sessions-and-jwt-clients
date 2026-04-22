# Notes API - Session Version (Backend Only)

A secure Flask REST API with session-based authentication.

## Description
This is a standalone backend implementation for the Notes productivity app. It uses Flask sessions for user authentication and provides full CRUD capabilities for notes.

## Architecture
- **Models**: User (Auth), Note (Resource)
- **Security**: Flask-Bcrypt for password hashing
- **Auth**: Flask-Sessions
- **Resource**: User-owned notes with pagination

## Setup Instructions (Python 3.14)
1. Navigate to this folder:
   ```bash
   cd client-with-sessions
   ```
2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. Run the API:
   ```bash
   python3 run.py
   ```
   The server will run on `http://localhost:5555`.

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/signup` | Register a new user |
| POST | `/login` | Login and start session |
| GET | `/check_session` | Validate current session |
| DELETE | `/logout` | End session |
| GET | `/notes` | Get own notes (paginated) |
| POST | `/notes` | Create a new note |
| GET | `/notes/<id>` | View specific note |
| PATCH | `/notes/<id>` | Update specific note |
| DELETE | `/notes/<id>` | Delete specific note |
