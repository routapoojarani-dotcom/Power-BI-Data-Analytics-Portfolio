"""Current date/time tool using the Python standard library."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from langchain_core.tools import tool


def get_current_datetime(timezone_name: str = "UTC") -> dict[str, str]:
    try:
        selected_timezone = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Unknown IANA timezone: {timezone_name}") from exc
    current = datetime.now(UTC).astimezone(selected_timezone)
    return {
        "timezone": timezone_name,
        "iso_datetime": current.isoformat(timespec="seconds"),
        "date": current.date().isoformat(),
        "time": current.strftime("%H:%M:%S"),
    }


@tool("current_datetime")
def current_datetime(timezone_name: str = "UTC") -> str:
    """Get the current date and time in an IANA timezone such as `UTC` or `Asia/Kolkata`."""

    return json.dumps(get_current_datetime(timezone_name))

