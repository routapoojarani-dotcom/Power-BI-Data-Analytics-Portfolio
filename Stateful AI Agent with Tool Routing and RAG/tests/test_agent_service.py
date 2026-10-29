import pytest
from langgraph.checkpoint.memory import InMemorySaver

from src.agent_service import AgentService
from src.graph import build_agent_graph
from src.guardrails import InputValidationError
from tests.fakes import FakeToolModel
from tools.calculator import calculator


def service(tutorial_settings):
    graph = build_agent_graph(
        model=FakeToolModel(),
        tools=[calculator],
        checkpointer=InMemorySaver(),
        settings=tutorial_settings,
    )
    return AgentService(graph=graph, settings=tutorial_settings)


def test_structured_result_has_tools_and_public_steps(tutorial_settings) -> None:
    result = service(tutorial_settings).run_agent("Calculate 15% of 200", "abc123")
    assert result.thread_id == "abc123"
    assert result.tools_used == ["calculator"]
    expected_steps = {"received", "tool_call", "tool_result", "response"}
    assert {step.type for step in result.steps} >= expected_steps
    assert "reasoning" not in result.model_dump_json().lower()


def test_empty_input_is_rejected(tutorial_settings) -> None:
    with pytest.raises(InputValidationError):
        service(tutorial_settings).run_agent("   ", "abc")


def test_service_exposes_multi_turn_conversation(tutorial_settings) -> None:
    agent_service = service(tutorial_settings)
    agent_service.run_agent("Hello", "same-thread")
    conversation = agent_service.get_conversation("same-thread")
    assert conversation == [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hello from the deterministic fake model."},
    ]
