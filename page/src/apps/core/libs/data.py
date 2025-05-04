def exclude_empty(data: dict) -> dict:
    """Return a copy of the dict excluding None, empty strings, lists, and dicts."""
    return {k: v for k, v in data.items() if v not in (None, "", (), [], {})}
