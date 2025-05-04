from dataclasses import dataclass
from typing import Any, Optional

from rest_framework.response import Response

from .data import exclude_empty
from .formats import to_serialize
from .types import ErrorType, RespCode, RespStatus


@dataclass
class Error(Exception):
    code: RespCode = RespCode.BAD_REQUEST
    type: ErrorType = ErrorType.UNKNOWN_ERROR
    message: Optional[str] = None
    details: Any = None

    def to_dict(self) -> dict:
        raw = {
            "status": RespStatus.ERROR,
            "code": self.code,
            "error_type": self.type,
            "message": self.message,
            "details": to_serialize(self.details),
        }
        return exclude_empty(raw)

    def to_resp(self) -> Response:
        return Response(
            data=self.to_dict(),
            status=self.code,
        )
