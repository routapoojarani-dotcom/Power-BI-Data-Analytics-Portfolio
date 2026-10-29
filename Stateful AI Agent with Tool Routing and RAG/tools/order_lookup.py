"""Read-only order lookup backed by local sample JSON."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from langchain_core.tools import tool

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "orders.json"


@lru_cache(maxsize=1)
def _orders() -> dict[str, dict[str, object]]:
    records = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {str(item["order_id"]).upper(): item for item in records}


def find_order(order_id: str) -> dict[str, object]:
    if not isinstance(order_id, str) or not order_id.strip():
        return {"found": False, "error": "order_id is required"}
    normalized = order_id.strip().upper()
    record = _orders().get(normalized)
    if record is None:
        return {"found": False, "order_id": normalized, "error": "Order not found"}
    return {"found": True, **record}


@tool("order_lookup")
def order_lookup(order_id: str) -> str:
    """Look up a sample order by ID, for example `ORD-1042`. This tool is read-only."""

    return json.dumps(find_order(order_id), ensure_ascii=False)

