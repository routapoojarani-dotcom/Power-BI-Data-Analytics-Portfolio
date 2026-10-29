"""Step 8: the same thread can read previous messages; a new thread cannot."""

import re

from _bootstrap import ROOT  # noqa: F401
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph


def remember_name(state: MessagesState) -> dict:
    latest = str(state["messages"][-1].content)
    match = re.search(r"name is (\w+)", latest, re.IGNORECASE)
    if match:
        answer = f"I will remember that your name is {match.group(1)} in this thread."
    else:
        names = [
            re.search(r"name is (\w+)", str(message.content), re.IGNORECASE)
            for message in state["messages"]
            if isinstance(message, HumanMessage)
        ]
        remembered = next((item.group(1) for item in reversed(names) if item), None)
        answer = f"Your name is {remembered}." if remembered else "I do not know your name."
    return {"messages": [AIMessage(content=answer)]}


builder = StateGraph(MessagesState)
builder.add_node("remember", remember_name)
builder.add_edge(START, "remember")
builder.add_edge("remember", END)
graph = builder.compile(checkpointer=InMemorySaver())

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "conversation-a"}}
    graph.invoke({"messages": [HumanMessage(content="My name is Asha.")]}, config)
    same_thread = graph.invoke({"messages": [HumanMessage(content="What is my name?")]}, config)
    other_thread = graph.invoke(
        {"messages": [HumanMessage(content="What is my name?")]},
        {"configurable": {"thread_id": "conversation-b"}},
    )
    print("Conversation A:", same_thread["messages"][-1].content)
    print("Conversation B:", other_thread["messages"][-1].content)

