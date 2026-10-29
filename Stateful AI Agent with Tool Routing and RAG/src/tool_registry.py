"""One discoverable registry for every capability available to the agent."""

from __future__ import annotations

from langchain_core.tools import BaseTool

from tools.calculator import calculator
from tools.current_datetime import current_datetime
from tools.employee_lookup import employee_lookup
from tools.knowledge_search import knowledge_search
from tools.order_lookup import order_lookup

AVAILABLE_TOOLS: list[BaseTool] = [
    calculator,
    employee_lookup,
    order_lookup,
    knowledge_search,
    current_datetime,
]

TOOLS_BY_NAME: dict[str, BaseTool] = {tool.name: tool for tool in AVAILABLE_TOOLS}


def list_tool_summaries() -> list[dict[str, str]]:
    return [
        {"name": registered_tool.name, "description": registered_tool.description}
        for registered_tool in AVAILABLE_TOOLS
    ]

