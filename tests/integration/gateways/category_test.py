import pytest

from app import create_app
from gateways.category import CategoryGateway
from heart.core.extensions import db


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session


def test_create_category(session):
    category = CategoryGateway.create(name="Test Category")
    assert category.id is not None
    assert category.name == "Test Category"


def test_get_category_by_id(session):
    category = CategoryGateway.create(name="Test Category")
    retrieved_category = CategoryGateway.get_by_id(category.id)
    assert retrieved_category is not None
    assert retrieved_category.name == "Test Category"


def test_get_all_categories(session):
    CategoryGateway.create(name="Test Category 1")
    CategoryGateway.create(name="Test Category 2")
    categories = CategoryGateway.get_all()
    assert len(categories) == 12


def test_get_category_by_name(session):
    CategoryGateway.create(name="Unique Category")
    category = CategoryGateway.get_by_name("Unique Category")
    assert category is not None
    assert category.name == "Unique Category"


def test_update_category(session):
    category = CategoryGateway.create(name="Old Category Name")
    updated_category = CategoryGateway.update(category.id, name="Updated Category Name")
    assert updated_category is not None
    assert updated_category.name == "Updated Category Name"


def test_delete_category(session):
    category = CategoryGateway.create(name="Category to Delete")
    CategoryGateway.delete(category.id)
    retrieved_category = CategoryGateway.get_by_id(category.id)
    assert retrieved_category is None
