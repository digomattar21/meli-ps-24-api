from unittest.mock import MagicMock, patch

import pytest

from gateways.severity import SeverityGateway
from gateways.ticket import TicketGateway
from services.severity import SeverityService
from utils.apiMessages import LocalApiCode, error_message


@pytest.fixture
def severity_data():
    return {"id": 1, "level": 2, "description": "High"}


def test_get_severity_by_id(severity_data):
    # Case with valid severity ID
    with patch.object(
        SeverityGateway,
        "get_by_id",
        return_value=MagicMock(to_dict=lambda: severity_data),
    ):
        result = SeverityService.get_severity_by_id(1)
        assert result == {"severity": severity_data}

    # Case with invalid ID
    with patch.object(SeverityGateway, "get_by_id", return_value=None):
        result = SeverityService.get_severity_by_id(10)
        expected_error = {"errors": [error_message(LocalApiCode.severityNotFound)]}
        assert result == expected_error


def test_get_all_severities(severity_data):
    with patch.object(
        SeverityGateway,
        "get_all",
        return_value=[MagicMock(to_dict=lambda: severity_data)],
    ):
        result = SeverityService.get_all_severities()
        assert result == [severity_data]


def test_create_severity():
    # Case when the severity level does not exist and is successfully created
    with patch.object(SeverityGateway, "get_by_level", return_value=None), patch.object(
        SeverityGateway, "create", return_value=MagicMock(id=1)
    ):
        result = SeverityService.create_severity(2)
        assert result == {"severity_id": 1}

    # Case when the severity level already exists
    with patch.object(SeverityGateway, "get_by_level", return_value=MagicMock()):
        result = SeverityService.create_severity(2)
        expected_error = {
            "errors": [error_message(LocalApiCode.duplicateSeverityLevel)]
        }
        assert result == expected_error


def test_update_severity(severity_data):
    # Case when updating a severity successfully
    with patch.object(SeverityGateway, "get_by_level", return_value=None), patch.object(
        TicketGateway, "get_by_severity_id", return_value=[]
    ), patch.object(
        SeverityGateway, "update", return_value=MagicMock(to_dict=lambda: severity_data)
    ):
        result = SeverityService.update_severity(1, level=2)
        assert result == {"severity": severity_data}

    # Case when severity level 1 is in use by tickets
    with patch.object(TicketGateway, "get_by_severity_id", return_value=[MagicMock()]):
        result = SeverityService.update_severity(1, level=1)
        expected_error = {"errors": [error_message(LocalApiCode.severityLevelOneInUse)]}
        assert result == expected_error

    # Case when trying to update to a severity level that already exists
    with patch.object(SeverityGateway, "get_by_level", return_value=MagicMock()):
        result = SeverityService.update_severity(1, level=2)
        expected_error = {
            "errors": [error_message(LocalApiCode.duplicateSeverityLevel)]
        }
        assert result == expected_error


def test_delete_severity(severity_data):
    # Case when severity is successfully deleted
    with patch.object(
        TicketGateway, "get_by_severity_id", return_value=[]
    ), patch.object(SeverityGateway, "delete", return_value=None):
        result = SeverityService.delete_severity(1)
        assert result == {"message": "Severity deleted successfully"}

    # Case when severity is in use by tickets
    with patch.object(TicketGateway, "get_by_severity_id", return_value=[MagicMock()]):
        result = SeverityService.delete_severity(1)
        expected_error = {"errors": [error_message(LocalApiCode.severityInUse)]}
        assert result == expected_error
