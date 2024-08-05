from unittest.mock import MagicMock, patch

import pytest

from app import create_app
from gateways.category import CategoryGateway
from gateways.ticket import TicketGateway
from services.category import CategoryService
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
def category_data():
    return {"id": 1, "name": "Test Category", "parent_id": None, "subcategories": []}


def test_create_category(app_context, category_data):
    # Case when category is successfully created
    with patch.object(CategoryGateway, "create", return_value=MagicMock(id=1)):
        result = CategoryService.create_category(name="Test Category")
        assert result == {"category_id": 1}

    # Case when parent category is invalid
    with patch.object(CategoryGateway, "get_by_id", return_value=None):
        result = CategoryService.create_category(name="Test Category", parent_id=2)
        expected_error = {"errors": [error_message(LocalApiCode.invalidParentCategory)]}
        assert result == expected_error

    # Case when category name is duplicated
    with patch.object(CategoryGateway, "create", return_value=None):
        result = CategoryService.create_category(name="Test Category")
        expected_error = {"errors": [error_message(LocalApiCode.duplicateCategoryName)]}
        assert result == expected_error


def test_get_category_by_id(app_context, category_data):
    # Case when category is found
    with patch.object(
        CategoryGateway,
        "get_by_id",
        return_value=MagicMock(to_dict=lambda include_subcategories: category_data),
    ):
        result = CategoryService.get_category_by_id(1)
        assert result == category_data

    # Case when category is not found
    with patch.object(CategoryGateway, "get_by_id", return_value=None):
        result = CategoryService.get_category_by_id(10)
        expected_error = {"errors": [error_message(LocalApiCode.categoryNotFound)]}
        assert result == expected_error


def test_get_all_categories(app_context, category_data):
    with patch.object(
        CategoryGateway,
        "get_all",
        return_value=[MagicMock(to_dict=lambda include_subcategories: category_data)],
    ):
        result = CategoryService.get_all_categories()
        assert result == [category_data]


def test_update_category(app_context, category_data):
    # Case when category is successfully updated
    with patch.object(
        CategoryGateway, "get_by_id", return_value=MagicMock()
    ), patch.object(
        CategoryGateway, "update", return_value=MagicMock(to_dict=lambda: category_data)
    ), patch.object(
        CategoryGateway, "get_by_name", return_value=None
    ):

        result = CategoryService.update_category(1, name="Updated Category")
        assert result == {"category": category_data}

    # Case when category name is duplicated
    with patch.object(CategoryGateway, "get_by_name", return_value=MagicMock()):
        result = CategoryService.update_category(1, name="Test Category")
        expected_error = {"errors": [error_message(LocalApiCode.duplicateCategoryName)]}
        assert result == expected_error

    # Case when category is not found
    with patch.object(CategoryGateway, "get_by_id", return_value=None):
        result = CategoryService.update_category(10, name="Updated Category")
        expected_error = {"errors": [error_message(LocalApiCode.categoryNotFound)]}
        assert result == expected_error


def test_delete_category(app_context, category_data):
    # Case when category is successfully deleted
    with patch.object(
        CategoryGateway, "get_by_id", return_value=MagicMock()
    ), patch.object(TicketGateway, "get_by_category_id", return_value=[]), patch.object(
        CategoryGateway, "get_by_parent_id", return_value=[]
    ), patch.object(
        TicketGateway, "get_by_subcategory_id", return_value=[]
    ), patch.object(
        CategoryGateway, "delete", return_value=None
    ):

        result = CategoryService.delete_category(1)
        assert result == {"message": "Category deleted successfully"}

    # Case when category has tickets
    with patch.object(TicketGateway, "get_by_category_id", return_value=[MagicMock()]):
        result = CategoryService.delete_category(1)
        expected_error = {"errors": [error_message(LocalApiCode.categoryHasTickets)]}
        assert result == expected_error

    # Case when category has subcategories
    with patch.object(CategoryGateway, "get_by_parent_id", return_value=[MagicMock()]):
        result = CategoryService.delete_category(1)
        expected_error = {
            "errors": [error_message(LocalApiCode.categoryHasSubcategories)]
        }
        expected_error2 = {"errors": [error_message(LocalApiCode.categoryHasTickets)]}
        assert result == expected_error or result == expected_error2

    # Case when subcategory has tickets
    with patch.object(
        CategoryGateway, "get_by_id", return_value=MagicMock()
    ), patch.object(CategoryGateway, "get_by_parent_id", return_value=[]), patch.object(
        TicketGateway, "get_by_category_id", return_value=[]
    ), patch.object(
        TicketGateway, "get_by_subcategory_id", return_value=[MagicMock()]
    ):

        result = CategoryService.delete_category(1)
        expected_error = {"errors": [error_message(LocalApiCode.subcategoryHasTickets)]}
        assert result == expected_error

    # Case when category is not found
    with patch.object(CategoryGateway, "get_by_id", return_value=None):
        result = CategoryService.delete_category(10)
        expected_error = {"errors": [error_message(LocalApiCode.categoryNotFound)]}
        assert result == expected_error
