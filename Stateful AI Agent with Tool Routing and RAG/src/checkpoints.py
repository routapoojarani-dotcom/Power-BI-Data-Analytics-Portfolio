"""In-memory and SQLite checkpointer factories."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

from src.config import PROJECT_ROOT, Settings, get_settings

_SQLITE_CONNECTIONS: list[sqlite3.Connection] = []


def create_checkpointer(settings: Settings | None = None) -> Any:
    """Use zero-setup memory, or SQLite when ``CHECKPOINT_DB_PATH`` is set."""

    settings = settings or get_settings()
    if not settings.checkpoint_db_path:
        return InMemorySaver()

    db_path = Path(settings.checkpoint_db_path)
    if not db_path.is_absolute():
        db_path = PROJECT_ROOT / db_path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path, check_same_thread=False)
    _SQLITE_CONNECTIONS.append(connection)
    saver = SqliteSaver(connection)
    saver.setup()
    return saver


def close_sqlite_connections() -> None:
    """Close tutorial SQLite connections (mainly useful in tests and scripts)."""

    while _SQLITE_CONNECTIONS:
        _SQLITE_CONNECTIONS.pop().close()

