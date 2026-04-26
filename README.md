# Notes API - Dual Authentication Lab

This repository contains two separate implementations of a Flask-based Notes API, each demonstrating a different authentication strategy: **JWT (JSON Web Tokens)** and **Session-based Authentication**.

## Project Overview

The project is designed to help you understand the practical differences between stateless (JWT) and stateful (Session) authentication in a RESTful API.

### 1. JWT Implementation (`client-with-jwt`)
- **Port:** `5555`
- **Mechanism:** Stateless authentication using `Flask-JWT-Extended`.
- **Workflow:** The client sends credentials, the server returns a signed token, and the client sends this token in the `Authorization` header for every subsequent request.
- **Key Files:** 
    - `app/utils/decorators.py`: Validates the Bearer token.
    - `app/api/auth/routes.py`: Contains `/login`, `/signup`, and `/me`.

### 2. Session Implementation (`client-with-sessions`)
- **Port:** `5556`
- **Mechanism:** Stateful authentication using Flask's built-in session management.
- **Workflow:** The server stores user information in a session and sends a `session` cookie to the client. The browser/Postman automatically sends this cookie back with each request.
- **Key Files:**
    - `app/utils/decorators.py`: Checks for an active session.
    - `app/api/auth/routes.py`: Contains `/login`, `/signup`, `/check_session`, and `/logout`.

---

## Getting Started

### Prerequisites
- Python 3.14+
- `pip`

### Installation & Setup

Both projects come with isolated virtual environments (`.venv`) and seeded databases.

#### To run the JWT version:
```bash
cd client-with-jwt
source .venv/bin/activate
python run.py
```

#### To run the Session version:
```bash
cd client-with-sessions
source .venv/bin/activate
python run.py
```

*Note: You can run both simultaneously as they use different ports.*

---

## API Reference

### JWT Version (`localhost:5555`)
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/signup` | No | Register and get a token |
| POST | `/login` | No | Login and get a token |
| GET | `/me` | Yes (JWT) | Get current user info |
| GET | `/notes` | Yes (JWT) | List own notes |
| POST | `/notes` | Yes (JWT) | Create a note |

### Session Version (`localhost:5556`)
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/signup` | No | Register and start session |
| POST | `/login` | No | Login and start session |
| GET | `/check_session` | No* | Returns user if session is active |
| DELETE | `/logout` | No | End the session |
| GET | `/notes` | Yes (Session) | List own notes |

---

## Testing with Postman

### Testing JWT
1. Call `POST /login` with `{"username": "...", "password": "password123"}`.
2. Copy the `token` from the JSON response.
3. In your next request (e.g., `GET /notes`), go to the **Auth** tab in Postman.
4. Select **Bearer Token** and paste your token.

### Testing Sessions
1. Call `POST /login` with `{"username": "...", "password": "password123"}`.
2. Postman will automatically handle the cookie.
3. Simply call `GET /notes` or `GET /check_session`. No manual token handling is required.

---

## Database & Seeding
Both implementations use SQLite (`app.db`). Each has been seeded with:
- **3 Test Users** (Password: `password123`)
- **15 Notes** (Distributed across users)

To re-seed either database:
```bash
cd <folder_name>
source .venv/bin/activate
python seed.py
```
