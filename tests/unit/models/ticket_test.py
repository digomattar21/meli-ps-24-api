import pytest

from app import create_app
from heart.core.extensions import db
from models.category import Category
from models.ticket import Ticket


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


def test_create_ticket(session):
    category = Category(name="Test Category")
    session.add(category)
    session.commit()

    ticket = Ticket(
        title="Test Ticket",
        description="A test ticket",
        category_id=category.id,
        severity_id=2,
        user_id=1,
    )
    session.add(ticket)
    session.commit()

    assert ticket.id is not None
    assert ticket.title == "Test Ticket"
    assert ticket.category.name == "Test Category"
    assert ticket.severity.description == "High"
