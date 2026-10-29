"""Assemble and compile the complete single-agent LangGraph."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph

from src.checkpoints import create_checkpointer
from src.config import Settings, get_settings
from src.llm import get_chat_model
from src.nodes import create_agent_node, create_limit_node, create_tool_node
from src.routing import should_continue
from src.state import AgentState
from src.tool_registry import AVAILABLE_TOOLS


def build_agent_graph(
    model: Any | None = None,
    tools: Sequence[BaseTool] | None = None,
    checkpointer: Any | None = None,
    settings: Settings | None = None,
) -> Any:
    """Define nodes and edges, then compile them into a runnable graph."""

    settings = settings or get_settings()
    selected_tools = list(tools or AVAILABLE_TOOLS)
    selected_model = model or get_chat_model(settings)
    selected_checkpointer = checkpointer or create_checkpointer(settings)

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", create_agent_node(selected_model, selected_tools, settings))
    workflow.add_node("tools", create_tool_node(selected_tools, settings))
    workflow.add_node("limit", create_limit_node(settings))

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        lambda state: should_continue(state, settings),
        {"tools": "tools", "limit": "limit", "end": END},
    )
    workflow.add_edge("tools", "agent")
    workflow.add_edge("limit", END)

    return workflow.compile(checkpointer=selected_checkpointer)

