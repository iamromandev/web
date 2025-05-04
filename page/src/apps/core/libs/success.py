from dataclasses import dataclass, field
from typing import Any, Optional

from rest_framework.response import Response

from .formats import to_serialize
from .times import utc_iso_timestamp
from .types import Code, Status


@dataclass
class Success:
    status: Status = Status.SUCCESS
    code: Code = Code.OK
    timestamp: str = field(default_factory=utc_iso_timestamp)
    message: Optional[str] = None
    meta: Optional[dict[str, Any]] = None
    data: Any = None

    def add_pagination(self, pagination: dict[str, Any]) -> None:
        if self.meta is None:
            self.meta = {}
        self.meta["pagination"] = pagination

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "code": self.code,
            "message": self.message,
            "data": to_serialize(self.data),
        }

    def to_resp(self) -> Response:
        return Response(
            data=self.to_dict(),
            status=self.code,
        )
