from typing import Any

from django.views.generic import TemplateView

from .constants import (
    USER,
)


class IndexView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["user"] = USER
        return context
