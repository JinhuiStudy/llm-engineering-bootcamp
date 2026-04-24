"""Day 8: Cross-encoder rerank."""

from __future__ import annotations

from functools import lru_cache


@lru_cache(maxsize=1)
def _cross_encoder(name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
    from sentence_transformers import CrossEncoder

    return CrossEncoder(name)


def rerank(query: str, candidates: list[str], top_k: int = 5) -> list[tuple[int, float]]:
    """candidates의 index와 rerank score를 반환. top_k 개."""
    model = _cross_encoder()
    pairs = [(query, c) for c in candidates]
    scores = model.predict(pairs)
    ranked = sorted(enumerate(scores), key=lambda x: -x[1])
    return [(i, float(s)) for i, s in ranked[:top_k]]
