from typing import Any, Optional

from .services.user_service import UserService


class InjectUserServiceMixin:
    def __init__(
        self,
        *args: Any,
        user_service: Optional[UserService] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.user_service = user_service or UserService()

# class InjectBaseApiClientMixin:
#     def __init__(
#         self,
#         base_url: settings.BASE_URL,
#         username: Optional[str] = settings.USERNAME,
#         password: Optional[str] = settings.PASSWORD,
#     ) -> None:
#         self.client = ApiClient(
#             base_url=base_url,
#             token_endpoint="auth/token/",
#             refresh_endpoint="auth/token/refresh/",
#             auth_payload={
#                 "username": username,
#                 "password": password,
#             } if username and password else None,
#         )
