import math
from typing import Any, Optional

from loguru import logger
from rest_framework import response, status

from apps.core.libs.types import ResponseStatus


class ResponseBuilder:
    def __init__(
        self,
        status: Optional[ResponseStatus] = None,
        timestamp: Optional[str] = None,
        code: Optional[str] = None,
        message: Optional[str] = None,
        data: Optional[Any] = None,
        details: Optional[dict[str, list[str]]] = None,
        meta: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        self.status = status
        self.timestamp = timestamp
        self.code = code
        self.message = message
        self.data = data
        self.details = details
        self.meta = meta
        self.headers = headers

    # def __new__[T](cls: Type[T], *args: Any, **kwargs: Any) -> T:
    #    raise RuntimeError("Use `ResponseBuilder.create()` instead of direct instantiation")

    @staticmethod
    def new(
        status: Optional[ResponseStatus] = None,
        timestamp: Optional[str] = None,
        code: Optional[str] = None,
        message: Optional[str] = None,
        data: Optional[Any] = None,
        details: Optional[dict[str, list[str]]] = None,
        meta: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> "ResponseBuilder":
        builder = ResponseBuilder(
            status=status,
            timestamp=timestamp,
            code=code,
            message=message,
            data=data,
            details=details,
            meta=meta,
            headers=headers
        )
        return builder

    def set_status(self, status: ResponseStatus) -> "ResponseBuilder":
        self.status = status
        return self

    def set_timestamp(self, timestamp: str) -> "ResponseBuilder":
        self.timestamp = timestamp
        return self

    def set_code(self, code: str) -> "ResponseBuilder":
        self.code = code
        return self

    def set_message(self, message: str) -> "ResponseBuilder":
        self.message = message
        return self

    def set_data(self, data: Any) -> "ResponseBuilder":
        self.data = data
        return self

    def set_details(self, details: dict[str, list[str]]) -> "ResponseBuilder":
        self.details = details
        return self

    def set_meta(self, meta: dict[str, Any]) -> "ResponseBuilder":
        self.meta = meta
        return self

    def set_pagination(
        self, page: int = 1, page_size: int = 10, total: int = 0, total_pages: int = 0
    ) -> "ResponseBuilder":
        self.meta = {
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": math.ceil(total / page_size),
            }
        }
        return self

    def set_headers(self, headers: dict[str, str]) -> "ResponseBuilder":
        self.headers = headers
        return self

    def build(self, status_code=status.HTTP_200_OK) -> response.Response:
        if not self.status:
            self.status = (
                ResponseStatus.ERROR
                if status_code > status.HTTP_226_IM_USED
                else ResponseStatus.SUCCESS
            )
        data = {
            "status": self.status.value,
            "timestamp": self.timestamp,
            "code": self.code,
            "message": self.message,
            "data": self.data,
            "details": self.details,
            "meta": self.meta,
        }

        data = {k: v for k, v in data.items() if v not in (None, "", [], {}, ())}
        logger.info(f"Response Builder Data: {data}")
        return response.Response(
            data,
            status=status_code,
            headers=self.headers
        )
