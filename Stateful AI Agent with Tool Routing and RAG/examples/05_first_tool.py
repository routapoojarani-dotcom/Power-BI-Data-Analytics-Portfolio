"""Step 5: a tool is still an ordinary, directly testable Python function."""

from _bootstrap import ROOT  # noqa: F401

from tools.calculator import calculator

if __name__ == "__main__":
    print("Tool result:", calculator.invoke({"expression": "18% of 4250"}))

