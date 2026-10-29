"""The shared state carried between LangGraph nodes."""

from __future__ import annotations

from typing import Annotated, Any, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict, total=False):
    """Transparent state for the teaching agent.

    Only ``messages`` uses a reducer: ``add_messages`` appends new messages while
    preserving LangChain message IDs. The other fields describe the current turn
    and are replaced when a node returns an update.
    """

    messages: Annotated[list[AnyMessage], add_messages]
    user_query: str
    tool_calls: list[dict[str, Any]]
    tool_results: list[dict[str, Any]]
    iteration_count: int
    current_step: str
    final_answer: str | None
    errors: list[str]
    steps: list[dict[str, Any]]


def initial_state(user_query: str) -> AgentState:
    """Create the per-turn fields. The service adds the HumanMessage separately."""

    return {
        "user_query": user_query,
        "tool_calls": [],
        "tool_results": [],
        "iteration_count": 0,
        "current_step": "received",
        "final_answer": None,
        "errors": [],
        "steps": [{"type": "received", "status": "success", "details": {}}],
    }

