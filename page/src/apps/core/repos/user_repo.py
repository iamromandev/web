from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from ..models import User
from .base_repo import BaseRepo


class UserRepo(BaseRepo[User]):

    def __init__(self):
        super().__init__(User)

    @staticmethod
    def get_user_by_username(
        username: str
    ) -> Optional[User]:
        try:
            user: User = User.objects.get(username=username)
            return user
        except ObjectDoesNotExist:
            return None
