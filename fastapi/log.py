from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Pydantic model
class User(BaseModel):
    username: str
    password: str

# Environment variable fetcher
def get_env_variable(name: str, default=None, required=False):
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"Environment variable '{name}' is required but not set.")
    return value

# Database connection
def get_connection():
    host = get_env_variable("DB_HOST", "localhost")
    user = get_env_variable("DB_USER", required=True)
    password = get_env_variable("DB_PASSWORD", required=True)
    database = get_env_variable("DB_NAME", "fastapi")
    port = int(get_env_variable("DB_PORT", "3306"))

    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
        cursorclass=pymysql.cursors.DictCursor
    )

# Serve frontend
@app.get("/", response_class=HTMLResponse)
def serve_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Get all users (with password for demo)
@app.get("/users")
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, username, password FROM new")
        users = cursor.fetchall()
        return users
    finally:
        cursor.close()
        conn.close()

# Create user
@app.post("/users")
def create_user(user: User):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO new (username, password) VALUES (%s, %s)", (user.username, user.password))
        conn.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {e}")
    finally:
        cursor.close()
        conn.close()

# Update user
@app.put("/users/{id}")
def update_user(id: int, user: User):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE new SET username=%s, password=%s WHERE id=%s", (user.username, user.password, id))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {e}")
    finally:
        cursor.close()
        conn.close()

# Delete user
@app.delete("/users/{id}")
def delete_user(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM new WHERE id=%s", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {e}")
    finally:
        cursor.close()
        conn.close()