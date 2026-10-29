"""Simple boundaries that keep the educational agent predictable."""

from __future__ import annotations

from src.config import Settings, get_settings


class InputValidationError(ValueError):
    """A safe error that can be shown to an end user."""


def validate_user_message(message: object, settings: Settings | None = None) -> str:
    settings = settings or get_settings()
    if not isinstance(message, str):
        raise InputValidationError("Message must be a string.")
    cleaned = message.strip()
    if not cleaned:
        raise InputValidationError("Please enter a message before sending.")
    if len(cleaned) > settings.max_user_message_length:
        raise InputValidationError(
            f"Message is too long. Maximum length is {settings.max_user_message_length} characters."
        )
    return cleaned


def limit_message(settings: Settings | None = None) -> str:
    settings = settings or get_settings()
    return (
        "I stopped safely because the agent reached its execution limit "
        f"({settings.max_agent_iterations} model steps or {settings.max_tool_calls} tool calls). "
        "Please simplify the request or try again."
    )

