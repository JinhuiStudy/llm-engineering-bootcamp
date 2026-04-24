"""Langfuse 싱글톤 — Day 12부터 사용.

    from ai_study.langfuse_client import get_langfuse, observe
    lf = get_langfuse()
    @observe(name="my_node")
    def ...

Langfuse 키가 없으면 no-op 처리 (에러 없이 스킵).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Callable

from ai_study.config import settings
from ai_study.logging import logger

try:
    from langfuse import Langfuse, observe as _observe  # type: ignore
except Exception:  # noqa: BLE001
    Langfuse = None  # type: ignore
    _observe = None  # type: ignore


@lru_cache(maxsize=1)
def get_langfuse() -> "Langfuse | None":
    if Langfuse is None:
        logger.warning("langfuse not installed — tracing disabled")
        return None
    if not (settings.langfuse_public_key and settings.langfuse_secret_key):
        logger.debug("langfuse keys not set — tracing disabled")
        return None
    return Langfuse(
        public_key=settings.langfuse_public_key,
        secret_key=settings.langfuse_secret_key,
        host=settings.langfuse_host,
    )


def observe(*args, **kwargs) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Langfuse observe decorator의 안전 wrapper.

    Langfuse 미설정이면 decorator는 그냥 원함수를 반환 (no-op).
    """
    if _observe is None or get_langfuse() is None:

        def _noop(fn):
            return fn

        # @observe vs @observe() 둘 다 지원
        if len(args) == 1 and callable(args[0]):
            return args[0]  # type: ignore[return-value]
        return _noop

    return _observe(*args, **kwargs)


def flush() -> None:
    """프로세스 종료 전 호출 권장."""
    lf = get_langfuse()
    if lf is not None:
        try:
            lf.flush()
        except Exception as e:  # noqa: BLE001
            logger.warning(f"langfuse flush failed: {e}")
