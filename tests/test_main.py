
import pytest
from app.main import app


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_ruy_lopez(client):
    response = client.post(
        "/api/opening",
        json={"moves": "e4 e5 Nf3 Nc6 Bb5"},
    )

    assert response.status_code == 200
    assert response.json["opening"]["name"] == "Ruy Lopez"
    assert response.json["opening"]["eco"] == "C60"


def test_invalid_move(client):
    response = client.post(
        "/api/opening",
        json={"moves": "e4 e5 Nf3 Nf6 Bb5"},
    )

    assert response.status_code == 400


def test_missing_moves(client):
    response = client.post("/api/opening", json={})

    assert response.status_code == 400
