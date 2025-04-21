from datetime import datetime
from functools import lru_cache

import pytz


class TimezoneChoices:
    @classmethod
    @lru_cache(maxsize=1)  # Cache the result with a size of 1 since it won't change
    def get_choices(cls) -> list[tuple[str, str]]:
        """
        Generate a list of timezone choices with UTC offsets.
        Cached using lru_cache for performance.
        """
        now = datetime.now()
        choices = []
        for tz_name in pytz.common_timezones:
            tz = pytz.timezone(tz_name)
            offset = tz.utcoffset(now)
            if offset is not None:
                offset_seconds = offset.total_seconds()
                offset_hours = offset_seconds / 3600
                label = f"{tz_name} (UTC{offset_hours:+.1f})"
                choices.append((tz_name, label))
        return choices
