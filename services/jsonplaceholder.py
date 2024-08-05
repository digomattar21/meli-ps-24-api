import logging

import requests
from flask import current_app


class JSONPlaceholderService:

    @classmethod
    def get_user_by_id(cls, user_id):
        base_url = current_app.config["JSONPLACEHOLDER_BASE_URL"]
        try:
            response = requests.get(f"{base_url}/users/{user_id}", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logging.error(
                f"Request timed out when trying to reach {base_url}/users/{user_id}"
            )
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as err:
            logging.error(f"An error occurred: {err}")
        return None

    @classmethod
    def get_all_users(cls):
        base_url = current_app.config["JSONPLACEHOLDER_BASE_URL"]
        try:
            response = requests.get(f"{base_url}/users", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logging.error(f"Request timed out when trying to reach {base_url}/users")
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as err:
            logging.error(f"An error occurred: {err}")
        return None
