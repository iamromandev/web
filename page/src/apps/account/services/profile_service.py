from typing import Optional

from apps.authn.services.auth_service import AuthService
from apps.core.clients import ApiClient


class ProfileService(AuthService):
    def __init__(
        self,
        base_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> None:
        super().__init__()
        self._client = ApiClient(
            base_url=base_url,
            token_endpoint="auth/token/",
            refresh_endpoint="auth/token/refresh/",
            auth_payload={
                "username": username,
                "password": password,
            } if username and password else None,
        )

    def get_profile(self) -> dict:
        """
        Get the profile of the authenticated user.
        """
        return self._client.get("profile/")
