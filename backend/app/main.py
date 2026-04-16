import mysql.connector
import jwt
print(jwt.__file__)
print(hasattr(jwt, "encode"))
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

SECRET_KEY = "rahul_secret_key"

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------
# DATABASE CONNECTION
# ----------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="jaysingh@89",
        database="task_management_db"
    )


# ----------------------------
# MODELS
# ----------------------------
class RegisterUser(BaseModel):
    name: str
    email: str
    password: str


class LoginUser(BaseModel):
    email: str
    password: str


class Task(BaseModel):
    title: str
    description: str


# ----------------------------
# JWT VERIFY
# ----------------------------
def verify_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


# ----------------------------
# ROOT
# ----------------------------
@app.get("/")
def read_root():
    return {"message": "Backend running successfully"}


# ----------------------------
# REGISTER
# ----------------------------
@app.post("/register")
def register(user: RegisterUser):
    try:
        db = get_db()
        cursor = db.cursor()

        query = """
        INSERT INTO users (name, email, password, role)
        VALUES (%s, %s, %s, %s)
        """

        values = (
            user.name,
            user.email,
            user.password,
            "user"
        )

        cursor.execute(query, values)
        db.commit()

        return {"message": "User registered successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ----------------------------
# LOGIN
# ----------------------------
@app.post("/login")
def login(user: LoginUser):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (user.email,)
        )

        db_user = cursor.fetchone()

        if not db_user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        if str(db_user["password"]).strip() != str(user.password).strip():
            raise HTTPException(
                status_code=401,
                detail="Invalid password"
            )

        token = jwt.encode(
            {
                "user_id": int(db_user["id"]),
                "email": db_user["email"],
                "exp": datetime.utcnow() + timedelta(hours=2)
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return {
            "message": "Login successful",
            "token": token
        }

    except Exception as e:
        print("LOGIN ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# ----------------------------
# CREATE TASK
# ----------------------------
@app.post("/tasks")
def create_task(
    task: Task,
    user=Depends(verify_token)
):
    db = get_db()
    cursor = db.cursor()

    query = """
    INSERT INTO tasks (title, description, user_id)
    VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (
            task.title,
            task.description,
            user["user_id"]
        )
    )

    db.commit()

    return {"message": "Task created successfully"}


# ----------------------------
# GET TASKS
# ----------------------------
@app.get("/tasks")
def get_tasks(user=Depends(verify_token)):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM tasks WHERE user_id=%s",
        (user["user_id"],)
    )

    tasks = cursor.fetchall()

    return tasks


# ----------------------------
# DELETE TASK
# ----------------------------
@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    user=Depends(verify_token)
):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=%s",
        (task_id,)
    )

    db.commit()

    return {"message": "Task deleted successfully"}


# ----------------------------
# UPDATE TASK
# ----------------------------
@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task: Task,
    user=Depends(verify_token)
):
    db = get_db()
    cursor = db.cursor()

    query = """
    UPDATE tasks
    SET title=%s, description=%s
    WHERE id=%s
    """

    cursor.execute(
        query,
        (
            task.title,
            task.description,
            task_id
        )
    )

    db.commit()

    return {"message": "Task updated successfully"}

    db.commit()

    return {"message": "Task updated successfully"}