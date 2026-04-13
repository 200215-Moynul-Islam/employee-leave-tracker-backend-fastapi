# Employee Leave Tracker

Employee Leave Tracker is a FastAPI-based backend for managing employees and their leave requests.
It supports role-based access for admins and employees, JWT authentication, soft deletion, and approval workflows for leave requests.

## Features

- JWT-based authentication
- Admin and employee role separation
- Employee leave request creation
- Employee soft deletion of their own pending leave requests
- Admin approval and rejection of leave requests
- Admin view of all active leave requests with employee details
- Employee view of their own active leave requests
- Soft deletion for users and leave requests
- Alembic-based database migrations

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- JWT

## Project Structure

```text
app/
  constants/      # enums, roles, messages, validation rules
  core/           # configuration and exception handling
  db/             # database session and dependency providers
  dependencies.py # auth and role dependencies
  models/         # SQLAlchemy models
  repositories/   # database access layer
  routers/        # API route definitions
  schemas/        # request/response models
  services/       # business logic
  utils/          # password hashing and JWT helpers
migrations/       # Alembic migration environment
scripts/          # utility scripts such as admin seeding
```

## Roles

- `admin`
  Can create employees, update users, deactivate users, review all leave requests, and approve or reject leave requests.

- `employee`
  Can log in, create leave requests, delete their own pending leave requests, update their password, and view their own active leave requests.

## Data Model

### User

- `id`
- `email`
- `name`
- `role`
- `password_hash`
- `is_deleted`

### LeaveRequest

- `id`
- `start_date`
- `end_date`
- `created_at`
- `status`
- `user_id`
- `is_deleted`

## Leave Request Statuses

- `pending`
- `approved`
- `rejected`

## Environment Variables

Create a `.env` file based on `.env.example`.

```env
DATABASE_URL="postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DB_NAME"
DEFAULT_ADMIN_EMAIL="admin@example.com"
DEFAULT_ADMIN_PASSWORD="change-this-in-real-environments"
DEFAULT_ADMIN_NAME="System Administrator"
JWT_SECRET_KEY="replace-with-a-strong-random-secret"
```

Optional:

```env
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Installation

1. Create a virtual environment.
2. Install dependencies.

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Database Setup

Run migrations:

```powershell
alembic upgrade head
```

Seed the default admin:

```powershell
python scripts\seed_admin.py
```

## Running the Application

```powershell
uvicorn app.main:app --reload
```

Application URLs:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/health`

## Authentication

Authenticate with:

- `POST /auth/login`

The API returns a bearer token. Pass it in the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

## API Overview

### Authentication

- `POST /auth/login`

### Users

- `POST /users`
  Admin only. Create a new employee.

- `GET /users/employees`
  Admin only. Get all active employees.

- `GET /users/me/leave-requests`
  Authenticated user only. Get the current user with that user’s active leave requests.

- `PATCH /users/{user_id}`
  Admin only. Update user name and/or email.

- `DELETE /users/{user_id}`
  Admin only. Soft-delete a user.

- `PATCH /users/me/password`
  Authenticated user only. Update the current user’s password.

### Leave Requests

- `GET /leave-requests`
  Admin only. Get all active leave requests with employee details.

- `POST /leave-requests/me`
  Employee only. Create a leave request.

- `DELETE /leave-requests/me/{leave_request_id}`
  Employee only. Soft-delete a leave request if it belongs to the current user and is still pending.

- `PATCH /leave-requests/{leave_request_id}/approve`
  Admin only. Approve a pending leave request.

- `PATCH /leave-requests/{leave_request_id}/reject`
  Admin only. Reject a pending leave request.

## Business Rules

- Only admins can create employees.
- New users created through the API are employees.
- A user can only view their own leave requests through `/users/me/leave-requests`.
- A user can only delete their own leave request.
- A leave request can only be deleted, approved, or rejected while its status is `pending`.
- Deletion is soft deletion through `is_deleted = true`.
- Inactive users and deleted leave requests are excluded from active queries.

## Notes

- The application uses a consistent `ApiResponse[T]` wrapper for responses.
- Request validation and business exceptions are handled centrally.
- Passwords are stored as hashes, not plain text.
- SQLAlchemy async sessions are used throughout the app.
