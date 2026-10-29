"""Interactive, multi-turn CLI for the complete Azure OpenAI agent."""

from uuid import uuid4

from _bootstrap import ROOT  # noqa: F401

from src.agent_service import AgentService


def main() -> None:
    print("LangGraph Agent\n===============")
    try:
        service = AgentService()
    except ValueError as exc:
        print(f"\nSetup error: {exc}")
        return

    thread_id = str(uuid4())
    print(f"Thread: {thread_id}\nType 'exit' or 'quit' to stop.\n")
    while True:
        try:
            user_message = input("You:\n").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if user_message.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        try:
            result = service.run_agent(user_message, thread_id)
        except ValueError as exc:
            print(f"\nInput error: {exc}\n")
            continue
        print(f"\nAgent:\n{result.answer}")
        if result.tools_used:
            print("\nTools used:", ", ".join(result.tools_used))
        print()


if __name__ == "__main__":
    main()

