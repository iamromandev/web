from datetime import UTC, datetime


def utc_iso_timestamp() -> str:
    """Get the current UTC timestamp in ISO 8601 format."""
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")