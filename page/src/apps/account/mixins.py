from typing import Any, Optional

from django.conf import settings

from .services.profile_service import ProfileService


class InjectProfileServiceMixin:
    def __init__(
        self,
        *args: Any,
        profile_service: Optional[ProfileService] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.profile_service = profile_service or ProfileService(
            base_url=settings.BASE_URL,
            username=settings.USERNAME,
            password=settings.PASSWORD,
        )
