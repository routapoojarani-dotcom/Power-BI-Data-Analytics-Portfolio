"""Step 9: SQLite stores checkpoints beyond one in-memory graph object."""

import sqlite3
import tempfile
from pathlib import Path
from typing import TypedDict

from _bootstrap import ROOT  # noqa: F401
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph


class CountState(TypedDict):
    count: int


def increment(state: CountState) -> dict[str, int]:
    return {"count": state["count"] + 1}


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="langgraph-tutorial-") as temporary_directory:
        db_path = Path(temporary_directory) / "checkpoints.sqlite3"
        connection = sqlite3.connect(db_path, check_same_thread=False)
        saver = SqliteSaver(connection)
        saver.setup()
        builder = StateGraph(CountState)
        builder.add_node("increment", increment)
        builder.add_edge(START, "increment")
        builder.add_edge("increment", END)
        graph = builder.compile(checkpointer=saver)
        config = {"configurable": {"thread_id": "saved-game"}}
        graph.invoke({"count": 0}, config)
        print("Saved state:", graph.get_state(config).values)
        print("Temporary SQLite checkpoint verified:", db_path)
        connection.close()
