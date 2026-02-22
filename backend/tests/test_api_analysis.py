def test_analyze_rules_creates_latest_analysis(client):
    # Create note with markers
    r_note = client.post(
        "/notes",
        json={
            "title": "N2",
            "content": "TODO: chiamare cliente\n- preparare demo\nIMPORTANTE",
        },
    )
    assert r_note.status_code == 201
    note_id = r_note.json()["id"]

    # Analyze rules
    r_an = client.post(f"/notes/{note_id}/analyze", params={"mode": "rules"})
    assert r_an.status_code == 201
    an = r_an.json()

    assert an["mode"] == "rules"
    assert an["priority"] in ("low", "medium", "high")
    assert "tasks" in an
    assert "chiamare cliente" in an["tasks"]
    assert "preparare demo" in an["tasks"]

    # GET note should expose latest_analysis
    r_get = client.get(f"/notes/{note_id}")
    assert r_get.status_code == 200
    data = r_get.json()
    assert data["latest_analysis"] is not None
    assert data["latest_analysis"]["mode"] == "rules"

def test_analyze_ai_returns_501(client):
    r_note = client.post("/notes", json={"title": "N3", "content": "x"})
    note_id = r_note.json()["id"]

    r = client.post(f"/notes/{note_id}/analyze", params={"mode": "ai"})
    assert r.status_code == 501

def test_analyze_note_not_found_returns_404(client):
    r = client.post("/notes/999999/analyze", params={"mode": "rules"})
    assert r.status_code == 404