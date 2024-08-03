import requests
from flask import current_app


class JSONPlaceholderService:

    @classmethod
    def get_user_by_id(cls, user_id):
        base_url = current_app.config["JSONPLACEHOLDER_BASE_URL"]
        response = requests.get(f"{base_url}/users/{user_id}")
        if response.status_code == 200:
            return response.json()
        return None

    @classmethod
    def get_all_users(cls):
        base_url = current_app.config["JSONPLACEHOLDER_BASE_URL"]
        response = requests.get(f"{base_url}/users")
        if response.status_code == 200:
            return response.json()
        return None
