import json

import pytest

from tools.calculator import calculate_expression, calculator
from tools.current_datetime import get_current_datetime
from tools.employee_lookup import employee_lookup, find_employee
from tools.knowledge_search import lexical_search, search_documents
from tools.order_lookup import find_order, order_lookup


@pytest.mark.parametrize(
    ("expression", "expected"),
    [("18% of 4250", 765), ("25 * 14", 350), ("(8 + 2) / 5", 2)],
)
def test_calculator(expression: str, expected: float) -> None:
    assert calculate_expression(expression) == expected


def test_calculator_rejects_code_execution() -> None:
    with pytest.raises(ValueError):
        calculate_expression("__import__('os').system('whoami')")


def test_calculator_tool_interface() -> None:
    assert calculator.invoke({"expression": "15% of 200"}) == "30"


def test_employee_lookup_success_and_business_error() -> None:
    assert find_employee("e102")["department"] == "Finance"
    missing = json.loads(employee_lookup.invoke({"employee_id": "E999"}))
    assert missing == {"found": False, "employee_id": "E999", "error": "Employee not found"}


def test_order_lookup() -> None:
    assert find_order("ord-1042")["status"] == "Shipped"
    assert json.loads(order_lookup.invoke({"order_id": "ORD-404"}))["found"] is False


def test_current_datetime_and_invalid_timezone() -> None:
    assert get_current_datetime("UTC")["timezone"] == "UTC"
    with pytest.raises(ValueError, match="Unknown IANA timezone"):
        get_current_datetime("Not/AZone")


def test_knowledge_search_is_grounded() -> None:
    results = lexical_search("annual leave allowance", top_k=1)
    assert results[0]["source"] == "sample_company_policy.txt"
    assert "25 days" in results[0]["content"]
    assert search_documents("annual leave")["found"] is True

