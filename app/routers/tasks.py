from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field

from ..schemas.task import TaskCreate, TaskOut, TaskPatch, TaskStatus, TaskUpdate
from ..core.security import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

tasks_db = [
    {"id": 1, "title": "Learn FastAPI", "description": "do it", "status": "in_progress", "priority": "high", "assigned_to": {"id":5, "username":"blue_chief"}},
    {"id": 2, "title": "Setup PostgreSQL", "description": "do it", "status": "todo", "priority": "medium"},
    {"id": 3, "title": "Write Tests", "description": "do it", "status": "completed", "priority": "low"},
]

next_id = 4

@router.get("", response_model=list[TaskOut])
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

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id : int, current_user: Annotated[dict, Depends(get_current_user)]):
    task_lookup = {task["id"]: task for task in tasks_db} 
    result = task_lookup.get(task_id, None)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@router.post("", response_model=TaskOut, status_code=201)
def create_task(task: TaskCreate):
    global next_id
    new_task = {"id": next_id, "title": task.title, "description": task.description}
    tasks_db.append(new_task)
    next_id += 1
    return new_task

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate):
    task_lookup = {task["id"]: task for task in tasks_db}
    result = task_lookup.get(task_id, None)
    if result:
        result.update({"title": task.title})
        result.update({"description": task.description})
        return result
    else:
        raise HTTPException(status_code=404, detail="Task not Found")

@router.patch("/{task_id}", response_model=TaskOut)
def patch_task(task_id: int, patch: TaskPatch):
    task_lookup = {task["id"]: task for task in tasks_db}
    result = task_lookup.get(task_id, None)
    if result:
        update_data = patch.model_dump(exclude_unset=True)
        result.update(update_data)
        return result
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, t in enumerate(tasks_db):
        if t["id"] == task_id:
            tasks_db.pop(i)
            return
    raise HTTPException(status_code=404, detail="Task not found")