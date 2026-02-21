import os
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import get_db, Base



# 1️⃣ Crea un database temporaneo SQLite per i test
@pytest.fixture(scope="session")
def test_engine():
    # crea un file temporaneo per il DB
    fd, path = tempfile.mkstemp()
    os.close(fd)

    print("Test DB path:", path)

    engine = create_engine(
        f"sqlite:///{path}",
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(bind=engine)

    yield engine

    # cleanup finale
    os.remove(path)


# 2️⃣ Crea una sessione DB per ogni test
@pytest.fixture(scope="function")
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )
    session = TestingSessionLocal()

    yield session

    session.close()


# 3️⃣ Override della dependency get_db di FastAPI
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()