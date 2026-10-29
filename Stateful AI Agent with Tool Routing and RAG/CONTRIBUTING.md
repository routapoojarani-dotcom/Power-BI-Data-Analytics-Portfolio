# Contributing

1. Create a branch from the default branch.
2. Keep examples small and introduce concepts in progressive order.
3. Never add real credentials, customer data, or tools that execute arbitrary shell/code.
4. Add deterministic tests; normal CI must not call paid model APIs.
5. Run `pytest` and `ruff check .`.
6. Update `TUTORIAL.md` whenever behavior or commands change.
7. In a pull request, explain the learner impact and include the checks run.

When upgrading LangGraph or LangChain, verify node/edge APIs, message reducers, ToolNode behavior,
checkpointers, interrupts, Azure tool calling, examples, and the “Last verified” note together.

