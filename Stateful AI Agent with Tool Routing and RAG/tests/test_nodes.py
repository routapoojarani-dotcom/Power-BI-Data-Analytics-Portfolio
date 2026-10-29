from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from src.memory import thread_config
from src.nodes import create_agent_node, create_tool_node
from src.state import AgentState, initial_state
from tests.fakes import FakeToolModel
from tools.calculator import calculator


def test_agent_node_records_observable_tool_call(tutorial_settings) -> None:
    state = initial_state("Calculate 15% of 200")
    state["messages"] = [HumanMessage(content=state["user_query"])]
    update = create_agent_node(FakeToolModel(), [calculator], tutorial_settings)(state)
    assert update["tool_calls"][0]["name"] == "calculator"
    assert update["steps"][-1]["type"] == "tool_call"


def test_tool_node_executes_requested_tool(tutorial_settings) -> None:
    state = initial_state("Calculate")
    from langchain_core.messages import AIMessage

    state["messages"] = [
        AIMessage(
            content="",
            tool_calls=[
                {"name": "calculator", "args": {"expression": "2 + 3"}, "id": "calc-test"}
            ],
        )
    ]
    # Current ToolNode execution receives LangGraph runtime context from a compiled graph.
    workflow = StateGraph(AgentState)
    workflow.add_node("tools", create_tool_node([calculator], tutorial_settings))
    workflow.add_edge(START, "tools")
    workflow.add_edge("tools", END)
    graph = workflow.compile(checkpointer=InMemorySaver())
    result = graph.invoke(state, thread_config("tool-node-test"))
    assert result["tool_results"][0]["content"] == "5"
    assert result["steps"][-2]["status"] == "success"
