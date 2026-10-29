"""Safe debugging helpers."""

from __future__ import annotations

import json
import logging
from typing import Any

LOGGER = logging.getLogger("langgraph_tutorial")


def configure_logging(debug: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def debug_event(enabled: bool, title: str, details: dict[str, Any]) -> None:
    """Log observable events only. Never pass prompts, credentials, or hidden reasoning."""

    if enabled:
        LOGGER.debug("%s\n%s", title, json.dumps(details, indent=2, default=str))

