from unittest.mock import MagicMock, patch

import pytest

from app import create_app
from gateways.category import CategoryGateway
from gateways.severity import SeverityGateway
from gateways.ticket import TicketGateway
from gateways.user import UserGateway
from services.ticket import TicketService
from utils.apiMessages import LocalApiCode, error_message


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def app_context(app):
    with app.app_context():
        yield


@pytest.fixture
def ticket_data():
    return {
        "id": 1,
        "title": "Test Ticket",
        "description": "This is a test ticket",
        "category_id": 1,
        "subcategory_id": 1,
        "severity_id": 2,
    }


def test_get_all_tickets(app_context, ticket_data):
    with patch.object(
        TicketGateway, "get_all", return_value=[MagicMock(to_dict=lambda: ticket_data)]
    ):
        result = TicketService.get_all_tickets()
        assert result == {"tickets": [ticket_data]}

    with patch.object(TicketGateway, "get_all", return_value=[]):
        result = TicketService.get_all_tickets()
        expected_error = {"errors": [error_message(LocalApiCode.ticketNotFound)]}
        assert result == expected_error


def test_get_ticket_by_id(app_context, ticket_data):
    with patch.object(
        TicketGateway, "get_by_id", return_value=MagicMock(to_dict=lambda: ticket_data)
    ):
        result = TicketService.get_ticket_by_id(1)
        assert result == {"ticket": ticket_data}

    with patch.object(TicketGateway, "get_by_id", return_value=None):
        result = TicketService.get_ticket_by_id(10)
        expected_error = {"errors": [error_message(LocalApiCode.ticketNotFound)]}
        assert result == expected_error


def test_create_ticket(app_context, ticket_data):
    # Mock the database operations and other gateways
    with patch.object(
        CategoryGateway,
        "get_by_id",
        side_effect=[MagicMock(id=1), MagicMock(id=1, parent_id=1)],
    ), patch.object(
        SeverityGateway, "get_by_id", return_value=MagicMock(level=2, id=2)
    ), patch.object(
        UserGateway, "get_all_users", return_value=[{"id": 1}]
    ), patch.object(
        TicketGateway, "get_by_user_id", return_value=[]
    ), patch.object(
        TicketGateway, "create", return_value=MagicMock(to_dict=lambda: ticket_data)
    ):

        result = TicketService.create_ticket(
            "Test Ticket", "This is a test ticket", 1, 1, 2
        )
        assert result == {"ticket": ticket_data}

    # Case when the subcategory is invalid
    with patch.object(
        CategoryGateway,
        "get_by_id",
        side_effect=[MagicMock(id=1), MagicMock(id=2, parent_id=2)],
    ):
        result = TicketService.create_ticket(
            "Test Ticket", "This is a test ticket", 1, 2, 2
        )
        expected_error = {"errors": [error_message(LocalApiCode.isNotSubcategory)]}
        assert result == expected_error


def test_update_ticket(app_context, ticket_data):
    with patch.object(
        TicketGateway, "get_by_id", return_value=MagicMock(subcategory_id=1)
    ), patch.object(
        CategoryGateway, "get_by_id", return_value=MagicMock(id=1)
    ), patch.object(
        SeverityGateway, "get_by_id", return_value=MagicMock(level=2, id=2)
    ), patch.object(
        TicketGateway, "update", return_value=MagicMock(to_dict=lambda: ticket_data)
    ):
        result = TicketService.update_ticket(1, title="Updated Ticket")
        assert result == {"ticket": ticket_data}

    with patch.object(TicketGateway, "get_by_id", return_value=None):
        result = TicketService.update_ticket(10, title="Updated Ticket")
        expected_error = {"errors": [error_message(LocalApiCode.ticketNotFound)]}
        assert result == expected_error


def test_delete_ticket(app_context, ticket_data):
    with patch.object(
        TicketGateway, "get_by_id", return_value=MagicMock()
    ), patch.object(TicketGateway, "delete", return_value=None):
        result = TicketService.delete_ticket(1)
        assert result == {"message": "Ticket deleted successfully"}

    with patch.object(TicketGateway, "get_by_id", return_value=None):
        result = TicketService.delete_ticket(10)
        expected_error = {"errors": [error_message(LocalApiCode.ticketNotFound)]}
        assert result == expected_error
