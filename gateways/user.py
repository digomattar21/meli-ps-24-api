from services.jsonplaceholder import JSONPlaceholderService

class UserGateway:

    @classmethod
    def get_user_by_id(cls, user_id):
        return JSONPlaceholderService.get_user_by_id(user_id)

    @classmethod
    def get_all_users(cls):
        return JSONPlaceholderService.get_all_users()