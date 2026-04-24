"""Day 7: 기본 RAG 파이프라인.

사용:
    python rag.py "질문" --collection day7_rag
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ai_study.embeddings import embed
from ai_study.llm import chat
from ai_study.vectors import search

PROMPT_TEMPLATE = (Path(__file__).parent / "prompts" / "rag_template.txt").read_text(
    encoding="utf-8"
) if (Path(__file__).parent / "prompts" / "rag_template.txt").exists() else """\
아래 context에만 근거하여 답하라. 근거가 없으면 "모르겠습니다"라고 답하라.
사용한 근거를 [{source}:p{page}] 형태로 인용하라.

<context>
{context}
</context>

<question>
{question}
</question>
"""


def build_context(hits: list) -> str:
    return "\n\n".join(
        f"[{(h.payload or {}).get('source')}:p{(h.payload or {}).get('page')}]\n"
        f"{(h.payload or {}).get('text', '')}"
        for h in hits
    )


def answer(question: str, collection: str, top_k: int = 5) -> tuple[str, list]:
    qv = embed([question])[0]
    hits = search(collection, qv, top_k=top_k)
    context = build_context(hits)
    prompt = PROMPT_TEMPLATE.replace("{context}", context).replace("{question}", question)
    response = chat("anthropic", prompt, temperature=0.0, max_tokens=1024)
    return response, hits


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="+")
    ap.add_argument("--collection", default="day7_rag")
    ap.add_argument("--top-k", type=int, default=5)
    args = ap.parse_args()

    q = " ".join(args.question)
    resp, hits = answer(q, args.collection, args.top_k)
    print(f"── question: {q}\n")
    print("── retrieved ──")
    for h in hits:
        p = h.payload or {}
        print(f"  {h.score:.3f}  {p.get('source')}:p{p.get('page')}")
    print("\n── answer ──")
    print(resp)


if __name__ == "__main__":
    main()
