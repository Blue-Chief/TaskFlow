from typing import Annotated
from fastapi import FastAPI, Body, Query, Path
from pydantic import BaseModel, Field

app = FastAPI()

task_db = [
    {"id": 1, "title": "Learn FastAPI"},
    {"id": 2, "title": "Setup PostgreSQL"},
    {"id": 3, "title": "Write Tests"},
]

@app.get("/")
def home():
    return {"message" : "Welcome to TaskFlow"}

@app.get("/health/")
def health_status():
    return {"status" : "Healthy"}

@app.get("/tasks")
def list_task(
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return task_db[skip: skip + limit]

@app.get("/tasks/{task_id}")
def read_task(task_id : Annotated[int, Path(gt=0)]):
    task_lookup = {task["id"]: task for task in task_db} 
    return task_lookup.get(task_id, None)
    