
from apps.core.clients import BaseApiClient


class ApiClient(BaseApiClient):
    def __init__(
        self,
        base_url: str,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        super().__init__(
            base_url=base_url,
            token_endpoint="auth/token/",
            refresh_endpoint="auth/token/refresh/",
            auth_payload={
                "username": username,
                "password": password,
            } if username and password else None,
        )

    def get_self_user(self) -> dict | None:
        endpoint: str = "api/users/self/"
        return self.get(endpoint)
