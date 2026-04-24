"""Day 10: Agent state."""

from __future__ import annotations

from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    plan: list[str]
    retrieved: list[dict]
    tool_results: list[dict]
    draft: str
    critique: str
    iterations: int
