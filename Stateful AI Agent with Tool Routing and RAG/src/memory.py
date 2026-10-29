"""Helpers that explain and inspect thread-scoped short-term memory."""

from __future__ import annotations

from typing import Any

from langchain_core.messages import AIMessage, HumanMessage


def thread_config(thread_id: str, recursion_limit: int = 30) -> dict[str, Any]:
    """Create the config LangGraph uses to isolate one conversation."""

    if not thread_id or not thread_id.strip():
        raise ValueError("thread_id must not be empty")
    return {
        "configurable": {"thread_id": thread_id.strip()},
        "recursion_limit": recursion_limit,
    }


def public_conversation(messages: list[Any]) -> list[dict[str, str]]:
    """Return only user-visible messages; tool protocol messages stay internal."""

    conversation: list[dict[str, str]] = []
    for message in messages:
        if isinstance(message, HumanMessage):
            conversation.append({"role": "user", "content": str(message.content)})
        elif isinstance(message, AIMessage) and message.content and not message.tool_calls:
            conversation.append({"role": "assistant", "content": str(message.content)})
    return conversation

