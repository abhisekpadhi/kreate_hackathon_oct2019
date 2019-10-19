from app.models import User


class UserManager:
    def __init__(self):
        pass

    def get_user_by_id(self, user_id=None):
        if not user_id:
            return None

        if User.objects.filter(id=user_id).exists():
            return User.objects.get(id=user_id)
        else:
            return None

    def get_user_by_phone(self, phone=None):
        if not phone:
            return None

        if User.objects.filter(phone=phone).exists():
            return User.objects.get(phone=phone)
        else:
            return None
