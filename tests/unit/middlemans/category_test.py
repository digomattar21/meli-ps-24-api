from unittest.mock import MagicMock

import pytest

from middlemans.category import validate_category_fields, verify_category_get


@pytest.fixture
def mock_controller():
    controller = MagicMock()
    controller.send_json = MagicMock()
    controller.get_json_body = MagicMock()
    return controller


def test_verify_category_get(mock_controller):
    next_func = MagicMock()
    decorated_func = verify_category_get(next_func)

    # Call the decorator with a category_id
    decorated_func(mock_controller, category_id=1)
    next_func.assert_called_once_with(mock_controller, category_id=1)

    # Call the decorator without a category_id
    decorated_func(mock_controller)
    next_func.assert_called_with(mock_controller)


def test_validate_category_fields():
    # Test with valid data
    data = {"name": "Test Category"}
    errors = validate_category_fields(data)
    assert errors == []

    # Test with invalid data type
    data = {"name": 123}
    errors = validate_category_fields(data)
    assert len(errors) == 1
    assert "name is expected to be of type str" in errors[0]
