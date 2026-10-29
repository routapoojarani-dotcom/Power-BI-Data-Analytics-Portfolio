"""Step 10: pause a simulated cancellation until a human approves or rejects it."""

from typing import TypedDict

from _bootstrap import ROOT  # noqa: F401
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class ApprovalState(TypedDict):
    order_id: str
    outcome: str


def request_approval(state: ApprovalState) -> dict[str, str]:
    approved = interrupt(
        {"question": f"Approve simulated cancellation of {state['order_id']}?", "risk": "high"}
    )
    outcome = "Simulated cancellation approved." if approved else "Cancellation stopped."
    return {"outcome": outcome}


builder = StateGraph(ApprovalState)
builder.add_node("approval", request_approval)
builder.add_edge(START, "approval")
builder.add_edge("approval", END)
graph = builder.compile(checkpointer=InMemorySaver())

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "approval-demo"}}
    paused = graph.invoke({"order_id": "ORD-1042", "outcome": ""}, config)
    print("Paused for human:", paused["__interrupt__"][0].value)
    resumed = graph.invoke(Command(resume=True), config)
    print("After approval:", resumed["outcome"])

