import math
from dataclasses import dataclass, field
from typing import Any, Optional

from .data import exclude_empty
from .formats import to_serialize
from .resp import Resp
from .times import utc_iso_timestamp


@dataclass
class Success(Resp):
    data: Any = None
    meta: Optional[dict[str, Any]] = None
    timestamp: str = field(default_factory=utc_iso_timestamp)

    def __post_init__(self):
        self.status = Resp.Status.SUCCESS
        self.code = Resp.Code.OK

    def add_pagination(
        self,
        page: int = 1,
        page_size: int = 10, total: int = 0, total_pages: int = 0
    ) -> None:
        if self.meta is None:
            self.meta = {}
        self.meta["pagination"] = {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": math.ceil(total / page_size),
        }

    def to_dict(self) -> dict:
        raw = {
            "status": self.status,
            "code": self.code,
            "message": self.message,
            "data": to_serialize(self.data),
            "meta": self.meta,
            "timestamp": self.timestamp,
        }
        return exclude_empty(raw)
