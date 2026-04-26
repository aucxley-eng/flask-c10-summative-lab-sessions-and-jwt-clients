# Notes API - JWT Version (Backend Only)

A secure Flask REST API with JWT (JSON Web Token) authentication.

## Description
This is a standalone backend implementation for the Notes productivity app. It uses `flask-jwt-extended` for secure authentication via Bearer tokens and provides full CRUD capabilities for notes.

## Architecture
- **Models**: User (Auth), Note (Resource)
- **Security**: Flask-Bcrypt for password hashing
- **Auth**: JWT (Bearer Tokens)
- **Resource**: User-owned notes with pagination

## Installation (Python 3.14)
1. Install dependencies:
   ```bash
   cd client-with-jwt
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
The server will run on `http://localhost:5555`.

## API Endpoints
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/signup` | No | Register a new user (returns JWT) |
| POST | `/login` | No | Login (returns JWT) |
| GET | `/me` | JWT | Get current user |
| GET | `/notes` | JWT | Get own notes (paginated) |
| POST | `/notes` | JWT | Create a new note |
| GET | `/notes/<id>` | JWT | View specific note |
| PATCH | `/notes/<id>` | JWT | Update specific note |
| DELETE | `/notes/<id>` | JWT | Delete specific note |

Pagination: `/notes?page=1&per_page=10`

## Test Users (after seeding)
- Password for all test users: `password123`
