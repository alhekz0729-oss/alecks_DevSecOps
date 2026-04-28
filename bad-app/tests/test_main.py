import pytest
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_register_rejects_weak_password(client):
    # This test FAILS: The password "12345" has a digit but is < 8 chars
    # The buggy validation logic accepts it despite being weak
    response = client.post("/register", json={"username": "alice", "password": "12345"})
    assert response.status_code == 400
    assert "weak" in response.get_data(as_text=True).lower()


def test_register_accepts_strong_password(client):
    response = client.post("/register", json={"username": "alice", "password": "secure123"})
    assert response.status_code == 201
    assert response.get_json()["status"] == "registered"
