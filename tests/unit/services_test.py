from app import create_app
from services.jsonplaceholder import JSONPlaceholderService

def test_get_all_users():
    app = create_app()
    with app.app_context():
        users = JSONPlaceholderService.get_all_users()
        assert users is not None
        assert len(users) == 10
        assert users[0]["name"] == "Leanne Graham"
