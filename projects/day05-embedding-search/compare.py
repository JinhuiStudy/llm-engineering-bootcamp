"""Day 6: BM25 vs embedding 검색 결과 비교."""

from __future__ import annotations

import argparse
from pathlib import Path

from rank_bm25 import BM25Okapi

from ai_study.embeddings import embed
from ai_study.vectors import search


def tokenize(s: str) -> list[str]:
    return s.lower().split()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="+")
    ap.add_argument("--collection", default="day6_demo")
    ap.add_argument("--corpus", type=Path, required=True,
                    help="BM25용 원본 텍스트 디렉토리 (ingest에 썼던 것)")
    ap.add_argument("--top-k", type=int, default=5)
    args = ap.parse_args()

    q = " ".join(args.query)

    # BM25
    docs = []
    for p in sorted(args.corpus.rglob("*")):
        if p.suffix.lower() in {".md", ".txt"} and p.is_file():
            docs.append((str(p.relative_to(args.corpus)), p.read_text(errors="ignore")))
    bm25 = BM25Okapi([tokenize(t) for _, t in docs])
    scores = bm25.get_scores(tokenize(q))
    bm25_top = sorted(zip(scores, docs), key=lambda x: -x[0])[: args.top_k]

    print("── BM25 ──")
    for score, (src, _) in bm25_top:
        print(f"  {score:.3f}  {src}")

    # Dense
    qv = embed([q])[0]
    dense = search(args.collection, qv, top_k=args.top_k)
    print("\n── Dense (embedding) ──")
    for r in dense:
        p = r.payload or {}
        print(f"  {r.score:.3f}  {p.get('source')} #{p.get('chunk_idx')}")


if __name__ == "__main__":
    main()
