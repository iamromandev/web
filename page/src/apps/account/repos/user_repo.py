from django.core.exceptions import ObjectDoesNotExist

from apps.core.models import User


class UserRepo:
    @staticmethod
    def create_user(
        username: str, email: str, password: str
    ) -> User:
        user = User(
            username=username,
            email=email,
            password=password
        )
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def get_user_by_username(
        username: str
    ) -> User:
        try:
            user = User.objects.get(username=username)
            return user
        except ObjectDoesNotExist:
            return None
