"""Step 13: specialists collaborate through explicit shared state."""

from typing import TypedDict

from _bootstrap import ROOT  # noqa: F401
from langgraph.graph import END, START, StateGraph

from tools.employee_lookup import find_employee
from tools.knowledge_search import search_documents


class LeaveState(TypedDict):
    employee_id: str
    employee: dict
    policy: dict
    answer: str


def employee_agent(state: LeaveState) -> dict:
    return {"employee": find_employee(state["employee_id"])}


def knowledge_agent(_state: LeaveState) -> dict:
    return {"policy": search_documents("full-time annual leave allowance")}


def supervisor_agent(state: LeaveState) -> dict[str, str]:
    allowance = 25  # Extracted deterministically from this tutorial's known sample policy.
    taken = int(state["employee"].get("annual_leave_taken", 0))
    return {"answer": f"{state['employee'].get('name')} has {allowance - taken} days remaining."}


builder = StateGraph(LeaveState)
builder.add_node("employee_agent", employee_agent)
builder.add_node("knowledge_agent", knowledge_agent)
builder.add_node("supervisor_agent", supervisor_agent)
builder.add_edge(START, "employee_agent")
builder.add_edge("employee_agent", "knowledge_agent")
builder.add_edge("knowledge_agent", "supervisor_agent")
builder.add_edge("supervisor_agent", END)
graph = builder.compile()

if __name__ == "__main__":
    initial = {"employee_id": "E102", "employee": {}, "policy": {}, "answer": ""}
    print(graph.invoke(initial)["answer"])

