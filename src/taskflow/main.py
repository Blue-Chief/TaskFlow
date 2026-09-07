from typing import Annotated
from enum import Enum
from fastapi import FastAPI, Body, Query, Path
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

app = FastAPI()

tasks_db = [
    {"id": 1, "title": "Learn FastAPI", "status": "in_progress", "priority": "high"},
    {"id": 2, "title": "Setup PostgreSQL", "status": "todo", "priority": "medium"},
    {"id": 3, "title": "Write Tests", "status": "completed", "priority": "low"},
]

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

next_id = 4

@app.get("/")
def home():
    return {"message" : "Welcome to TaskFlow"}

@app.get("/health/")
def health_status():
    return {"status" : "Healthy"}

@app.get("/tasks")
def list_task(
    status: Annotated[TaskStatus | None, Query()] = None,
    priority: Annotated[str | None, Query()] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    results = tasks_db
    if status is not None:
        results = [t for t in results if t.get("status") == status]
    if priority is not None:
        results = [t for t in results if t.get("priority") == priority]
    return results[skip: skip + limit]

@app.get("/tasks/{task_id}")
def read_task(task_id : Annotated[int, Path(gt=0)]):
    task_lookup = {task["id"]: task for task in tasks_db} 
    return task_lookup.get(task_id, None)

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    global next_id
    new_task = {"id": next_id, "title": task.title, "description": task.description}
    tasks_db.append(new_task)
    next_id += 1
    return new_task