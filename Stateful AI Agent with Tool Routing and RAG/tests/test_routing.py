from langchain_core.messages import AIMessage

from src.config import Settings
from src.routing import should_continue


def test_routes_tool_call_to_tools(tutorial_settings: Settings) -> None:
    message = AIMessage(
        content="", tool_calls=[{"name": "calculator", "args": {"expression": "1+1"}, "id": "1"}]
    )
    assert should_continue({"messages": [message], "tool_calls": []}, tutorial_settings) == "tools"


def test_routes_plain_response_to_end(tutorial_settings: Settings) -> None:
    assert should_continue({"messages": [AIMessage(content="done")]}, tutorial_settings) == "end"


def test_routes_excess_tool_calls_to_limit(tutorial_settings: Settings) -> None:
    message = AIMessage(
        content="", tool_calls=[{"name": "calculator", "args": {"expression": "1+1"}, "id": "1"}]
    )
    calls = [{"name": "calculator"}] * 11
    state = {"messages": [message], "tool_calls": calls}
    assert should_continue(state, tutorial_settings) == "limit"
