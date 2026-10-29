"""Node functions: model decides, tools act, and a guardrail stops runaway loops."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool
from langgraph.prebuilt import ToolNode

from src.config import Settings, get_settings
from src.guardrails import limit_message
from src.prompts import SYSTEM_PROMPT
from src.state import AgentState
from src.utils import debug_event

Node = Callable[[AgentState], dict[str, Any]]


def _text_content(message: AIMessage) -> str:
    if isinstance(message.content, str):
        return message.content
    return str(message.content)


def _safe_tool_error(error: Exception) -> str:
    """Convert tool exceptions to useful observations without exposing internals."""

    root_error = error.__cause__ or error
    if isinstance(root_error, ValueError):
        return f"Tool input error: {root_error}"
    return "The tool failed unexpectedly. Try again or contact the application operator."


def create_agent_node(
    model: Any,
    tools: Sequence[BaseTool],
    settings: Settings | None = None,
) -> Node:
    """Bind tools once, then return the graph's model/decision node."""

    settings = settings or get_settings()
    model_with_tools = model.bind_tools(list(tools))

    def agent_node(state: AgentState) -> dict[str, Any]:
        current_iteration = state.get("iteration_count", 0)
        steps = list(state.get("steps", []))
        if current_iteration >= settings.max_agent_iterations:
            answer = limit_message(settings)
            steps.append(
                {
                    "type": "guardrail",
                    "status": "stopped",
                    "details": {"reason": "maximum iterations reached"},
                }
            )
            return {
                "messages": [AIMessage(content=answer)],
                "current_step": "guardrail",
                "final_answer": answer,
                "steps": steps,
            }

        response = model_with_tools.invoke(
            [SystemMessage(content=SYSTEM_PROMPT), *state.get("messages", [])]
        )
        if not isinstance(response, AIMessage):
            response = AIMessage(content=str(response.content))

        tool_calls = list(state.get("tool_calls", []))
        for call in response.tool_calls:
            public_call = {
                "id": call.get("id", ""),
                "name": call.get("name", "unknown"),
                "args": call.get("args", {}),
            }
            tool_calls.append(public_call)
            steps.append(
                {
                    "type": "tool_call",
                    "status": "success",
                    "tool": public_call["name"],
                    "details": {"arguments": public_call["args"]},
                }
            )

        is_final = not response.tool_calls
        answer = _text_content(response) if is_final else None
        if is_final:
            steps.append({"type": "response", "status": "success", "details": {}})

        debug_event(
            settings.debug_agent,
            f"Agent Step {current_iteration + 1}",
            {
                "node": "agent",
                "decision": "call_tools" if response.tool_calls else "final_response",
                "tools": [call.get("name") for call in response.tool_calls],
            },
        )
        return {
            "messages": [response],
            "iteration_count": current_iteration + 1,
            "current_step": "agent",
            "tool_calls": tool_calls,
            "final_answer": answer,
            "steps": steps,
        }

    return agent_node


def create_tool_node(
    tools: Sequence[BaseTool],
    settings: Settings | None = None,
) -> Node:
    """Wrap LangGraph's ToolNode to add safe, observable activity metadata."""

    settings = settings or get_settings()
    executor = ToolNode(list(tools), handle_tool_errors=_safe_tool_error)

    def tools_node(state: AgentState) -> dict[str, Any]:
        output = executor.invoke(state)
        tool_messages = output.get("messages", [])
        results = list(state.get("tool_results", []))
        steps = list(state.get("steps", []))
        for message in tool_messages:
            if not isinstance(message, ToolMessage):
                continue
            status = "error" if getattr(message, "status", "success") == "error" else "success"
            results.append(
                {
                    "tool_call_id": message.tool_call_id,
                    "name": message.name or "unknown",
                    "status": status,
                    "content": str(message.content),
                }
            )
            steps.append(
                {
                    "type": "tool_result",
                    "status": status,
                    "tool": message.name or "unknown",
                    "details": {},
                }
            )
            debug_event(
                settings.debug_agent,
                "Tool Result",
                {"node": "tools", "tool": message.name, "status": status},
            )
        return {
            "messages": tool_messages,
            "tool_results": results,
            "current_step": "tools",
            "steps": steps,
        }

    return tools_node


def create_limit_node(settings: Settings | None = None) -> Node:
    settings = settings or get_settings()

    def limit_node(state: AgentState) -> dict[str, Any]:
        answer = limit_message(settings)
        steps = list(state.get("steps", []))
        steps.append(
            {
                "type": "guardrail",
                "status": "stopped",
                "details": {"reason": "maximum tool calls reached"},
            }
        )
        return {
            "messages": [AIMessage(content=answer)],
            "current_step": "guardrail",
            "final_answer": answer,
            "steps": steps,
        }

    return limit_node
