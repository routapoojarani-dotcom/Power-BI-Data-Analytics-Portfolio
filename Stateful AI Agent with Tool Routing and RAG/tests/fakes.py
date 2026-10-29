"""Small fake chat models keep tests deterministic and free of paid API calls."""

from __future__ import annotations

import json

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


class FakeToolModel:
    def __init__(self) -> None:
        self.calls = 0

    def bind_tools(self, _tools):
        return self

    def invoke(self, messages):
        self.calls += 1
        last = messages[-1]
        if isinstance(last, ToolMessage):
            if last.name == "employee_lookup":
                record = json.loads(str(last.content))
                if "increase" in self._latest_user_text(messages).lower() and record.get("found"):
                    return AIMessage(
                        content="",
                        tool_calls=[
                            {
                                "name": "calculator",
                                "args": {"expression": f"{record['annual_salary']} * 1.07"},
                                "id": "calc-after-employee",
                            }
                        ],
                    )
                return AIMessage(content=f"Employee lookup result: {last.content}")
            if last.name == "calculator":
                return AIMessage(content=f"The calculated result is {last.content}.")
            if last.name == "order_lookup":
                return AIMessage(content=f"Order lookup result: {last.content}")
            return AIMessage(content=f"Tool result: {last.content}")

        query = self._latest_user_text(messages).lower()
        if "employee" in query or "e102" in query or "e999" in query:
            employee_id = "E999" if "e999" in query else "E102"
            return AIMessage(
                content="",
                tool_calls=[
                    {"name": "employee_lookup", "args": {"employee_id": employee_id}, "id": "emp-1"}
                ],
            )
        if "order" in query or "ord-" in query:
            return AIMessage(
                content="",
                tool_calls=[
                    {"name": "order_lookup", "args": {"order_id": "ORD-1042"}, "id": "ord-1"}
                ],
            )
        if "%" in query or "calculate" in query:
            return AIMessage(
                content="",
                tool_calls=[
                    {"name": "calculator", "args": {"expression": "15% of 200"}, "id": "calc-1"}
                ],
            )
        return AIMessage(content="Hello from the deterministic fake model.")

    @staticmethod
    def _latest_user_text(messages) -> str:
        for message in reversed(messages):
            if isinstance(message, HumanMessage):
                return str(message.content)
        return ""


class LoopingModel:
    def __init__(self) -> None:
        self.calls = 0

    def bind_tools(self, _tools):
        return self

    def invoke(self, _messages):
        self.calls += 1
        return AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "calculator",
                    "args": {"expression": "1 + 1"},
                    "id": f"loop-{self.calls}",
                }
            ],
        )

