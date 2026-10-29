"""Run a local fake agent and pretty-print its transparent state."""

import json

from _bootstrap import ROOT  # noqa: F401
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

from src.graph import build_agent_graph
from src.memory import thread_config
from src.state import initial_state
from tools.order_lookup import order_lookup


class OrderModel:
    def bind_tools(self, _tools):
        return self

    def invoke(self, messages):
        if isinstance(messages[-1], ToolMessage):
            return AIMessage(content="Order lookup completed using the observed tool result.")
        return AIMessage(
            content="",
            tool_calls=[
                {"name": "order_lookup", "args": {"order_id": "ORD-1042"}, "id": "order-1"}
            ],
        )


if __name__ == "__main__":
    graph = build_agent_graph(
        model=OrderModel(), tools=[order_lookup], checkpointer=InMemorySaver()
    )
    state = initial_state("What is the status of order ORD-1042?")
    from langchain_core.messages import HumanMessage

    state["messages"] = [HumanMessage(content=state["user_query"])]
    graph.invoke(state, thread_config("inspect-state"))
    snapshot = graph.get_state(thread_config("inspect-state"))
    printable = {key: value for key, value in snapshot.values.items() if key != "messages"}
    printable["message_types"] = [type(message).__name__ for message in snapshot.values["messages"]]
    print(json.dumps(printable, indent=2, default=str))

