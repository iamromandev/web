from django.core.exceptions import ObjectDoesNotExist

from apps.core.models import User
from apps.core.repos.base_repo import BaseRepo


class UserRepo(BaseRepo[User]):

    def __init__(self):
        super().__init__(User)

    def create_user(
        self, username: str, email: str, password: str
    ) -> User:
        user = super().create(
            username=username,
            email=email,
            password=password
        )
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
