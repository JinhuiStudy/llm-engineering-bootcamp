"""Day 8: Dense + BM25 → RRF."""

from __future__ import annotations

from typing import Iterable

from rank_bm25 import BM25Okapi

from ai_study.embeddings import embed
from ai_study.vectors import search


def tokenize(s: str) -> list[str]:
    return s.lower().split()


def rrf_merge(
    ranked_lists: list[list[tuple[str, float]]],
    k: int = 60,
    top_k: int = 5,
) -> list[tuple[str, float]]:
    """각 리스트는 [(doc_id, score)] 순위대로. RRF 점수 합산."""
    scores: dict[str, float] = {}
    for lst in ranked_lists:
        for rank, (doc_id, _) in enumerate(lst, 1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    return ranked[:top_k]


def hybrid_search(
    query: str,
    collection: str,
    corpus: Iterable[tuple[str, str]],  # (doc_id, text)
    top_k: int = 5,
) -> list[tuple[str, float]]:
    corpus_list = list(corpus)
    doc_ids = [d for d, _ in corpus_list]

    # dense
    qv = embed([query])[0]
    dense_hits = search(collection, qv, top_k=top_k * 4)
    dense_ranked = [
        (str((h.payload or {}).get("chunk_idx", i)), h.score)
        for i, h in enumerate(dense_hits)
    ]

    # bm25
    bm25 = BM25Okapi([tokenize(t) for _, t in corpus_list])
    scores = bm25.get_scores(tokenize(query))
    bm25_ranked = sorted(
        [(doc_ids[i], float(scores[i])) for i in range(len(doc_ids))],
        key=lambda x: -x[1],
    )[: top_k * 4]

    return rrf_merge([dense_ranked, bm25_ranked], top_k=top_k)
