# Notes API - JWT Version (Backend Only)

A secure Flask REST API with JWT (JSON Web Token) authentication.

## Description
This is a standalone backend implementation for the Notes productivity app. It uses `flask-jwt-extended` for secure authentication via Bearer tokens and provides full CRUD capabilities for notes.

## How JWT Authentication Works

### The Authentication Flow

1. **User Registration (`/signup`)**
   - User sends `username` and `password` in JSON body
   - Server hashes the password using Flask-Bcrypt (never stores plain text)
   - Server creates a new User record in database
   - Server generates a JWT token containing user's ID
   - Server returns the token to the client

2. **User Login (`/login`)**
   - User sends `username` and `password` 
   - Server verifies credentials against database
   - Server generates a new JWT token (different each time)
   - Token contains: `sub` (user ID), `iat` (issued at), `exp` (expiry), `jti` (unique ID)
   - Server returns token in response

3. **Making Authenticated Requests**
   - Client includes the token in the `Authorization` header:
     ```
     Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
     ```
   - Server validates the token signature and expiration on every protected route
   - If valid, server extracts user ID and loads the user
   - Request proceeds with `request.current_user` set

4. **Token Verification**
   - JWT is stateless - server validates using cryptographic signature
   - Each login creates a unique token (includes timestamp)
   - No server-side session storage needed
   - Token expires after set time (configured in JWTManager)

### Why JWT?

- **Stateless**: No server-side session storage needed
- **Scalable**: Works across multiple servers
- **Mobile-friendly**: Easy to store in mobile apps
- **Each login creates new token**: Security feature allowing token invalidation

### Logout in JWT
JWT is stateless, so "logout" is handled client-side:
- Client discards the token
- For proper logout, server can maintain a token blacklist (not implemented in this version)

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
- Passwords hashed with Flask-Bcrypt ( salted hashing)
- JWT signed with secret key
- Protected routes require valid JWT
- User can only access their own notes (enforced in repository)

## Required Fields
- `username` - Required, must be unique
- `password` - Required, minimum 6 characters

## Installation (Python 3.14)
1. Navigate to folder:
   ```bash
   cd client-with-jwt
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
Server runs on `http://localhost:5555`

## API Endpoints

### Authentication
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/signup` | No | Register user, returns JWT |
| POST | `/login` | No | Login, returns JWT |
| GET | `/me` | JWT | Get current user info |

### Notes Resource
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/notes` | JWT | Get own notes (paginated) |
| POST | `/notes` | JWT | Create new note |
| GET | `/notes/<id>` | JWT | Get specific note |
| PATCH | `/notes/<id>` | JWT | Update note |
| DELETE | `/notes/<id>` | JWT | Delete note |

### Pagination
```
GET /notes?page=1&per_page=10
```
Returns: `notes[]`, `total`, `page`, `per_page`, `pages`

## Testing with Postman

1. **Signup/Login**: POST to `/login` with username/password
2. **Copy token** from response JSON
3. **Add Authorization header**: `Bearer <token>`
4. **Make requests** to protected endpoints

## Test Users (after seeding)
- All test users have password: `password123`
- 3 users created with 5 notes each