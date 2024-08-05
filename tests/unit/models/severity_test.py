import pytest

from app import create_app
from heart.core.extensions import db
from models.severity import Severity


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
    severity_to_delete = Severity.query.filter_by(level=1).first()
    session.delete(severity_to_delete)
    session.commit()
    severity = Severity(level=1, description="Issue High")
    session.add(severity)
    session.commit()

    assert severity.id is not None
    assert severity.level == 1
    assert severity.description == "Issue High"


def test_update_severity(session):
    severity_to_delete = Severity.query.filter_by(level=1).first()
    session.delete(severity_to_delete)
    severity_to_delete_2 = Severity.query.filter_by(level=4).first()
    session.delete(severity_to_delete_2)
    session.commit()

    severity = Severity(level=1, description="High")
    session.add(severity)
    session.commit()

    severity.level = 4
    severity.description = "Low"
    session.commit()

    updated_severity = Severity.query.get(severity.id)
    assert updated_severity.level == 4
    assert updated_severity.description == "Low"


def test_delete_severity(session):
    severity_to_delete = Severity.query.filter_by(level=4).first()
    session.delete(severity_to_delete)
    session.commit()

    deleted_severity = Severity.query.get(severity_to_delete.id)
    assert deleted_severity is None
