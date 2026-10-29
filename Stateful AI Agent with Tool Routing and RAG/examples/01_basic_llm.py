"""Step 1: one user message goes directly to Azure OpenAI."""

from _bootstrap import ROOT  # noqa: F401
from langchain_core.messages import HumanMessage

from src.llm import get_chat_model


def main() -> None:
    try:
        model = get_chat_model()
    except ValueError as exc:
        print(f"Setup required: {exc}")
        return
    response = model.invoke([HumanMessage(content="Explain an AI agent in one sentence.")])
    print(response.content)


if __name__ == "__main__":
    main()

