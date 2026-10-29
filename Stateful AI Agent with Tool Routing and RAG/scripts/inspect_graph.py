"""Print a Mermaid representation of the complete graph without calling Azure."""

from _bootstrap import ROOT  # noqa: F401
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver

from src.graph import build_agent_graph


class NoOpModel:
    def bind_tools(self, _tools):
        return self

    def invoke(self, _messages):
        return AIMessage(content="Inspection only")


if __name__ == "__main__":
    graph = build_agent_graph(model=NoOpModel(), checkpointer=InMemorySaver())
    print(graph.get_graph().draw_mermaid())

