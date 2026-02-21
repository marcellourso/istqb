def test_create_note(client):
    response = client.post(
        "/notes",
        json={"title": "Test", "content": "Contenuto"}
    )

    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Test"
    assert data["content"] == "Contenuto"
    assert "id" in data