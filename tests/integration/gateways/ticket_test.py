import pytest

from app import create_app
from gateways.ticket import TicketGateway
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


def test_create_ticket(session):
    ticket = TicketGateway.create(
        title="Test Ticket",
        description="This is a test ticket",
        category_id=1,
        user_id=1,
        subcategory_id=2,
        severity_id=3,
    )
    assert ticket.id is not None
    assert ticket.title == "Test Ticket"
    assert ticket.category_id == 1


def test_get_ticket_by_id(session):
    ticket = TicketGateway.create(
        title="Test Ticket",
        description="This is a test ticket",
        category_id=1,
        user_id=1,
        subcategory_id=2,
        severity_id=3,
    )
    retrieved_ticket = TicketGateway.get_by_id(ticket.id)
    assert retrieved_ticket is not None
    assert retrieved_ticket.title == "Test Ticket"


def test_get_ticket_by_user_id(session):
    tickets = TicketGateway.get_by_user_id(1)
    assert len(tickets) > 0


def test_update_ticket(session):
    ticket = TicketGateway.create(
        title="Test Ticket",
        description="This is a test ticket",
        category_id=1,
        user_id=1,
        subcategory_id=2,
        severity_id=3,
    )
    updated_ticket = TicketGateway.update(ticket.id, title="Updated Title")
    assert updated_ticket is not None
    assert updated_ticket.title == "Updated Title"


def test_delete_ticket(session):
    ticket = TicketGateway.create(
        title="Test Ticket",
        description="This is a test ticket",
        category_id=1,
        user_id=1,
        subcategory_id=2,
        severity_id=3,
    )
    TicketGateway.delete(ticket.id)
    retrieved_ticket = TicketGateway.get_by_id(ticket.id)
    assert retrieved_ticket is None
