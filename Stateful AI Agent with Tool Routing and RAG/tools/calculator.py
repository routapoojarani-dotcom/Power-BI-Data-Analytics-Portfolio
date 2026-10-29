"""A safe calculator tool: arithmetic is parsed, never executed as Python code."""

from __future__ import annotations

import ast
import operator
import re
from collections.abc import Callable

from langchain_core.tools import tool

_BINARY_OPERATORS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
_UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}
_PERCENT_OF = re.compile(
    r"^\s*(-?\d+(?:\.\d+)?)\s*%\s+of\s+(-?\d+(?:\.\d+)?)\s*$",
    re.IGNORECASE,
)


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left, right = _evaluate(node.left), _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and (abs(right) > 10 or abs(left) > 1_000_000):
            raise ValueError("Exponent is outside the safe calculator range.")
        return _BINARY_OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        return _UNARY_OPERATORS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Only numbers and +, -, *, /, %, **, and parentheses are allowed.")


def calculate_expression(expression: str) -> float:
    """Calculate one safe arithmetic expression or a phrase such as `18% of 4250`."""

    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("expression must be a non-empty string")
    if len(expression) > 200:
        raise ValueError("expression is too long")

    percent_match = _PERCENT_OF.fullmatch(expression)
    if percent_match:
        percentage, value = map(float, percent_match.groups())
        result = (percentage / 100.0) * value
        return int(result) if result.is_integer() else round(result, 10)

    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree)
    except (SyntaxError, TypeError, ZeroDivisionError) as exc:
        raise ValueError(f"Invalid calculation: {exc}") from exc
    if abs(result) > 1e15:
        raise ValueError("result is outside the safe calculator range")
    return int(result) if result.is_integer() else round(result, 10)


@tool("calculator")
def calculator(expression: str) -> str:
    """Safely calculate arithmetic. Input examples: `25 * 14` or `18% of 4250`."""

    return str(calculate_expression(expression))
