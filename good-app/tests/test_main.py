import pytest
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_echo_returns_message(client):
    response = client.post("/echo", json={"message": "hello"})
    assert response.status_code == 200
    assert response.get_json() == {"message": "hello"}


def test_echo_rejects_missing_body(client):
    response = client.post("/echo", json={})
    assert response.status_code == 400
