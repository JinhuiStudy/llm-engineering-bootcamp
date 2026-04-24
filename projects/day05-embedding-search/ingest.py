"""Day 6: 문서 → chunk → embed → Qdrant.

사용:
    python ingest.py data/ --collection day6_demo --chunk-size 500 --overlap 50
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ai_study.embeddings import embed, embedding_dim
from ai_study.logging import logger
from ai_study.vectors import UpsertItem, ensure_collection, upsert_texts


def chunk_text(text: str, size: int, overlap: int) -> list[str]:
    """간이 문자 기반 chunk. 실무에서는 RecursiveCharacterTextSplitter 권장."""
    if size <= overlap:
        raise ValueError("size > overlap")
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += size - overlap
    return chunks


def load_dir(path: Path) -> list[tuple[str, str]]:
    """(source, text) 쌍. .md/.txt만."""
    out = []
    for p in sorted(path.rglob("*")):
        if p.suffix.lower() in {".md", ".txt"} and p.is_file():
            out.append((str(p.relative_to(path)), p.read_text(encoding="utf-8", errors="ignore")))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=Path)
    ap.add_argument("--collection", default="day6_demo")
    ap.add_argument("--chunk-size", type=int, default=500)
    ap.add_argument("--overlap", type=int, default=50)
    ap.add_argument("--provider", choices=["openai", "gemini", "local"], default="openai")
    ap.add_argument("--recreate", action="store_true")
    args = ap.parse_args()

    dim = embedding_dim(args.provider)
    ensure_collection(args.collection, dim=dim, recreate=args.recreate)
    logger.info(f"collection={args.collection} dim={dim}")

    all_items: list[UpsertItem] = []
    docs = load_dir(args.path)
    logger.info(f"loaded {len(docs)} files")

    for source, text in docs:
        chunks = chunk_text(text, args.chunk_size, args.overlap)
        vecs = embed(chunks, provider=args.provider)
        for idx, (c, v) in enumerate(zip(chunks, vecs, strict=True)):
            all_items.append(
                UpsertItem(text=c, vector=v, payload={"source": source, "chunk_idx": idx})
            )

    if all_items:
        n = upsert_texts(args.collection, all_items)
        logger.info(f"upserted {n} points")


if __name__ == "__main__":
    main()
