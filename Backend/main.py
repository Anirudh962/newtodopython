from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from sqlite3 import Error

app = FastAPI()

# Database connection
DATABASE_URL = "sqlite:///todo.db"
database = Database(DATABASE_URL)

# CORS configuration
origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create table
@app.on_event("startup")
async def create_table():
    query = """
        CREATE TABLE IF NOT EXISTS todo (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER NOT NULL DEFAULT 0
        );
    """
    await database.execute(query)

# Get all todos
@app.get("/todos")
async def get_todos():
    query = "SELECT * FROM todo"
    results = await database.fetch_all(query)
    return {"todos": results}

# Get todo by id
@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    query = "SELECT * FROM todo WHERE id = :id"
    results = await database.fetch_one(query, {"id": todo_id})
    if not results:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"todo": results}

# Create todo
@app.post("/todos")
async def create_todo(todo: dict):
    query = "INSERT INTO todo (title, description, completed) VALUES (:title, :description, :completed)"
    await database.execute(query, {"title": todo["title"], "description": todo["description"], "completed": todo["completed"]})
    return {"todo": await database.fetch_one("SELECT * FROM todo WHERE id = (SELECT MAX(id) FROM todo)")}

# Update todo
@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo: dict):
    query = "UPDATE todo SET title = :title, description = :description, completed = :completed WHERE id = :id"
    await database.execute(query, {"title": todo["title"], "description": todo["description"], "completed": todo["completed"], "id": todo_id})
    return {"todo": await database.fetch_one("SELECT * FROM todo WHERE id = :id", {"id": todo_id})}

# Delete todo
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    query = "DELETE FROM todo WHERE id = :id"
    await database.execute(query, {"id": todo_id})
    return {"message": "Todo deleted successfully"}
