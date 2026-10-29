"""Step 6: Azure OpenAI decides whether to request a registered tool."""

from _bootstrap import ROOT  # noqa: F401
from langchain_core.messages import HumanMessage

from src.llm import get_chat_model
from src.tool_registry import AVAILABLE_TOOLS


def main() -> None:
    try:
        model = get_chat_model().bind_tools(AVAILABLE_TOOLS)
    except ValueError as exc:
        print(f"Setup required: {exc}")
        return
    response = model.invoke([HumanMessage(content="What is 15% of 360?")])
    print("Model content:", response.content)
    print("Requested tool calls:", response.tool_calls)


if __name__ == "__main__":
    main()

