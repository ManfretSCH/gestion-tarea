from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from app.schemas import TaskCreate, TaskUpdate, TaskResponse
from app.database import get_db
from app.models import Task

router = APIRouter()

@router.get("/", status_code=200, response_model=list[TaskResponse])
def read_tasks(user_id: int, completed: Optional[bool] = None, db=Depends(get_db)):
    query = db.query(Task).filter(Task.user_id == user_id)
    if completed is not None:
        query = query.filter(Task.completed == completed)
    return query.all()


@router.get("/{task_id}", status_code=200, response_model=TaskResponse)
def read_task(user_id: int, task_id: int, db=Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", status_code=201, response_model=TaskResponse)
def create_task(user_id: int, task: TaskCreate, db=Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.patch("/{task_id}", status_code=200, response_model=TaskResponse)
def update_task(user_id: int, task_id: int, task_update: TaskUpdate, db=Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(user_id: int, task_id: int, db=Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()