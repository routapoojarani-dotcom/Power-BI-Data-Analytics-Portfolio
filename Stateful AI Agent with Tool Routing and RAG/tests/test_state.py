from src.state import initial_state


def test_initial_state_is_easy_to_inspect() -> None:
    state = initial_state("hello")
    assert state["user_query"] == "hello"
    assert state["iteration_count"] == 0
    assert state["tool_calls"] == []
    assert state["steps"][0]["type"] == "received"

