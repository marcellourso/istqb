from __future__ import annotations

import re


def extract_tasks(text: str) -> list[str]:
    tasks: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("-"):
            value = stripped[1:].strip()
            if value:
                tasks.append(value)
            continue
        if stripped.upper().startswith("TODO:"):
            value = stripped[5:].strip()
            if value:
                tasks.append(value)
    return tasks


def compute_priority(text: str) -> str:
    upper = text.upper()
    if "URGENTE" in upper or "ASAP" in upper:
        return "high"
    if "IMPORTANTE" in upper:
        return "medium"
    return "low"


_sentence_split = re.compile(r"(?<=[.!?])\s+")


def compute_summary(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return ""
    parts = _sentence_split.split(stripped, maxsplit=1)
    if parts and parts[0]:
        first = parts[0].strip()
        if first:
            return first[:180]
    return stripped[:180]
