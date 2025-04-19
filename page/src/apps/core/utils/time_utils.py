from datetime import datetime
from functools import lru_cache
from zoneinfo import ZoneInfo, available_timezones


class TimezoneChoices:
    @classmethod
    @lru_cache(maxsize=1)  # Cache the result with a size of 1 since it won't change
    def get_choices(cls):
        """
            Generate a list of timezone choices with UTC offsets.
            Cached using lru_cache for performance.
            """
        now = datetime.now()
        choices = []
        for tz_name in sorted(available_timezones()):
            tz = ZoneInfo(tz_name)
            offset = now.replace(tzinfo=tz).utcoffset()
            if offset is not None:
                offset_hours = offset.total_seconds() / 3600
                label = f"{tz_name} (UTC{offset_hours:+.1f})"
                choices.append((tz_name, label))
        return choices

