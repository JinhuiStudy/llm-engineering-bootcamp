"""Safe arithmetic — AST 화이트리스트. 임의 코드 실행 불가."""

from __future__ import annotations

import ast
import operator as op

_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}


def _walk(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_walk(node.left), _walk(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_walk(node.operand))
    raise ValueError(f"disallowed node: {ast.dump(node)}")


def calculator(expression: str) -> dict:
    tree = ast.parse(expression, mode="eval")
    return {"expression": expression, "result": _walk(tree.body)}
