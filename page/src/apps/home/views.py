from typing import Any

from django.views.generic import TemplateView
from loguru import logger

from .constants import (
    USER,
)
from .mixins import InjectApiClientMixin


class IndexView(InjectApiClientMixin, TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        user_data = self.api_client.get_self_user()
        logger.info(f"User data: {user_data.json()}")

        context["user"] = USER
        return context
