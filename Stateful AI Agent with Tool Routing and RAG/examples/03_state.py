"""Step 3: two nodes read and update the same state."""

from typing import TypedDict

from _bootstrap import ROOT  # noqa: F401
from langgraph.graph import END, START, StateGraph


class CounterState(TypedDict):
    value: int
    history: list[str]


def add_ten(state: CounterState) -> dict:
    return {"value": state["value"] + 10, "history": [*state["history"], "added 10"]}


def double(state: CounterState) -> dict:
    return {"value": state["value"] * 2, "history": [*state["history"], "doubled"]}


workflow = StateGraph(CounterState)
workflow.add_node("add_ten", add_ten)
workflow.add_node("double", double)
workflow.add_edge(START, "add_ten")
workflow.add_edge("add_ten", "double")
workflow.add_edge("double", END)
graph = workflow.compile()

if __name__ == "__main__":
    print(graph.invoke({"value": 5, "history": []}))

