import pytest

from app import create_app
from gateways.severity import SeverityGateway
from heart.core.extensions import db
from heart.validators.severity import SEVERITY_DESCRIPTIONS


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


def test_create_severity(session):
    SeverityGateway.delete(1)
    severity = SeverityGateway.create(level=1, description=SEVERITY_DESCRIPTIONS[1])
    assert severity.level == 1
    assert severity.description == SEVERITY_DESCRIPTIONS[1]


def test_get_severity_by_id(session):
    severity = SeverityGateway.get_by_id(1)
    assert severity is not None
    assert severity.level == 1


def test_get_all_severities(session):
    severities = SeverityGateway.get_all()
    assert len(severities) == 4


def test_get_severity_by_level(session):
    severity = SeverityGateway.get_by_level(1)
    assert severity is not None
    assert severity.description == "Issue High"


def test_update_severity(session):
    SeverityGateway.delete(4)
    updated_severity = SeverityGateway.update(1, level=4)
    SeverityGateway.create(level=1, description=SEVERITY_DESCRIPTIONS[1])
    assert updated_severity is not None
    assert updated_severity.level == 4


def test_delete_severity(session):
    SeverityGateway.delete(1)
    retrieved_severity = SeverityGateway.get_by_id(1)
    assert retrieved_severity is None
    SeverityGateway.create(level=1, description=SEVERITY_DESCRIPTIONS[1])
