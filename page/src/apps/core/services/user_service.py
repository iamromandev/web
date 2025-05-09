from typing import Any

from ..repos.user_repo import UserRepo
from .base_service import BaseService


class UserService(BaseService):
    def __init__(
        self, *args: Any,
        user_repo: UserRepo | None = None,
        **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.user_repo = user_repo or UserRepo()
