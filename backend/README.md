# Backend (FastAPI)

Backend API for the Task Management project.

## Stack

- FastAPI
- Pydantic
- MySQL (mysql-connector-python)
- JWT auth (PyJWT)

## Location

- Main API file: app/main.py
- Python dependencies: requirements.txt

## Prerequisites

- Python 3.10+
- MySQL 8+
- Existing database: task_management_db

## Install Dependencies

From project root:

```bash
pip install -r backend/requirements.txt
pip install mysql-connector-python PyJWT
```

Note:
- The code imports mysql.connector and jwt directly.
- If these packages are missing, imports will fail.

## Run the API

Recommended from project root:

```bash
uvicorn main:app --reload
```

Alternative from backend/app:

```bash
uvicorn main:app --reload
```

API URL:
- http://127.0.0.1:8000

## Endpoints

- GET / : health check
- POST /register : register user
- POST /login : login and get JWT token
- POST /tasks : create task (requires Authorization header)
- GET /tasks : list tasks for logged-in user (requires Authorization header)
- DELETE /tasks/{task_id} : delete task (requires Authorization header)
- PUT /tasks/{task_id} : update task (requires Authorization header)

Authorization format:

```text
Authorization: Bearer <token>
```

## Database Setup

Database table schemas are in:
- ../database/schema/user_schema.py
- ../database/schema/table_tasks_schema.py

Create tables with:

```bash
python database/database_model.py
```

## Current Known Issues

- DB credentials and SECRET_KEY are hardcoded in app/main.py.
- Passwords are stored and compared as plain text.
- In delete endpoint, task_id is referenced but not declared in function parameters.
- requirements.txt does not currently include mysql-connector-python and PyJWT.

## Recommended Improvements

1. Move secrets and DB credentials to environment variables.
2. Hash passwords with passlib.
3. Fix delete endpoint signature to include task_id: int.
4. Add ownership checks for update/delete operations.
5. Pin and complete requirements.txt.
