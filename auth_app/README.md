# FastAPI Authentication Service

JWT-based auth API with PostgreSQL (via SQLAlchemy + `psycopg` v3 driver).

## Endpoints

| Method | Path            | Auth required | Description                          |
|--------|-----------------|----------------|--------------------------------------|
| POST   | `/register`     | No             | Create a new user                    |
| POST   | `/login`        | No             | Get a JWT access token (OAuth2 form) |
| GET    | `/users/me`     | Yes            | Get the current logged-in user       |
| GET    | `/users/{id}`   | Yes            | Get a user by ID                     |
| GET    | `/users`        | Yes            | List users (paginated)               |
| GET    | `/health`       | No             | Health check                         |

## Setup

1. **Start Postgres** (or point `DATABASE_URL` at an existing instance):
   ```bash
   docker compose up -d
   ```

2. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # edit .env: set DATABASE_URL and a strong SECRET_KEY
   ```

4. **Run the app** (tables are auto-created on startup):
   ```bash
   uvicorn app.main:app --reload
   ```

5. Open interactive docs at `http://localhost:8000/docs`.

## Usage examples

**Register:**
```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","username":"jane","password":"supersecret123"}'
```

**Login** (form-encoded, `username` field accepts email or username):
```bash
curl -X POST http://localhost:8000/login \
  -d "username=jane@example.com&password=supersecret123"
```
Response:
```json
{"access_token": "eyJ...", "token_type": "bearer"}
```

**Get current user:**
```bash
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer eyJ..."
```

**Get user by ID:**
```bash
curl http://localhost:8000/users/1 \
  -H "Authorization: Bearer eyJ..."
```

**List users:**
```bash
curl "http://localhost:8000/users?skip=0&limit=50" \
  -H "Authorization: Bearer eyJ..."
```

## Notes

- Passwords are hashed with bcrypt (`passlib`).
- Tokens are signed JWTs (`python-jose`), default expiry 60 minutes (`ACCESS_TOKEN_EXPIRE_MINUTES`).
- `Base.metadata.create_all()` is used for simplicity here. For production, switch to **Alembic** migrations (already included in requirements.txt) instead of auto-create.
- All `/users*` routes require a valid bearer token — adjust `get_current_active_user` dependencies if you want some routes public or want to restrict `/users` listing to superusers only.
