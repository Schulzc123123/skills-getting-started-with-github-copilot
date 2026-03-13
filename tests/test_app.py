import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # 9 activities
    # Check structure
    chess_club = data.get("Chess Club")
    assert chess_club is not None
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_success():
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    # Verify added
    response = client.get("/activities")
    data = response.json()
    assert "test@mergington.edu" in data["Chess Club"]["participants"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Programming Class/signup?email=duplicate@mergington.edu")
    # Second should fail
    response = client.post("/activities/Programming Class/signup?email=duplicate@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # Signup first
    client.post("/activities/Gym Class/signup?email=unregister@mergington.edu")
    # Then unregister
    response = client.delete("/activities/Gym Class/signup?email=unregister@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    # Verify removed
    response = client.get("/activities")
    data = response.json()
    assert "unregister@mergington.edu" not in data["Gym Class"]["participants"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Art Club/signup?email=notsigned@mergington.edu")
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]

def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent Activity/signup?email=test@mergington.edu")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]