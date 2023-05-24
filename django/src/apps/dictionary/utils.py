from typing import Optional, List


def join_list_in_sort(items: List[str]) -> Optional[str]:
    if not items or len(items) < 2:
        return None
    items.sort()
    return "".join(items)
