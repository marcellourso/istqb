def test_create_and_get_note(client):
    # 1️⃣ Create
    create_response = client.post(
        "/notes",
        json={"title": "Nota 1", "content": "Contenuto prova"}
    )

    assert create_response.status_code == 201
    note_id = create_response.json()["id"]

    # 2️⃣ Read
    get_response = client.get(f"/notes/{note_id}")

    assert get_response.status_code == 200
    data = get_response.json()

    assert data["id"] == note_id
    assert data["title"] == "Nota 1"
    assert data["content"] == "Contenuto prova"

    # 3️⃣ Coerenza struttura
    assert "tasks" in data
    assert data["tasks"] == []
    assert data["latest_analysis"] is None

def test_create_note_missing_title_returns_422(client):
    r = client.post("/notes", json={"content": "Contenuto prova"})
    assert r.status_code == 422


def test_create_note_missing_content_returns_422(client):
    r = client.post("/notes", json={"title": "Nota senza contenuto"})
    assert r.status_code == 422


def test_create_note_wrong_type_returns_422(client):
    # title dovrebbe essere stringa, qui passiamo un numero
    r = client.post("/notes", json={"title": 123, "content": "x"})
    assert r.status_code == 422

def test_create_note_empty_strings_behavior(client):
    r = client.post("/notes", json={"title": "", "content": ""})
    # Qui dipende dal tuo schema Pydantic: se non hai vincoli, potrebbe essere 201.
    # Se vuoi imporre il vincolo, allora questo test deve aspettare 422 e poi devi cambiare schema.
    assert r.status_code in (201, 422)