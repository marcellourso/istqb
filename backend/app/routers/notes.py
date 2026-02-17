from __future__ import annotations

import logging
import time
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import analyzer
from app.db import get_db
from app.models import Analysis, Note, Task
from app.schemas import AnalysisMode, AnalysisOut, NoteCreate, NoteOut, TaskCreate, TaskOut

logger = logging.getLogger("app.notes")

router = APIRouter(prefix="", tags=["notes"])


@router.post("/notes", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate, db: Annotated[Session, Depends(get_db)]):
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.get("/notes", response_model=list[NoteOut])
def list_notes(db: Annotated[Session, Depends(get_db)]):
    return db.query(Note).order_by(Note.id.desc()).all()


@router.get("/notes/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: Annotated[Session, Depends(get_db)]):
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("/notes/{note_id}/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(note_id: int, payload: TaskCreate, db: Annotated[Session, Depends(get_db)]):
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    task = Task(note_id=note_id, description=payload.description, done=False)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.post("/notes/{note_id}/analyze", response_model=AnalysisOut, status_code=status.HTTP_201_CREATED)
def analyze_note(
    note_id: int,
    mode: Annotated[AnalysisMode, Query()],
    db: Annotated[Session, Depends(get_db)],
):
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if mode == "ai":
        raise HTTPException(status_code=501, detail="AI mode not implemented yet")

    start = time.perf_counter()
    tasks = analyzer.extract_tasks(note.content)
    priority = analyzer.compute_priority(note.content)
    summary = analyzer.compute_summary(note.content)
    latency_ms = int((time.perf_counter() - start) * 1000)

    analysis = Analysis(
        note_id=note_id,
        mode="rules",
        provider="rules",
        latency_ms=latency_ms,
        raw_response="\n".join(tasks) if tasks else None,
        summary=summary,
        priority=priority,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis
