"""Day 7: PDF → chunk → Qdrant."""

from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfReader

from ai_study.embeddings import embed, embedding_dim
from ai_study.logging import logger
from ai_study.vectors import UpsertItem, ensure_collection, upsert_texts


def pdf_chunks(path: Path, size: int, overlap: int) -> list[tuple[str, int]]:
    """페이지별로 text 뽑고, 그 안에서 chunk. (text, page) 반환."""
    reader = PdfReader(str(path))
    out: list[tuple[str, int]] = []
    for page_idx, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        if not text.strip():
            continue
        start = 0
        while start < len(text):
            end = min(start + size, len(text))
            out.append((text[start:end], page_idx))
            if end == len(text):
                break
            start += size - overlap
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf_dir", type=Path)
    ap.add_argument("--collection", default="day7_rag")
    ap.add_argument("--chunk-size", type=int, default=800)
    ap.add_argument("--overlap", type=int, default=100)
    ap.add_argument("--recreate", action="store_true")
    args = ap.parse_args()

    ensure_collection(args.collection, dim=embedding_dim("openai"), recreate=args.recreate)

    items: list[UpsertItem] = []
    for pdf in sorted(args.pdf_dir.glob("*.pdf")):
        logger.info(f"ingest: {pdf.name}")
        chunks = pdf_chunks(pdf, args.chunk_size, args.overlap)
        texts = [c for c, _ in chunks]
        vecs = embed(texts)
        for (c, page), v in zip(chunks, vecs, strict=True):
            items.append(
                UpsertItem(
                    text=c,
                    vector=v,
                    payload={"source": pdf.name, "page": page},
                )
            )

    if items:
        n = upsert_texts(args.collection, items)
        logger.info(f"✔ upserted {n}")


if __name__ == "__main__":
    main()
