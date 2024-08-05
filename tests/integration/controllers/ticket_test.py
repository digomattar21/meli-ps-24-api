import pytest

from app import create_app
from heart.core.extensions import db
from utils.apiMessages import LocalApiCode, error_message

from ..bodies import invalid_ticket_bodies


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


def test_create_ticket_invalid_cases(client):
    for body, expected_response in invalid_ticket_bodies:
        response = client.post("/ticket", json=body)
        assert response.status_code == 400
        assert response.json == expected_response


def test_create_ticket(client):
    response = client.post(
        "/ticket",
        json={
            "title": "Test Ticket",
            "description": "This is a test ticket",
            "severity_id": 2,
            "category_id": 1,
            "subcategory_id": 6,
        },
    )
    assert response.status_code == 200
    assert response.json["ticket"]["title"] == "Test Ticket"


def test_update_ticket(client):
    # Test successful update of a ticket
    response = client.patch(
        "/ticket/1",
        json={
            "title": "Test Ticket 2",
            "description": "This is a test ticket",
            "severity_id": 2,
            "category_id": 1,
            "subcategory_id": 7,
        },
    )
    assert response.status_code == 200
    assert response.json["ticket"]["title"] == "Test Ticket 2"

    # Test when category or subcategory doesn't exist
    response = client.patch(
        "/ticket/1",
        json={
            "category_id": 999,
            "subcategory_id": 999,
        },
    )
    assert response.status_code == 400
    assert "errors" in response.json
    assert (
        response.json["errors"][0]["code"] == "categoryNotFound"
        or response.json["errors"][0]["code"] == "invalidSubcategory"
        or response.json["errors"][0]["code"] == "subcategoryNotFound"
    )

    # Test updating with empty JSON body
    response = client.patch("/ticket/1", json={})
    assert response.status_code == 400
    assert response.json["errors"] == [error_message(LocalApiCode.emptyRequest)]

    # Test updating a ticket with some fields as None (should ignore None values)
    response = client.patch(
        "/ticket/1",
        json={
            "title": None,
            "description": "Updated description",
        },
    )
    assert response.status_code == 400
    assert response.json["errors"] == [error_message(LocalApiCode.invalidTitle)]

    # Test when subcategory is not a child of the given category
    response = client.patch(
        "/ticket/1",
        json={
            "category_id": 1,
            "subcategory_id": 10,
        },
    )
    assert response.status_code == 400
    assert "errors" in response.json
    assert response.json["errors"][0]["code"] == "isNotSubcategory"


def test_get_ticket(client):
    response = client.get("/ticket")
    assert response.status_code == 200
    assert len(response.json["tickets"]) > 0


def test_get_ticket_by_id(client):
    response = client.get("/ticket/1")
    assert response.status_code == 200
    assert response.json["ticket"]


def test_delete_ticket(client):
    response = client.delete("/ticket/1")
    assert response.status_code == 200
