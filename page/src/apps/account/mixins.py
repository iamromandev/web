from typing import Any

from .services.profile_service import ProfileService


class InjectProfileServiceMixin:
    def __init__(
        self,
        *args: Any,
        profile_service: ProfileService | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.profile_service = profile_service or ProfileService()
