from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

if TYPE_CHECKING:
    from app.models import Analysis, Task


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=lambda: dt.datetime.now(dt.UTC), nullable=False)

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="note", cascade="all, delete-orphan")
    analyses: Mapped[list["Analysis"]] = relationship("Analysis", back_populates="note", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=lambda: dt.datetime.now(dt.UTC), nullable=False)

    note: Mapped[Note] = relationship("Note", back_populates="tasks")


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"), nullable=False, index=True)

    mode: Mapped[str] = mapped_column(String(20), nullable=False)
    provider: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    latency_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    raw_response: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    summary: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(10), nullable=False)

    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=lambda: dt.datetime.now(dt.UTC), nullable=False)

    note: Mapped[Note] = relationship("Note", back_populates="analyses")
