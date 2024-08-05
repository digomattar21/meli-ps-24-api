import pytest

from app import create_app
from heart.core.extensions import db


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_create_severity(client):
    client.delete("/severity/1")
    severity_delete = client.get("/severity/1")
    assert severity_delete.status_code == 400
    response = client.post("/severity", json={"level": 1})
    assert response.status_code == 200
    severity_id = response.json["severity_id"]
    assert isinstance(severity_id, int)


def test_get_severity(client):
    response = client.get("/severity")
    assert response.status_code == 200
    assert len(response.json["severities"]) > 0


def test_get_severity_by_id(client):
    response = client.get("/severity/2")
    assert response.status_code == 200


def test_update_severity(client):
    res = client.delete("/severity/4")
    res = client.delete("/severity/1")
    assert res.status_code == 200
    create_severity = client.post("/severity", json={"level": 1})
    assert create_severity.status_code == 200
    id = create_severity.json["severity_id"]
    response = client.patch(f"/severity/{id}", json={"level": 4})
    assert response.status_code == 200
    assert response.json["severity"]["level"] == 4
