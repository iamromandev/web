from typing import Any, Optional

from .builders.response import ResponseBuilder


class InjectCoreMixin:
    def __init__(
        self,
        *args: Any,
        response_builder: Optional[ResponseBuilder] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.response_builder = response_builder or ResponseBuilder.new()