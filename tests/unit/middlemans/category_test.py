import pytest
from unittest.mock import MagicMock, patch
from gateways.category import CategoryGateway
from utils.apiMessages import errorMessage, LocalApiCode
from middlemans.category import verifyCategoryGet, verifyCategoryPatch, verifyCategoryPost, verifyCategoryDelete, validateCategoryFields

@pytest.fixture
def mock_controller():
    controller = MagicMock()
    controller.sendJson = MagicMock()
    controller.getJsonBody = MagicMock()
    return controller

def test_verify_category_get(mock_controller):
    next_func = MagicMock()
    decorated_func = verifyCategoryGet(next_func)

    # Call the decorator with a category_id
    decorated_func(mock_controller, category_id=1)
    next_func.assert_called_once_with(mock_controller, category_id=1)

    # Call the decorator without a category_id
    decorated_func(mock_controller)
    next_func.assert_called_with(mock_controller)

def test_verify_category_delete(mock_controller):
    next_func = MagicMock()
    decorated_func = verifyCategoryDelete(next_func)

    # Test when category exists
    with patch.object(CategoryGateway, "get_by_id", return_value=True):
        decorated_func(mock_controller, category_id=1)
        next_func.assert_called_once_with(mock_controller, category_id=1)

    # Test when category does not exist
    with patch.object(CategoryGateway, "get_by_id", return_value=None):
        decorated_func(mock_controller, category_id=1)
        mock_controller.sendJson.assert_called_once_with({"errors": [errorMessage(LocalApiCode.categoryNotFound)]})

def test_validate_category_fields():
    # Test with valid data
    data = {"name": "Test Category"}
    errors = validateCategoryFields(data)
    assert errors == []

    # Test with invalid data type
    data = {"name": 123}
    errors = validateCategoryFields(data)
    assert len(errors) == 1
    assert "name is expected to be of type str" in errors[0]

