import pytest
from app import create_app
from heart.core.extensions import db
from models.category import Category

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def session(app):
    with app.app_context():
        yield db.session

def test_create_category(session):
    category = Category(name="Test Category")
    session.add(category)
    session.commit()

    assert category.id is not None
    assert category.name == "Test Category"

def test_update_category(session):
    category = Category(name="Test Category")
    session.add(category)
    session.commit()

    category.name = "Updated Category"
    session.commit()

    updated_category = Category.query.get(category.id)
    assert updated_category.name == "Updated Category"

def test_delete_category(session):
    category = Category(name="Test Category")
    session.add(category)
    session.commit()

    session.delete(category)
    session.commit()

    deleted_category = Category.query.get(category.id)
    assert deleted_category is None

def test_category_relationship(session):
    parent_category = Category(name="Parent Category")
    child_category = Category(name="Child Category", parent=parent_category)
    session.add(parent_category)
    session.add(child_category)
    session.commit()

    retrieved_child = Category.query.get(child_category.id)
    assert retrieved_child.parent.name == "Parent Category"
