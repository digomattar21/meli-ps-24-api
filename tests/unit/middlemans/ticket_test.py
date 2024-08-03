import pytest
from unittest.mock import MagicMock, patch
from middlemans.ticket import verifyTicketGet, verifyTicketDelete, verifyTicketPatch, verifyTicketPost, validateTicketFields
from gateways.category import CategoryGateway
from gateways.ticket import TicketGateway
from utils.apiMessages import errorMessage, LocalApiCode

@pytest.fixture
def mock_controller():
    controller = MagicMock()
    controller.sendJson = MagicMock()
    controller.getJsonBody = MagicMock()
    return controller

def test_verify_ticket_get(mock_controller):
    next_func = MagicMock()
    decorated_func = verifyTicketGet(next_func)

    # Call the decorator with a ticket_id
    decorated_func(mock_controller, ticket_id=1)
    next_func.assert_called_once_with(mock_controller, ticket_id=1)

    # Call the decorator without a ticket_id
    decorated_func(mock_controller)
    next_func.assert_called_with(mock_controller)

def test_verify_ticket_delete(mock_controller):
    next_func = MagicMock()
    decorated_func = verifyTicketDelete(next_func)

    # Test when ticket exists
    with patch.object(TicketGateway, "get_by_id", return_value=True):
        decorated_func(mock_controller, ticket_id=1)
        next_func.assert_called_once_with(mock_controller, ticket_id=1)

    # Test when ticket does not exist
    with patch.object(TicketGateway, "get_by_id", return_value=None):
        decorated_func(mock_controller, ticket_id=1)
        mock_controller.sendJson.assert_called_once_with({"errors": [errorMessage(LocalApiCode.ticketNotFound)]})

def test_validate_ticket_fields():
    # Test with valid data
    data = {"title": "Test Ticket", "description": "Test description"}
    errors = validateTicketFields(data)
    assert errors == []

    # Test with invalid data type
    data = {"title": 123}
    errors = validateTicketFields(data)
    assert len(errors) == 1
    assert "title is expected to be of type str" in errors[0]

