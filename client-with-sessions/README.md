# Notes API - Session Version (Backend Only)

A secure Flask REST API with session-based authentication.

## Description
This is a standalone backend implementation for the Notes productivity app. It uses Flask sessions for user authentication and provides full CRUD capabilities for notes.

## How Session Authentication Works

### The Authentication Flow

1. **User Registration (`/signup`)**
   - User sends `username` and `password` in JSON body
   - Server hashes the password using Flask-Bcrypt (never stores plain text)
   - Server creates a new User record in database
   - Server creates a session for the user
   - Server sets a `session` cookie in the response

2. **User Login (`/login`)**
   - User sends `username` and `password`
   - Server verifies credentials against database
   - Server creates a session storing `user_id`
   - Server sets a `session` cookie

3. **Session Management**
   - Flask stores session data server-side (signed with SECRET_KEY)
   - Browser automatically sends cookie with each request
   - Server validates the signed cookie
   - If valid, server looks up user from `session['user_id']`
   - `request.current_user` is set for protected routes

4. **Check Session (`/check_session`)**
   - Returns user info if session is active
   - Returns empty if no valid session

5. **Logout (`/logout`)**
   - Clears the session data
   - Cookie becomes invalid
   - User must login again to access protected routes

### Why Sessions?

- **Stateful**: Server stores session data
- **Secure**: Session cookie is cryptographically signed
- **Easy**: Browser handles cookie automatically
- **Simple logout**: Just clear server-side session

### Session vs JWT

| Feature | Session | JWT |
|---------|---------|-----|
| Storage | Server-side | None (stateless) |
| Logout | Clear session | Client discards token |
| Scalability | Needs shared storage | Works anywhere |
| Cookie | Auto-handled | Manual (Bearer header) |

## Architecture

### Models

**User Model:**
- `id` (Integer, Primary Key)
- `username` (String, Unique, Required)
- `email` (String, Unique, Optional)
- `password_hash` (String, Bcrypt hashed)
- `created_at` (DateTime)

**Note Model:**
- `id` (Integer, Primary Key)
- `title` (String, Required)
- `content` (Text, Required)
- `user_id` (Foreign Key → User)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Security Features
- Passwords hashed with Flask-Bcrypt
- Session cookie signed with SECRET_KEY
- `HttpOnly` and `SameSite` cookie flags
- Protected routes require active session
- User can only access their own notes

## Required Fields
- `username` - Required, must be unique
- `password` - Required, minimum 6 characters

## Installation (Python 3.14)
1. Navigate to folder:
   ```bash
   cd client-with-sessions
   ```
2. Activate virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. Seed database (optional):
   ```bash
   python seed.py
   ```

## Run Instructions
```bash
python run.py
```
Server runs on `http://localhost:5556`

## API Endpoints

### Authentication
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/signup` | No | Register and start session |
| POST | `/login` | No | Login and start session |
| GET | `/check_session` | No* | Check if session active |
| DELETE | `/logout` | No | End session |

### Notes Resource
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/notes` | Yes | Get own notes (paginated) |
| POST | `/notes` | Yes | Create new note |
| GET | `/notes/<id>` | Yes | Get specific note |
| PATCH | `/notes/<id>` | Yes | Update note |
| DELETE | `/notes/<id>` | Yes | Delete note |

### Pagination
```
GET /notes?page=1&per_page=10
```
Returns: `notes[]`, `total`, `page`, `per_page`, `pages`

## Testing with Postman

1. **Signup/Login**: POST to `/login` with username/password
2. **Postman automatically handles cookies**
3. **Make requests** to protected endpoints
4. **Logout**: DELETE to `/logout`

## Test Users (after seeding)
- All test users have password: `password123`
- 3 users created with 5 notes each