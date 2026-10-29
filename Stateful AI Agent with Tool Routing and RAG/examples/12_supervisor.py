"""Step 12: a supervisor routes one request to a specialist."""

from typing import Literal, TypedDict

from _bootstrap import ROOT  # noqa: F401
from langgraph.graph import END, START, StateGraph


class SupervisorState(TypedDict):
    request: str
    specialist: str
    answer: str


def supervisor(state: SupervisorState) -> dict[str, str]:
    request = state["request"].lower()
    if "order" in request:
        specialist = "orders"
    elif "employee" in request:
        specialist = "employees"
    else:
        specialist = "knowledge"
    return {"specialist": specialist}


def route(state: SupervisorState) -> Literal["orders", "employees", "knowledge"]:
    return state["specialist"]  # type: ignore[return-value]


def specialist(name: str):
    return lambda state: {"answer": f"The {name} specialist received: {state['request']}"}


builder = StateGraph(SupervisorState)
builder.add_node("supervisor", supervisor)
for name in ("orders", "employees", "knowledge"):
    builder.add_node(name, specialist(name))
    builder.add_edge(name, END)
builder.add_edge(START, "supervisor")
builder.add_conditional_edges(
    "supervisor", route, {name: name for name in ("orders", "employees", "knowledge")}
)
graph = builder.compile()

if __name__ == "__main__":
    print(graph.invoke({"request": "Check order ORD-1042", "specialist": "", "answer": ""}))
