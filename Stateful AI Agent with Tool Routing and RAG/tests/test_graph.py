from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

from src.config import Settings
from src.graph import build_agent_graph
from src.memory import thread_config
from src.state import initial_state
from tests.fakes import FakeToolModel, LoopingModel
from tools.calculator import calculator
from tools.employee_lookup import employee_lookup


class OneToolModel:
    def __init__(self, name: str, args: dict) -> None:
        self.name = name
        self.args = args

    def bind_tools(self, _tools):
        return self

    def invoke(self, messages):
        if isinstance(messages[-1], ToolMessage):
            return AIMessage(content=f"Observed: {messages[-1].content}")
        return AIMessage(
            content="",
            tool_calls=[{"name": self.name, "args": self.args, "id": "one-tool"}],
        )


@tool("unavailable_service")
def unavailable_service() -> str:
    """Simulate an unexpected backend outage."""

    raise RuntimeError("private database connection detail")


def invoke(graph, query: str, thread: str = "test"):
    state = initial_state(query)
    state["messages"] = [HumanMessage(content=query)]
    return graph.invoke(state, thread_config(thread))


def test_complete_tool_loop_reaches_end(tutorial_settings) -> None:
    graph = build_agent_graph(
        model=FakeToolModel(),
        tools=[calculator],
        checkpointer=InMemorySaver(),
        settings=tutorial_settings,
    )
    result = invoke(graph, "Calculate 15% of 200")
    assert result["final_answer"] == "The calculated result is 30."
    assert result["iteration_count"] == 2


def test_agent_can_call_multiple_tools(tutorial_settings) -> None:
    graph = build_agent_graph(
        model=FakeToolModel(),
        tools=[employee_lookup, calculator],
        checkpointer=InMemorySaver(),
        settings=tutorial_settings,
    )
    result = invoke(graph, "What is employee E102's salary after a 7% increase?")
    assert [call["name"] for call in result["tool_calls"]] == ["employee_lookup", "calculator"]
    assert "85600" in result["final_answer"]


def test_expected_business_error_does_not_crash(tutorial_settings) -> None:
    graph = build_agent_graph(
        model=FakeToolModel(),
        tools=[employee_lookup],
        checkpointer=InMemorySaver(),
        settings=tutorial_settings,
    )
    result = invoke(graph, "Find employee E999")
    assert "Employee not found" in result["final_answer"]


def test_iteration_guardrail_stops_loop() -> None:
    settings = Settings(
        max_agent_iterations=2,
        max_tool_calls=10,
        flask_secret_key="test",
        _env_file=None,
    )
    graph = build_agent_graph(
        model=LoopingModel(),
        tools=[calculator],
        checkpointer=InMemorySaver(),
        settings=settings,
    )
    result = invoke(graph, "loop")
    assert "stopped safely" in result["final_answer"]
    assert result["iteration_count"] == 2


def test_invalid_tool_arguments_become_safe_observation(tutorial_settings) -> None:
    graph = build_agent_graph(
        model=OneToolModel("calculator", {}),
        tools=[calculator],
        checkpointer=InMemorySaver(),
        settings=tutorial_settings,
    )
    result = invoke(graph, "Use calculator without arguments", "invalid-tool-input")
    assert "Tool input error" in result["final_answer"]
    assert result["tool_results"][0]["status"] == "error"


def test_unexpected_tool_failure_does_not_leak_details(tutorial_settings) -> None:
    graph = build_agent_graph(
        model=OneToolModel("unavailable_service", {}),
        tools=[unavailable_service],
        checkpointer=InMemorySaver(),
        settings=tutorial_settings,
    )
    result = invoke(graph, "Use unavailable service", "failed-tool")
    assert "failed unexpectedly" in result["final_answer"]
    assert "private database" not in result["final_answer"]
