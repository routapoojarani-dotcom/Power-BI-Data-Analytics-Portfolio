"""Application-facing response models; no private model reasoning is exposed."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class AgentStep(BaseModel):
    """An observable event such as a tool call or tool result."""

    type: Literal["received", "tool_call", "tool_result", "response", "guardrail", "error"]
    status: Literal["pending", "success", "error", "stopped"] = "success"
    tool: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseModel):
    """Stable result shared by Flask, the JSON API, and the CLI."""

    answer: str
    thread_id: str
    tools_used: list[str] = Field(default_factory=list)
    steps: list[AgentStep] = Field(default_factory=list)
    iterations: int = 0
    errors: list[str] = Field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return self.model_dump()

