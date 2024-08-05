from unittest.mock import MagicMock

import pytest

from middlemans.ticket import validate_ticket_fields, verify_ticket_get


@pytest.fixture
def mock_controller():
    controller = MagicMock()
    controller.send_json = MagicMock()
    controller.get_json_body = MagicMock()
    return controller


def test_verify_ticket_get(mock_controller):
    next_func = MagicMock()
    decorated_func = verify_ticket_get(next_func)

    # Call the decorator with a ticket_id
    decorated_func(mock_controller, ticket_id=1)
    next_func.assert_called_once_with(mock_controller, ticket_id=1)

    # Call the decorator without a ticket_id
    decorated_func(mock_controller)
    next_func.assert_called_with(mock_controller)


def test_validate_ticket_fields():
    # Test with valid data
    data = {"title": "Test Ticket", "description": "Test description"}
    errors = validate_ticket_fields(data)
    assert errors == []

    # Test with invalid data type
    data = {"title": 123}
    errors = validate_ticket_fields(data)
    assert len(errors) == 1
    assert "title is expected to be of type str" in errors[0]
