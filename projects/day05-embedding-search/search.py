"""Day 6: 쿼리 → top-k 유사 chunk."""

from __future__ import annotations

import argparse

from ai_study.embeddings import embed
from ai_study.vectors import search


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="+")
    ap.add_argument("--collection", default="day6_demo")
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--provider", choices=["openai", "gemini", "local"], default="openai")
    args = ap.parse_args()

    q = " ".join(args.query)
    qv = embed([q], provider=args.provider)[0]
    results = search(args.collection, qv, top_k=args.top_k)

    print(f"── query: {q!r}\n")
    for i, r in enumerate(results, 1):
        payload = r.payload or {}
        print(f"[{i}] score={r.score:.4f}  source={payload.get('source')}  chunk_idx={payload.get('chunk_idx')}")
        print(f"    {payload.get('text', '')[:200]!r}\n")


if __name__ == "__main__":
    main()
