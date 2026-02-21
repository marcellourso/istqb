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