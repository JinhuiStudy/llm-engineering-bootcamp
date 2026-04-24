"""Day 9: Ragas로 RAG 품질 측정.

사용:
    python run_ragas.py --golden golden.json --collection day7_rag
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    context_precision,
    context_recall,
    faithfulness,
)

from ai_study.embeddings import embed
from ai_study.llm import chat
from ai_study.vectors import search


def answer_with_context(question: str, collection: str, top_k: int) -> tuple[str, list[str]]:
    qv = embed([question])[0]
    hits = search(collection, qv, top_k=top_k)
    contexts = [(h.payload or {}).get("text", "") for h in hits]
    ctx_block = "\n\n".join(contexts)
    prompt = (
        f"아래 context에만 근거해 답하라. 근거 없으면 '모르겠습니다'.\n\n"
        f"<context>{ctx_block}</context>\n\n<q>{question}</q>"
    )
    return chat("openai", prompt, temperature=0.0, max_tokens=500), contexts


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--golden", type=Path, required=True)
    ap.add_argument("--collection", required=True)
    ap.add_argument("--top-k", type=int, default=5)
    args = ap.parse_args()

    golden = json.loads(args.golden.read_text(encoding="utf-8"))
    rows = {"question": [], "answer": [], "contexts": [], "ground_truth": []}

    for item in golden:
        ans, ctx = answer_with_context(item["question"], args.collection, args.top_k)
        rows["question"].append(item["question"])
        rows["answer"].append(ans)
        rows["contexts"].append(ctx)
        rows["ground_truth"].append(item["ground_truth"])
        print(f"✔ {item['question'][:40]}…")

    ds = Dataset.from_dict(rows)
    result = evaluate(
        ds,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    )
    print("\n── Ragas scores ──")
    print(result)


if __name__ == "__main__":
    main()
