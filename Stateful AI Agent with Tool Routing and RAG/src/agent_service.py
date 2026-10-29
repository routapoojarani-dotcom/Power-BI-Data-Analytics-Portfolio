"""The one application-facing interface shared by the CLI and Flask."""

from __future__ import annotations

from functools import lru_cache
from typing import Any
from uuid import uuid4

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.errors import GraphRecursionError

from src.config import Settings, get_settings
from src.graph import build_agent_graph
from src.guardrails import InputValidationError, validate_user_message
from src.memory import public_conversation, thread_config
from src.models import AgentResult, AgentStep
from src.state import initial_state


class AgentService:
    """Run the graph and translate graph state into safe public results."""

    def __init__(self, graph: Any | None = None, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.graph = graph or build_agent_graph(settings=self.settings)

    def run_agent(self, user_message: str, thread_id: str | None = None) -> AgentResult:
        message = validate_user_message(user_message, self.settings)
        selected_thread = (thread_id or str(uuid4())).strip()
        recursion_limit = (self.settings.max_agent_iterations * 2) + 4
        config = thread_config(selected_thread, recursion_limit)

        state_input = initial_state(message)
        state_input["messages"] = [HumanMessage(content=message)]
        try:
            output = self.graph.invoke(state_input, config)
        except GraphRecursionError:
            answer = (
                "The graph reached its recursion limit and stopped safely. "
                "Please simplify the task."
            )
            return AgentResult(
                answer=answer,
                thread_id=selected_thread,
                steps=[AgentStep(type="guardrail", status="stopped")],
                errors=[answer],
            )

        answer = output.get("final_answer") or self._last_answer(output.get("messages", []))
        raw_steps = output.get("steps", [])
        steps = [AgentStep.model_validate(step) for step in raw_steps]
        tools_used = list(
            dict.fromkeys(
                step.tool
                for step in steps
                if step.type == "tool_call" and step.tool is not None
            )
        )
        return AgentResult(
            answer=answer or "The agent completed without a text response.",
            thread_id=selected_thread,
            tools_used=tools_used,
            steps=steps,
            iterations=output.get("iteration_count", 0),
            errors=list(output.get("errors", [])),
        )

    def get_conversation(self, thread_id: str) -> list[dict[str, str]]:
        snapshot = self.graph.get_state(thread_config(thread_id))
        return public_conversation(list(snapshot.values.get("messages", [])))

    @staticmethod
    def _last_answer(messages: list[Any]) -> str:
        for message in reversed(messages):
            if isinstance(message, AIMessage) and message.content and not message.tool_calls:
                return str(message.content)
        return ""


@lru_cache(maxsize=1)
def get_agent_service() -> AgentService:
    """Lazily build the graph so importing Flask does not call Azure OpenAI."""

    return AgentService()


def run_agent(user_message: str, thread_id: str | None = None) -> dict[str, Any]:
    """Convenient function requested by the tutorial's CLI and web application."""

    return get_agent_service().run_agent(user_message, thread_id).as_dict()


__all__ = ["AgentService", "InputValidationError", "run_agent"]
