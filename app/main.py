from typing import Annotated
from enum import Enum
from fastapi import FastAPI, Body, Query, Path, HTTPException, Depends
from pydantic import BaseModel, Field

class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

app = FastAPI()

tasks_db = [
    {"id": 1, "title": "Learn FastAPI", "description": "do it", "status": "in_progress", "priority": "high", "assigned_to": {"id":5, "username":"blue_chief"}},
    {"id": 2, "title": "Setup PostgreSQL", "description": "do it", "status": "todo", "priority": "medium"},
    {"id": 3, "title": "Write Tests", "description": "do it", "status": "completed", "priority": "low"},
]

class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str | None = Field(default=None, max_length=2000)

next_id = 4

class User(BaseModel):
    id: int
    username: str

class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None 
    assigned_to: User | None = None

class TaskUpdate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str | None = Field(default=None, max_length=2000)

class TaskPatch(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    description: str | None = Field(default=None, max_length=2000)

def get_current_user() -> dict:
    return {"id":1, "username":"temp_user"}

@app.get("/")
def home():
    return {"message" : "Welcome to TaskFlow"}

@app.get("/health/")
def health_status():
    return {"status" : "Healthy"}

@app.get("/tasks", response_model=list[TaskOut])
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
    if results:
        return results[skip: skip + limit]
    else:
        raise HTTPException(status_code=404, detail="No Task found")

@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id : int, current_user: Annotated[dict, Depends(get_current_user)]):
    task_lookup = {task["id"]: task for task in tasks_db} 
    result = task_lookup.get(task_id, None)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate):
    global next_id
    new_task = {"id": next_id, "title": task.title, "description": task.description}
    tasks_db.append(new_task)
    next_id += 1
    return new_task

@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate):
    task_lookup = {task["id"]: task for task in tasks_db}
    result = task_lookup.get(task_id, None)
    if result:
        result.update({"title": task.title})
        result.update({"description": task.description})
        return result
    else:
        raise HTTPException(status_code=404, detail="Task not Found")

@app.patch("/tasks/{task_id}", response_model=TaskOut)
def patch_task(task_id: int, patch: TaskPatch):
    task_lookup = {task["id"]: task for task in tasks_db}
    result = task_lookup.get(task_id, None)
    if result:
        update_data = patch.model_dump(exclude_unset=True)
        result.update(update_data)
        return result
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, t in enumerate(tasks_db):
        if t["id"] == task_id:
            tasks_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")