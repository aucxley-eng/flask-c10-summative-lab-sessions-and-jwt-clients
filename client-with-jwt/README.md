# Notes API - JWT Version (Backend Only)

A secure Flask REST API with JWT (JSON Web Token) authentication.

## Description
This is a standalone backend implementation for the Notes productivity app. It uses `flask-jwt-extended` for secure authentication via Bearer tokens and provides full CRUD capabilities for notes.

## Architecture
- **Models**: User (Auth), Note (Resource)
- **Security**: Flask-Bcrypt for password hashing
- **Auth**: JWT (Bearer Tokens)
- **Resource**: User-owned notes with pagination

## Setup Instructions (Python 3.14)
1. Navigate to this folder:
   ```bash
   cd client-with-jwt
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
| POST | `/signup` | Register a new user (returns JWT) |
| POST | `/login` | Login (returns JWT) |
| GET | `/me` | Get current user via JWT |
| GET | `/notes` | Get own notes (paginated) |
| POST | `/notes` | Create a new note |
| GET | `/notes/<id>` | View specific note |
| PATCH | `/notes/<id>` | Update specific note |
| DELETE | `/notes/<id>` | Delete specific note |
