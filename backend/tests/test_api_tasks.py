def test_create_task_and_toggle(client):
    # 1️⃣ Creo una nota
    create_note = client.post(
        "/notes",
        json={"title": "Nota con task", "content": "Contenuto"}
    )
    assert create_note.status_code == 201
    note_id = create_note.json()["id"]

    # 2️⃣ Creo un task per la nota
    create_task = client.post(
        f"/notes/{note_id}/tasks",
        json={"description": "Comprare latte"}
    )
    assert create_task.status_code == 201

    task_data = create_task.json()
    task_id = task_data["id"]

    assert task_data["description"] == "Comprare latte"
    assert task_data["done"] is False

    # 3️⃣ Toggle task
    toggle = client.patch(
        f"/tasks/{task_id}",
        json={"done": True}
    )
    assert toggle.status_code == 200
    assert toggle.json()["done"] is True

    # 4️⃣ Verifico persistenza via GET note
    get_note = client.get(f"/notes/{note_id}")
    data = get_note.json()

    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["done"] is True

def test_toggle_task_non_existing_returns_404(client):
    r = client.patch("/tasks/999999", json={"done": True})
    assert r.status_code == 404