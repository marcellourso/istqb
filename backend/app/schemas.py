from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class NoteOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TaskCreate(BaseModel):
    description: str = Field(min_length=1, max_length=500)


class TaskOut(BaseModel):
    id: int
    note_id: int
    description: str
    done: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TaskToggle(BaseModel):
    done: bool


AnalysisMode = Literal["rules", "ai"]


class AnalysisOut(BaseModel):
    id: int
    note_id: int
    mode: AnalysisMode
    provider: Optional[str] = None
    latency_ms: Optional[int] = None
    raw_response: Optional[str] = None
    summary: str
    priority: Literal["low", "medium", "high"]
    created_at: datetime

    model_config = {"from_attributes": True}
