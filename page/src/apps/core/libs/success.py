from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from rest_framework.response import Response

from .formats import to_serialize
from .types import Code, Status


@dataclass
class Success:
    status: Status
    code: Code
    message: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat().replace("+00:00", "Z")
    )
    data: Any = None

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
