from app.UserManager import UserManager


class LoginManager:
    def __init__(self):
        self.user_manager = UserManager()

    def login_by_phone(self, phone=None):
        if not phone:
            return None

        user = self.user_manager.get_user_by_phone(phone)
        return user
