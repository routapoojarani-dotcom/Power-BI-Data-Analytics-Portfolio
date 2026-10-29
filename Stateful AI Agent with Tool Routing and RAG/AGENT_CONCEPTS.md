# Agentic AI Concepts — Plain-English Reference

| Term | Simple definition | In this repository |
|---|---|---|
| Agent | A system in which a model can choose actions, observe results, and repeat until done. | The compiled graph in `src/graph.py`. |
| LLM | The language model that interprets the request and decides the next response/action. | Azure OpenAI through `src/llm.py`. |
| Chatbot | Usually a one-request/one-response interaction. It may have history but does not necessarily act. | `examples/01_basic_llm.py` is the closest simple form. |
| Workflow | A path chosen by the programmer. | `examples/04_conditional_edges.py`. |
| Tool | A named, described function the model may request. | Functions in `tools/`. |
| Tool call | A structured request containing a tool name, arguments, and ID. | Stored on `AIMessage.tool_calls`. |
| Tool result | The returned observation linked to a tool-call ID. | A LangChain `ToolMessage`. |
| Observation | Information returned after an action. The agent uses it to decide again. | Employee JSON, order JSON, calculation text, or retrieved excerpts. |
| Graph | Nodes plus connections defining allowed execution. | The `StateGraph` builder. |
| StateGraph | A LangGraph graph whose nodes read shared state and return partial updates. | `StateGraph(AgentState)`. |
| Node | A function that performs one kind of work. | `agent`, `tools`, and `limit`. |
| Edge | A connection saying what runs next. | `tools → agent` is a normal edge. |
| Conditional edge | A connection selected by a routing function. | Agent routes to tools, limit, or end. |
| State | The current snapshot of information carried through the graph. | `AgentState` in `src/state.py`. |
| State transition | The change produced by a node before the next step. | Adding an `AIMessage` or `ToolMessage`. |
| Reducer | A rule for merging a state update with existing state. | `add_messages` appends/updates messages. |
| Agent loop | Decide → act → observe → decide again. | `agent → tools → agent`. |
| Iteration | One model/agent-node decision in this tutorial. | Counted by `iteration_count`. |
| Recursion limit | LangGraph runtime protection limiting graph steps. It is not Python function recursion here. | Set per invocation in `thread_config`. |
| Guardrail | A technical or policy boundary restricting behavior. | Input length, safe calculator, iteration/tool limits. |
| Memory | Previous information passed back to the model. It does not retrain the model. | Checkpointed messages in a thread. |
| Short-term memory | Context limited to one conversation/thread. | Messages associated with one `thread_id`. |
| Long-term memory | Information deliberately stored across threads or users. | Discussed, but not implemented in this beginner app. |
| Thread | A logical conversation identified by a stable ID. | Browser session or CLI UUID. |
| Checkpoint | A snapshot of graph state at a super-step—like a saved game. | In-memory or SQLite saver. |
| Checkpointer | Component that saves and retrieves checkpoints. | `InMemorySaver` / `SqliteSaver`. |
| Persistence | Keeping state beyond one invocation; durable persistence can survive a process restart. | Optional SQLite file. |
| Interrupt | A deliberate pause that surfaces a value and waits for external input. | Human-approval example. |
| Command | A LangGraph instruction used to resume, route, or update execution. | `Command(resume=True)`. |
| Human-in-the-loop | A person reviews or approves a step before execution continues. | Simulated order cancellation. |
| Structured output | Data constrained to an explicit schema rather than arbitrary prose. | `AgentResult` and tool-call schemas. |
| Supervisor | A coordinator that assigns work to a specialist. | `examples/12_supervisor.py`. |
| Specialist agent | An agent or node with a narrow responsibility and tool context. | Employee, order, and knowledge specialists. |
| Multi-agent system | Multiple specialized agent components coordinating on a task. | Simplified example 13. |
| RAG | Retrieve relevant documents, then supply them to a model for a grounded answer. | `knowledge_search` capability. |
| Agentic RAG | An agent chooses when to retrieve and may combine retrieval with other tools. | Policy + employee + calculator scenario. |
| Tool registry | A central list of allowed capabilities and their descriptions. | `src/tool_registry.py`. |
| Tool error | An expected business error or unexpected system failure during an action. | “Employee not found” vs database outage. |
| Idempotency | Repeating an operation has no additional unwanted effect. Essential when retries/replays happen. | Required for any future write tool. |
| Observability | Safe evidence of what ran, how long, and whether it succeeded. | Public `steps` plus debug logs. |

## Four sentences to remember

1. **The LLM decides.** It interprets the goal and may request a tool.
2. **The tool acts.** It calculates, retrieves, or changes something within its permission.
3. **State remembers.** It carries messages, observations, counters, and progress.
4. **The graph controls flow.** It defines allowed nodes, routes, loops, stops, and persistence.

