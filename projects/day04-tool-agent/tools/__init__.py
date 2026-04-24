"""Tools 구현 모음. 각 tool은 JSON-직렬화 가능한 값을 반환한다."""

from __future__ import annotations

from .calculator import calculator
from .file_io import list_files
from .weather import get_weather
from .web_search import web_search

REGISTRY = {
    "get_weather": get_weather,
    "calculator": calculator,
    "web_search": web_search,
    "list_files": list_files,
}


def dispatch(name: str, args: dict) -> dict | str | list:
    """Tool 이름으로 실행. 에러는 문자열로 반환 (LLM에 전달 가능하게)."""
    fn = REGISTRY.get(name)
    if fn is None:
        return f"ERROR: unknown tool '{name}'"
    try:
        return fn(**args)
    except Exception as e:  # noqa: BLE001
        return f"ERROR: {e.__class__.__name__}: {e}"
