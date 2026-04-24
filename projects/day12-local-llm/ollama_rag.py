"""Day 13: Day 7 RAG pipeline을 Ollama로 교체. Embedding은 OpenAI 유지 (무료 tier 한계),
Generation만 로컬.
"""

from __future__ import annotations

import argparse

from ai_study.embeddings import embed
from ai_study.llm import chat
from ai_study.vectors import search

PROMPT = """아래 context에만 근거해 답하라. 없으면 '모르겠습니다'.
<context>
{ctx}
</context>

<q>{q}</q>"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="+")
    ap.add_argument("--collection", default="day7_rag")
    ap.add_argument("--provider", choices=["ollama", "openai", "anthropic"], default="ollama")
    args = ap.parse_args()

    q = " ".join(args.question)
    qv = embed([q])[0]
    hits = search(args.collection, qv, top_k=5)
    ctx = "\n\n".join((h.payload or {}).get("text", "") for h in hits)
    print(chat(args.provider, PROMPT.format(ctx=ctx, q=q), temperature=0.0))


if __name__ == "__main__":
    main()
