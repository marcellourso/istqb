# Backend (FastAPI)

## Prerequisiti

- Python 3.11+

## Install

Da `backend/`:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
pip install -r requirements-dev.txt
```

## Run

Da `backend/`:

```bash
. .venv/bin/activate
uvicorn app.main:app --reload
```

Il DB SQLite viene creato automaticamente come `backend/app.db` al primo avvio.

## Test

Da `backend/`:

```bash
. .venv/bin/activate
pytest
```
