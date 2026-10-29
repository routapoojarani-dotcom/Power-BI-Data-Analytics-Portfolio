"""Step 4: a conditional edge chooses one of two paths."""

from typing import Literal, TypedDict

from _bootstrap import ROOT  # noqa: F401
from langgraph.graph import END, START, StateGraph


class RouteState(TypedDict):
    question: str
    answer: str


def classify(state: RouteState) -> dict:
    return {}


def route(state: RouteState) -> Literal["calculation", "general"]:
    has_number = any(character.isdigit() for character in state["question"])
    return "calculation" if has_number else "general"


def calculation(_state: RouteState) -> dict:
    return {"answer": "Send this request to a calculator."}


def general(_state: RouteState) -> dict:
    return {"answer": "Answer this as a general question."}


workflow = StateGraph(RouteState)
workflow.add_node("classify", classify)
workflow.add_node("calculation", calculation)
workflow.add_node("general", general)
workflow.add_edge(START, "classify")
workflow.add_conditional_edges(
    "classify", route, {"calculation": "calculation", "general": "general"}
)
workflow.add_edge("calculation", END)
workflow.add_edge("general", END)
graph = workflow.compile()

if __name__ == "__main__":
    print(graph.invoke({"question": "What is 12% of 4250?", "answer": ""})["answer"])
