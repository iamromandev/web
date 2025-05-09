from collections.abc import Iterable, Mapping
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import UUID

from rest_framework.exceptions import ErrorDetail


def to_serialize(obj: Any) -> str | list | dict | None:
    """
    Convert an object to a JSON-serializable format.

    Args:
        obj: Any Python object.

    Returns:
        A JSON-serializable representation of the object.
    """
    if obj is None:
        return None
    elif isinstance(obj, datetime | date):
        return obj.isoformat()
    elif isinstance(obj, Decimal | UUID | Exception | ErrorDetail):
        return str(obj)
    elif isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, list | tuple | set):
        return [to_serialize(item) for item in obj]
    elif isinstance(obj, Mapping):  # Handles dicts, OrderedDicts, etc.
        return {key: to_serialize(value) for key, value in obj.items()}
    elif hasattr(obj, "__dict__"):
        return {key: to_serialize(value) for key, value in obj.__dict__.items()}
    elif isinstance(obj, Iterable) and not isinstance(obj, str | bytes):
        return [to_serialize(item) for item in obj]
    else:
        return str(obj)
