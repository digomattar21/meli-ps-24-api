import pytest

from app import create_app
from gateways.user import UserGateway


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


def test_get_user_by_id(app):
    with app.app_context():
        user = UserGateway.get_user_by_id(1)
        assert user is not None
        assert user["name"] == "Leanne Graham"


def test_get_all_users(app):
    with app.app_context():
        users = UserGateway.get_all_users()
        assert len(users) == 10
        assert users[0]["name"] == "Leanne Graham"
