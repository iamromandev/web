from typing import Any

from django.views.generic import TemplateView

from apps.account.mixins import InjectProfileServiceMixin

from .constants import (
    USER,
)


class IndexView(InjectProfileServiceMixin, TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # TODO rest endpoint to get user profile

        context["user"] = USER
        return context
