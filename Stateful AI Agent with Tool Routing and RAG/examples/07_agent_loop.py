"""Step 7: an offline scripted model demonstrates agent -> tool -> agent."""

from _bootstrap import ROOT  # noqa: F401
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

from src.graph import build_agent_graph
from src.memory import thread_config
from src.state import initial_state
from tools.calculator import calculator


class ScriptedCalculatorModel:
    def bind_tools(self, _tools):
        return self

    def invoke(self, messages):
        if isinstance(messages[-1], ToolMessage):
            return AIMessage(content=f"18% of 4250 is {messages[-1].content}.")
        return AIMessage(
            content="",
            tool_calls=[
                {"name": "calculator", "args": {"expression": "18% of 4250"}, "id": "call-1"}
            ],
        )


if __name__ == "__main__":
    graph = build_agent_graph(
        model=ScriptedCalculatorModel(), tools=[calculator], checkpointer=InMemorySaver()
    )
    state = initial_state("What is 18% of 4250?")
    from langchain_core.messages import HumanMessage

    state["messages"] = [HumanMessage(content=state["user_query"])]
    result = graph.invoke(state, thread_config("agent-loop-demo"))
    print(result["final_answer"])
    print("Observable steps:", result["steps"])

