"""Multi-query: 쿼리 1개 → 변형 N개."""

from __future__ import annotations

from ai_study.llm import chat

PROMPT = """원 질문을 서로 다른 관점/어휘로 {n}개의 검색 쿼리로 다시 쓰라.
한 줄에 하나씩, 번호나 불릿 없이 출력하라.

원 질문: {q}
변형 쿼리들:"""


def multi_query(query: str, n: int = 3) -> list[str]:
    raw = chat("openai", PROMPT.format(q=query, n=n), temperature=0.4, max_tokens=400)
    lines = [ln.strip() for ln in raw.strip().splitlines() if ln.strip()]
    return lines[:n] if lines else [query]
