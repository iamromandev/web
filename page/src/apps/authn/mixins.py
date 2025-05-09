from typing import Any

from .services.auth_service import AuthService


class InjectAuthServiceMixin:
    def __init__(
        self,
        *args: Any,
        auth_service: AuthService | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.auth_service = auth_service or AuthService()