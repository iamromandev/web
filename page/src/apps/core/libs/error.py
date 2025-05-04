from dataclasses import dataclass
from typing import Any

from rest_framework.response import Response

from .formats import to_serialize
from .types import Code, Status, Type


@dataclass
class Error(Exception):
    code: Code
    type: Type
    message: str
    details: Any = None

    def to_dict(self) -> dict:
        return {
            "status": Status.ERROR,
            "code": self.code,
            "error_type": self.type,
            "message": self.message,
            "details": to_serialize(self.details),
        }

    def to_resp(self) -> Response:
        return Response(
            data=self.to_dict(),
            status=self.code,
        )



