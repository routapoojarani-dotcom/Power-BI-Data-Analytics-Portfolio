"""Run a small, paid-call-free evaluation of expected tool-selection behavior."""

import json

from _bootstrap import ROOT  # noqa: F401

from tools.calculator import calculate_expression
from tools.employee_lookup import find_employee
from tools.knowledge_search import search_documents
from tools.order_lookup import find_order


def deterministic_selector(query: str) -> str | None:
    lowered = query.lower()
    if "%" in query or "calculate" in lowered:
        return "calculator"
    if "e10" in lowered or "employee" in lowered:
        return "employee_lookup"
    if "ord-" in lowered or "order" in lowered:
        return "order_lookup"
    if "policy" in lowered or "leave" in lowered:
        return "knowledge_search"
    return None


if __name__ == "__main__":
    cases = json.loads((ROOT / "data" / "evaluation_cases.json").read_text(encoding="utf-8"))
    passed = 0
    for case in cases:
        actual = deterministic_selector(case["query"])
        ok = actual == case["expected_tool"]
        passed += int(ok)
        print(f"{'PASS' if ok else 'FAIL'} | expected={case['expected_tool']} actual={actual}")
    # Also exercise deterministic capabilities that LLM-behavior tests can mock around.
    assert calculate_expression("15% of 200") == 30
    assert find_employee("E102")["found"]
    assert find_order("ORD-1042")["found"]
    assert search_documents("annual leave")["found"]
    print(f"\nTool-selection accuracy: {passed}/{len(cases)} ({passed / len(cases):.0%})")

