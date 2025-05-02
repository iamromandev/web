from typing import Optional

from apps.core.mixins import ApiMixin


class ApiClient(ApiMixin):
    def __init__(
        self,
        base_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        super().__init__(base_url, username, password)


