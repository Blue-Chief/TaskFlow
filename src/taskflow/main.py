from typing import Annotated
from fastapi import FastAPI, Body, Query, Path
from pydantic import BaseModel, Field

app = FastAPI()

task_db = [
    {"id": 1, "title": "Learn FastAPI"},
    {"id": 2, "title": "Setup PostgreSQL"},
    {"id": 3, "title": "Write Tests"},
    {"id": 10, "title": "Become an Expert Backend Dev"}
]

@app.get("/")
async def home():
    return {"message" : "Welcome to TaskFlow"}

@app.get("/health/")
async def health_status():
    return {"status" : "Healthy"}

@app.get("/tasks/{task_id}")
async def read_task(task_id : Annotated[int, Path(gt=0)]):
    task_lookup = {task["id"]: task for task in task_db} 
    return task_lookup.get(task_id, None)
    