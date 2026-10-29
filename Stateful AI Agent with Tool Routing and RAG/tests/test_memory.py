from langgraph.checkpoint.memory import InMemorySaver

from src.graph import build_agent_graph
from src.memory import thread_config
from src.state import initial_state
from tests.fakes import FakeToolModel
from tools.calculator import calculator


def call(graph, text: str, thread: str):
    from langchain_core.messages import HumanMessage

    state = initial_state(text)
    state["messages"] = [HumanMessage(content=text)]
    return graph.invoke(state, thread_config(thread))


def test_threads_are_isolated(tutorial_settings) -> None:
    graph = build_agent_graph(
        model=FakeToolModel(),
        tools=[calculator],
        checkpointer=InMemorySaver(),
        settings=tutorial_settings,
    )
    call(graph, "Hello", "a")
    call(graph, "Hello again", "a")
    call(graph, "Hello", "b")
    assert len(graph.get_state(thread_config("a")).values["messages"]) == 4
    assert len(graph.get_state(thread_config("b")).values["messages"]) == 2


def test_thread_id_is_required() -> None:
    import pytest

    with pytest.raises(ValueError, match="thread_id"):
        thread_config("")

