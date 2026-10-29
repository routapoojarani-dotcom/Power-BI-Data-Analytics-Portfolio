"""Conditional edges: inspect state and return the name of the next branch."""

from __future__ import annotations

from typing import Literal

from langchain_core.messages import AIMessage

from src.config import Settings, get_settings
from src.state import AgentState

Route = Literal["tools", "limit", "end"]


def should_continue(state: AgentState, settings: Settings | None = None) -> Route:
    """Route pending model tool calls to ToolNode; otherwise finish."""

    settings = settings or get_settings()
    messages = state.get("messages", [])
    if not messages:
        return "end"
    last_message = messages[-1]
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        return "end"
    if len(state.get("tool_calls", [])) > settings.max_tool_calls:
        return "limit"
    return "tools"

