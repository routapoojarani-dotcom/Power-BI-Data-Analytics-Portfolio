"""Step 2: the smallest useful StateGraph: START -> greet -> END."""

from typing import TypedDict

from _bootstrap import ROOT  # noqa: F401
from langgraph.graph import END, START, StateGraph


class GreetingState(TypedDict):
    name: str
    message: str


def greet_node(state: GreetingState) -> dict[str, str]:
    return {"message": f"Hello, {state['name']}!"}


workflow = StateGraph(GreetingState)
workflow.add_node("greet", greet_node)
workflow.add_edge(START, "greet")
workflow.add_edge("greet", END)
graph = workflow.compile()

if __name__ == "__main__":
    print(graph.invoke({"name": "Learner", "message": ""})["message"])

