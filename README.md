# Notes API - Full Auth Flask Backend

A productivity app backend with two authentication implementations (JWT and Session).

## Project Overview

This project implements a secure RESTful API for a Notes productivity application with full CRUD capabilities. It demonstrates two different authentication strategies:

1. **JWT Implementation** - Stateless authentication using JSON Web Tokens
2. **Session Implementation** - Stateful authentication using Flask sessions

## How the Project Works

### Core Concept

This is a backend-only Flask API (no frontend). The main features are:

1. **User Authentication**: Users can register and login
2. **Secure Notes Management**: Each user can create, read, update, delete their own notes
3. **Protected Access**: Users cannot access other users' notes only
4. **Pagination**: Notes listing supports pagination

### The Data Flow

```
User → Request → Authentication Check → Business Logic → Database → Response
```

### Security Model

- **Passwords are never stored in plain text** - They're hashed using Flask-Bcrypt
- **Each user sees only their own data** - Enforced at repository level
- **Protected routes require authentication** - Verified via decorator

---

## JWT Authentication (How It Works)

### What is JWT?

JSON Web Token (JWT) is a compact, URL-safe token format for securely transmitting information between parties.

### The JWT Flow

1. **Signup/Login**:
   ```
   Client sends: {"username": "john", "password": "secret123"}
   Server verifies, then creates JWT containing: {"sub": user_id, "iat": timestamp, "exp": expiry}
   Server signs token with SECRET_KEY
   Server returns: {"token": "eyJhbGci...", "user": {...}}
   ```

2. **Making Authenticated Requests**:
   ```
   Client includes: Authorization: Bearer eyJhbGci...
   Server validates signature and expiry
   Server extracts user_id from token
   Server processes request with user context
   ```

3. **Token Contents**:
   - `sub`: User ID (subject)
   - `iat`: Issued at time
   - `exp`: Expiration time
   - `jti`: Unique token ID
   - `csr`f: Checksum for integrity

### Why JWT?

- ✅ Stateless - No server-side storage
- ✅ Scalable - Works across multiple servers
- ✅ Each login = New token - Security feature

---

## Session Authentication (How It Works)

### What are Sessions?

Sessions store user data server-side and identify users via a signed cookie.

### The Session Flow

1. **Signup/Login**:
   ```
   Client sends: {"username": "john", "password": "secret123"}
   Server verifies credentials
   Server creates session: session['user_id'] = user.id
   Server signs session with SECRET_KEY
   Server sends: Set-Cookie: session=signature.timestamp|encrypted_data
   ```

2. **Subsequent Requests**:
   ```
   Browser automatically sends cookie with request
   Server validates cookie signature
   Server loads user from session['user_id']
   Server processes request with user context
   ```

3. **Logout**:
   ```
   Client calls: DELETE /logout
   Server clears session data
   Cookie becomes invalid
   ```

### Why Sessions?

- ✅ Secure - Cookie is cryptographically signed
- ✅ Simple logout - Clear server session
- ✅ Browser handles automatically - No manual header needed

---

## Session vs JWT Comparison

| Feature | JWT | Sessions |
|---------|-----|----------|
| Storage | None (stateless) | Server-side |
| Logout | Client discards token | Server clears session |
| Scalability | Works anywhere | Needs shared storage |
| Cookie handling | Manual (Bearer header) | Automatic |
| Token per login | Different each time | Same until logout |

---

## Project Structure

```
client-with-jwt/
├── app/
│   ├── __init__.py       # App factory
│   ├── models.py         # User and Note models
│   ├── schemas.py        # Marshmallow schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth/routes.py    # /signup, /login, /me
│   │   └── notes/routes.py  # CRUD /notes
│   ├── services/
│   │   ├── auth_service.py
│   │   └── note_service.py
│   ├── repositories/
│   │   ├── base_repository.py
│   │   ├── user_repository.py
│   │   └── note_repository.py
│   ├── utils/
│   │   └── decorators.py # @require_auth
│   └── responses/
│       └── api_response.py
├── config.py             # Configuration
├── seed.py              # Database seeder
└── run.py              # Entry point

client-with-sessions/
├── (same structure)
└── run.py              # Port 5556
```

---

## API Endpoints

### Authentication (Both Versions)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/signup` | No | Register user |
| POST | `/login` | No | Login |
| GET | `/me` | JWT | Get current user (JWT only) |
| GET | `/check_session` | No* | Check session (Sessions only) |
| DELETE | `/logout` | No | Logout (Sessions only) |

### Notes CRUD

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/notes` | Yes | List notes (paginated) |
| POST | `/notes` | Yes | Create note |
| GET | `/notes/<id>` | Yes | Get note |
| PATCH | `/notes/<id>` | Yes | Update note |
| DELETE | `/notes/<id>` | Yes | Delete note |

### Pagination

```
GET /notes?page=1&per_page=10
```
Returns: `{notes: [], total: 15, page: 1, per_page: 10, pages: 2}`

---

## Installation & Running

### Prerequisites
- Python 3.14+

### JWT Version (Port 5555)

```bash
cd client-with-jwt
source .venv/bin/activate
python seed.py  # optional
python run.py
```

### Session Version (Port 5556)

```bash
cd client-with-sessions
source .venv/bin/activate
python seed.py  # optional
python run.py
```

### Test Users
After running `seed.py`:
- 3 users created
- Password for all: `password123`
- 15 notes (5 per user)

---

## Testing with Postman

### JWT Testing

1. POST `/login` with `{"username": "...", "password": "password123"}`
2. Copy `token` from response
3. In request Auth tab, select "Bearer Token"
4. Paste token and make requests

### Session Testing

1. POST `/login` with `{"username": "...", "password": "password123"}`
2. Postman automatically handles cookie
3. Make requests to protected endpoints
4. DELETE `/logout` to end session

---

## Security Features

1. **Password Hashing**: Flask-Bcrypt (salted, slow hashing)
2. **Session Signing**: SECRET_KEY (prevent tampering)
3. **JWT Signing**: Configured secret key
4. **Protected Routes**: `@require_auth` decorator
5. **Data Isolation**: Users can only query their own notes
6. **Input Validation**: Required fields checked

---

