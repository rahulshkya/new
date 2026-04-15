# Project Internshala

Full-stack Task Management application with:
- FastAPI backend
- MySQL database
- React frontend (Create React App)

## Current Architecture

- Backend API: FastAPI app in backend/app/main.py
- Database bootstrap: MySQL table creation script in database/database_model.py
- Frontend client: React app in frontend/src/App.js
- Root launcher: main.py imports backend app for uvicorn startup from project root

## Tech Stack

- Backend: FastAPI, Pydantic, JWT, MySQL Connector
- Frontend: React, Axios, Tailwind tooling installed in project
- Database: MySQL

## Project Structure

```text
project_internshala/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   └── README.md
├── database/
│   ├── database_model.py
│   └── schema/
│       ├── user_schema.py
│       └── table_tasks_schema.py
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── README.md
├── main.py
└── README.md
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL 8+

## Backend Setup

1. Create and activate a Python virtual environment.
2. Install backend dependencies:

```bash
pip install -r backend/requirements.txt
pip install mysql-connector-python PyJWT
```

3. Create MySQL database:

```sql
CREATE DATABASE task_management_db;
```

4. Initialize tables:

```bash
python database/database_model.py
```

5. Run backend server from project root:

```bash
uvicorn main:app --reload
```

API base URL:
- http://127.0.0.1:8000

## Frontend Setup

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Start development server:

```bash
npm start
```

Frontend URL:
- http://localhost:3000

## API Endpoints

- GET / : Health check
- POST /register : Register user
- POST /login : Login and receive JWT token
- POST /tasks : Create task (auth required)
- GET /tasks : Get tasks for logged in user (auth required)
- DELETE /tasks/{task_id} : Delete task (auth required)
- PUT /tasks/{task_id} : Update task (auth required)

Authorization header format:

```text
Authorization: Bearer <token>
```

## Database Schema

users table:
- id (PK)
- name
- email (unique)
- password
- role (user/admin)
- created_at

tasks table:
- id (PK)
- title
- description
- status (pending/completed)
- user_id (FK -> users.id)
- created_at

## Important Notes (Current Code State)

- Backend currently has hardcoded DB credentials in source code.
- Passwords are being stored as plain text right now.
- In backend/app/main.py, delete task endpoint uses task_id but task_id is missing in function arguments.
- requirements.txt does not currently include mysql-connector-python and PyJWT, so they must be installed manually unless requirements are updated.

## Recommended Next Improvements

1. Move DB credentials and SECRET_KEY to environment variables.
2. Hash passwords using passlib before storing.
3. Fix delete endpoint signature to include task_id: int.
4. Add proper error handling and validation for task ownership checks.
5. Pin all backend dependencies in backend/requirements.txt.
