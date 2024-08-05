import pytest

from app import create_app
from heart.core.extensions import db
from utils.apiMessages import LocalApiCode, error_message

from ..bodies import invalid_category_bodies


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


def test_create_category(client):
    response = client.post("/category", json={"name": "Test Category", "parent_id": 1})
    assert response.status_code == 200
    category_id = response.json["category_id"]
    assert isinstance(category_id, int)


def test_create_category_with_invalid_data(client):
    for body, expected_error in invalid_category_bodies:
        response = client.post("/category", json=body)
        if response.json != expected_error:
            print(body)
            print(response.json, expected_error)
        assert response.status_code == 400
        assert response.json == expected_error


def test_get_category(client):
    response = client.get("/category")
    assert response.status_code == 200
    assert len(response.json["categories"]) > 0


def test_get_category_by_id(client):
    response = client.get("/category/1")
    assert response.status_code == 200


def test_update_category(client):
    response = client.patch("/category/8", json={"name": "Teste2", "parent_id": 2})
    assert response.status_code == 200
    assert response.json["category"]["name"] == "Teste2"


def test_update_category_errors(client):
    # Case with non existing parent id
    response = client.patch("/category/1", json={"parent_id": 100})
    assert response.status_code == 400
    assert response.json["errors"] == [
        error_message(LocalApiCode.invalidParentCategory)
    ]

    # Case with invalid parent_id
    response2 = client.patch("/category/1", json={"parent_id": "teste"})
    assert response2.status_code == 400
    assert response2.json["errors"] == [
        error_message(LocalApiCode.invalidParentCategory)
    ]

    # Case with invalid category name
    response3 = client.patch("/category/1", json={"name": ""})
    assert response3.status_code == 400
    assert response3.json["errors"] == [error_message(LocalApiCode.invalidCategoryName)]
