from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Task
from app.schemas import TaskOut, TaskToggle

logger = logging.getLogger("app.tasks")

router = APIRouter(prefix="", tags=["tasks"])


@router.patch("/tasks/{task_id}", response_model=TaskOut)
def toggle_task(task_id: int, payload: TaskToggle, db: Annotated[Session, Depends(get_db)]):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.done = payload.done
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
