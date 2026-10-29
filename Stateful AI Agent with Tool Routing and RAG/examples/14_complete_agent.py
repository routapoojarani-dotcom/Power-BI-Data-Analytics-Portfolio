"""Step 14: run the same complete graph used by Flask and the CLI."""

from _bootstrap import ROOT  # noqa: F401

from src.agent_service import AgentService


def main() -> None:
    try:
        service = AgentService()
    except ValueError as exc:
        print(f"Setup required: {exc}")
        return
    result = service.run_agent(
        "According to company policy, how many annual leave days does E102 have remaining?",
        "complete-agent-demo",
    )
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()

