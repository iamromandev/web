from typing import Optional

from .services.auth_service import AuthService


class InjectAuthServiceMixin:
    def __init__(
        self,
        *args,
        auth_service: Optional[AuthService] = None, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.auth_service = auth_service or AuthService()


