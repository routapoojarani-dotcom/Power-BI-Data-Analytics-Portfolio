"""Read-only employee lookup backed by local sample JSON."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from langchain_core.tools import tool

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "employees.json"


@lru_cache(maxsize=1)
def _employees() -> dict[str, dict[str, object]]:
    records = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {str(item["employee_id"]).upper(): item for item in records}


def find_employee(employee_id: str) -> dict[str, object]:
    if not isinstance(employee_id, str) or not employee_id.strip():
        return {"found": False, "error": "employee_id is required"}
    normalized = employee_id.strip().upper()
    record = _employees().get(normalized)
    if record is None:
        return {"found": False, "employee_id": normalized, "error": "Employee not found"}
    return {"found": True, **record}


@tool("employee_lookup")
def employee_lookup(employee_id: str) -> str:
    """Look up a sample employee by ID, for example `E102`. This tool is read-only."""

    return json.dumps(find_employee(employee_id), ensure_ascii=False)

