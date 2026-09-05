from typing import Annotated
from fastapi import FastAPI, Body, Query, Path
from pydantic import BaseModel, Field

app = FastAPI()

tasks_db = [
    {"id": 1, "title": "Learn FastAPI", "status": "In Progress", "priority": "high"},
    {"id": 2, "title": "Setup PostgreSQL", "status": "Not started", "priority": "medium"},
    {"id": 3, "title": "Write Tests", "status": "completed", "priority": "low"},
]

@app.get("/")
def home():
    return {"message" : "Welcome to TaskFlow"}

@app.get("/health/")
def health_status():
    return {"status" : "Healthy"}

@app.get("/tasks")
def list_task(
    status: Annotated[str | None, Query()] = None,
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
    