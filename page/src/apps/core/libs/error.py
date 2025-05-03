import enum
from dataclasses import dataclass
from typing import Optional


@dataclass
class Error:
    class Code(enum.IntEnum):
        # 1xx Informational
        CONTINUE = 100
        SWITCHING_PROTOCOLS = 101
        PROCESSING = 102
        EARLY_HINTS = 103

        # 2xx Success
        OK = 200
        CREATED = 201
        ACCEPTED = 202
        NON_AUTHORITATIVE_INFORMATION = 203
        NO_CONTENT = 204
        RESET_CONTENT = 205
        PARTIAL_CONTENT = 206
        MULTI_STATUS = 207
        ALREADY_REPORTED = 208
        IM_USED = 226

        # 3xx Redirection
        MULTIPLE_CHOICES = 300
        MOVED_PERMANENTLY = 301
        FOUND = 302
        SEE_OTHER = 303
        NOT_MODIFIED = 304
        USE_PROXY = 305
        TEMPORARY_REDIRECT = 307
        PERMANENT_REDIRECT = 308

        # 4xx Client Errors
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        PAYMENT_REQUIRED = 402
        FORBIDDEN = 403
        NOT_FOUND = 404
        METHOD_NOT_ALLOWED = 405
        NOT_ACCEPTABLE = 406
        PROXY_AUTHENTICATION_REQUIRED = 407
        REQUEST_TIMEOUT = 408
        CONFLICT = 409
        GONE = 410
        LENGTH_REQUIRED = 411
        PRECONDITION_FAILED = 412
        PAYLOAD_TOO_LARGE = 413
        URI_TOO_LONG = 414
        UNSUPPORTED_MEDIA_TYPE = 415
        RANGE_NOT_SATISFIABLE = 416
        EXPECTATION_FAILED = 417
        IM_A_TEAPOT = 418
        MISDIRECTED_REQUEST = 421
        UNPROCESSABLE_ENTITY = 422
        LOCKED = 423
        FAILED_DEPENDENCY = 424
        TOO_EARLY = 425
        UPGRADE_REQUIRED = 426
        PRECONDITION_REQUIRED = 428
        TOO_MANY_REQUESTS = 429
        REQUEST_HEADER_FIELDS_TOO_LARGE = 431
        UNAVAILABLE_FOR_LEGAL_REASONS = 451

        # 5xx Server Errors
        INTERNAL_SERVER_ERROR = 500
        NOT_IMPLEMENTED = 501
        BAD_GATEWAY = 502
        SERVICE_UNAVAILABLE = 503
        GATEWAY_TIMEOUT = 504
        HTTP_VERSION_NOT_SUPPORTED = 505
        VARIANT_ALSO_NEGOTIATES = 506
        INSUFFICIENT_STORAGE = 507
        LOOP_DETECTED = 508
        NOT_EXTENDED = 510
        NETWORK_AUTHENTICATION_REQUIRED = 511

    class ErrorType(enum.Enum):
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



    error_type: ErrorType
    message: str
    code: Optional[int] = None
    field: Optional[str] = None  # Optional for field-level validation errors

    def to_dict(self) -> dict:
        return {
            "error_type": self.error_type.value,
            "message": self.message,
            "code": self.code,
            "field": self.field,
        }


