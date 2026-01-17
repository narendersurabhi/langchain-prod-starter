from __future__ import annotations

import datetime as dt
import ast
import operator
import re
from typing import Any

from langchain_core.runnables import Runnable, RunnableLambda
from langchain_core.tools import tool


_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_node(node.operand)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    raise ValueError("Unsupported expression")


@tool
def calculator(expression: str) -> str:
    """Evaluate a simple arithmetic expression."""
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        return "Invalid expression"
    try:
        parsed = ast.parse(expression, mode="eval")
        result = _eval_node(parsed.body)
    except Exception:
        return "Error"
    return str(result)


@tool
def current_time(_: str) -> str:
    """Return the current UTC time."""
    return dt.datetime.utcnow().isoformat() + "Z"


@tool
def search(query: str) -> str:
    """Search stub tool for demo."""
    return f"Search results for '{query}' are unavailable in offline mode."


def build_agent() -> Runnable:
    tools = {
        "calculator": calculator,
        "current_time": current_time,
        "search": search,
    }

    def run(task: str) -> dict[str, Any]:
        tool_calls: list[dict[str, Any]] = []
        if re.search(r"\d", task) and re.search(r"[+\-*/]", task):
            tool_name = "calculator"
            arg = re.sub(r"[^0-9+\-*/(). ]", "", task)
        elif "time" in task.lower():
            tool_name = "current_time"
            arg = "now"
        else:
            tool_name = "search"
            arg = task

        tool = tools[tool_name]
        output = tool.invoke(arg)
        tool_calls.append({"tool": tool_name, "input": arg, "output": output})
        return {"result": output, "tool_calls": tool_calls}

    return RunnableLambda(run)
