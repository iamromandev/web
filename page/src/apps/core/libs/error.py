from dataclasses import dataclass
from typing import Any, Union, cast

from loguru import logger
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .data import exclude_empty
from .formats import to_serialize
from .resp import Resp
from .types import StrBaseEnum


@dataclass
class Error(Resp, Exception):
    class Type(StrBaseEnum):
        # General
        UNKNOWN_ERROR = "unknown_error"
        SERVER_ERROR = "server_error"
        SERVICE_UNAVAILABLE = "service_unavailable"
        NOT_IMPLEMENTED = "not_implemented"
        TIMEOUT = "timeout"
        BAD_GATEWAY = "bad_gateway"
        DEPENDENCY_FAILURE = "dependency_failure"
        GATEWAY_TIMEOUT = "gateway_timeout"

        # HTTP-related
        VALIDATION_ERROR = "validation_error"
        INVALID_REQUEST = "invalid_request"
        UNPROCESSABLE_ENTITY = "unprocessable_entity"
        RATE_LIMITED = "rate_limited"
        NOT_FOUND = "not_found"
        METHOD_NOT_ALLOWED = "method_not_allowed"
        BAD_REQUEST = "bad_request"
        UNSUPPORTED_MEDIA_TYPE = "unsupported_media_type"
        TOO_MANY_REQUESTS = "too_many_requests"
        FORBIDDEN = "forbidden"
        UNAUTHORIZED = "unauthorized"
        CONFLICT = "conflict"
        PAYLOAD_TOO_LARGE = "payload_too_large"

        # Authentication & Authorization
        AUTHENTICATION_ERROR = "authentication_error"
        AUTHORIZATION_ERROR = "authorization_error"
        TOKEN_EXPIRED = "token_expired"
        TOKEN_INVALID = "token_invalid"
        SESSION_EXPIRED = "session_expired"

        # Business logic / domain errors
        DUPLICATE_ENTRY = "duplicate_entry"
        ALREADY_EXISTS = "already_exists"
        DOES_NOT_EXIST = "does_not_exist"
        INVALID_STATE = "invalid_state"
        PRECONDITION_FAILED = "precondition_failed"
        RESOURCE_LOCKED = "resource_locked"

        # Input/Output & Type Issues
        TYPE_ERROR = "type_error"
        VALUE_ERROR = "value_error"
        MISSING_FIELD = "missing_field"
        INVALID_FIELD = "invalid_field"
        INVALID_FORMAT = "invalid_format"
        UNSUPPORTED_OPERATION = "unsupported_operation"

        # External/3rd-party issues
        EXTERNAL_API_ERROR = "external_api_error"
        THIRD_PARTY_ERROR = "third_party_error"
        INTEGRATION_FAILURE = "integration_failure"

        # Database/Storage
        DB_ERROR = "db_error"
        DATA_INTEGRITY_ERROR = "data_integrity_error"
        UNIQUE_CONSTRAINT_VIOLATION = "unique_constraint_violation"
        FOREIGN_KEY_VIOLATION = "foreign_key_violation"

        # File Handling
        FILE_NOT_FOUND = "file_not_found"
        FILE_UPLOAD_ERROR = "file_upload_error"
        FILE_FORMAT_ERROR = "file_format_error"
        FILE_TOO_LARGE = "file_too_large"

        # Email / Notifications
        EMAIL_SEND_FAILED = "email_send_failed"
        NOTIFICATION_ERROR = "notification_error"

    type: Type = Type.UNKNOWN_ERROR
    details: Any | None = None

    def __post_init__(self) -> None:
        self.status = Resp.Status.ERROR

    def to_dict(self) -> dict:
        raw = {
            "status": self.status,
            "code": self.code,
            "message": self.message,
            "type": self.type,
            "details": to_serialize(self.details),
        }
        return exclude_empty(raw)

    @staticmethod
    def of(error: ValidationError) -> Union["Error", None]:
        if isinstance(error, ValidationError):
            return Error(
                status=Resp.Status.ERROR,
                code=Resp.Code.BAD_REQUEST,
                message="Validation failed",
                type=Error.Type.VALIDATION_ERROR,
                details=error.detail
            )
        return None


@dataclass
class PasswordMismatchError(Error):
    def __post_init__(self) -> None:
        super().__post_init__()
        self.code = Resp.Code.BAD_REQUEST
        self.message = "Passwords do not match."
        self.type = Error.Type.VALIDATION_ERROR


def error_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    logger.error("Error||error_handler|Unhandled exception", exc_info=exc)

    error: Error | None = None
    if isinstance(exc, Error):
        error = cast(Error, exc)
    else:
        logger.error("Error||error_handler|Exception|", exc_info=exc)
        error = Error.of(exc)

    return error.to_resp() or None
    # else:
    #     resp = exception_handler(exc, context)
    #     if resp is None:
    #         logger.error("Unhandled exception", exc_info=exc)
    #         error
    #
    #     # Default Error
    #     error = Error(
    #         code=resp.status_code,
    #         type=exc.__class__.__name__.lower(),
    #         message="An unknown error occurred.",
    #         details=resp.data,
    #     ) if not error else error
    #     return error.to_resp()
