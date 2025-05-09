from typing import Any

from django.conf import settings

from .clients import ApiClient


class InjectApiClientMixin:
    def __init__(
        self,
        *args: Any,
        api_client: ApiClient | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.api_client = api_client or ApiClient(
            base_url=settings.BASE_URL,
            username=settings.USERNAME,
            password=settings.PASSWORD,
        )
