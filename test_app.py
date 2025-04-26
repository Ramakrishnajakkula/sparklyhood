import pytest
import os
import json
from app import app, db

@pytest.fixture(autouse=True)
def clear_db():
    # Clear incidents collection before each test
    db.incidents.delete_many({})
    yield
    db.incidents.delete_many({})

def test_get_incidents_empty():
    client = app.test_client()
    resp = client.get("/incidents")
    assert resp.status_code == 200
    assert resp.get_json() == []

def test_create_incident_success():
    client = app.test_client()
    data = {
        "title": "Test Incident",
        "description": "Test Description",
        "severity": "Medium"
    }
    resp = client.post("/incidents", json=data)
    assert resp.status_code == 201
    incident = resp.get_json()
    assert incident["title"] == data["title"]
    assert incident["description"] == data["description"]
    assert incident["severity"] == data["severity"]
    assert "id" in incident
    assert "reported_at" in incident

def test_create_incident_missing_fields():
    client = app.test_client()
    # Missing title
    data = {"description": "desc", "severity": "Low"}
    resp = client.post("/incidents", json=data)
    assert resp.status_code == 400
    # Missing description
    data = {"title": "t", "severity": "Low"}
    resp = client.post("/incidents", json=data)
    assert resp.status_code == 400
    # Missing severity
    data = {"title": "t", "description": "d"}
    resp = client.post("/incidents", json=data)
    assert resp.status_code == 400

def test_create_incident_invalid_severity():
    client = app.test_client()
    data = {
        "title": "t",
        "description": "d",
        "severity": "Critical"
    }
    resp = client.post("/incidents", json=data)
    assert resp.status_code == 400
    assert "Invalid severity" in resp.get_json()["error"]

def test_get_incident_by_id_success():
    client = app.test_client()
    data = {
        "title": "Incident",
        "description": "Desc",
        "severity": "High"
    }
    post_resp = client.post("/incidents", json=data)
    incident_id = post_resp.get_json()["id"]
    get_resp = client.get(f"/incidents/{incident_id}")
    assert get_resp.status_code == 200
    incident = get_resp.get_json()
    assert incident["id"] == incident_id

def test_get_incident_by_id_not_found():
    client = app.test_client()
    resp = client.get("/incidents/64b7f9f9f9f9f9f9f9f9f9f9")
    assert resp.status_code == 404
    assert "Incident not found" in resp.get_json()["error"]

def test_get_incident_by_id_invalid():
    client = app.test_client()
    resp = client.get("/incidents/invalidid")
    assert resp.status_code == 400
    assert "Invalid incident id" in resp.get_json()["error"]

def test_delete_incident_success():
    client = app.test_client()
    data = {
        "title": "Incident",
        "description": "Desc",
        "severity": "Low"
    }
    post_resp = client.post("/incidents", json=data)
    incident_id = post_resp.get_json()["id"]
    del_resp = client.delete(f"/incidents/{incident_id}")
    assert del_resp.status_code == 204
    # Confirm it's deleted
    get_resp = client.get(f"/incidents/{incident_id}")
    assert get_resp.status_code == 404

def test_delete_incident_not_found():
    client = app.test_client()
    resp = client.delete("/incidents/64b7f9f9f9f9f9f9f9f9f9f9")
    assert resp.status_code == 404
    assert "Incident not found" in resp.get_json()["error"]

def test_delete_incident_invalid_id():
    client = app.test_client()
    resp = client.delete("/incidents/invalidid")
    assert resp.status_code == 400
    assert "Invalid incident id" in resp.get_json()["error"]

def test_get_incidents_multiple():
    client = app.test_client()
    data1 = {"title": "A", "description": "D1", "severity": "Low"}
    data2 = {"title": "B", "description": "D2", "severity": "Medium"}
    client.post("/incidents", json=data1)
    client.post("/incidents", json=data2)
    resp = client.get("/incidents")
    assert resp.status_code == 200
    incidents = resp.get_json()
    assert len(incidents) == 2
    titles = {i["title"] for i in incidents}
    assert titles == {"A", "B"}

