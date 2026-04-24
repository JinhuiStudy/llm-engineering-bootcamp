"""Day 9: Ragas v0.2+ API로 RAG 품질 측정.

사용:
    python run_ragas.py --golden golden.json --collection day7_rag
    python run_ragas.py --golden golden.json --collection day7_rag --sample 20  # CI용

v0.2 변경점:
- `EvaluationDataset.from_list(...)` (신) + `evaluate(dataset, metrics)` 패턴
- Metric은 클래스 (Faithfulness / ResponseRelevancy / LLMContextPrecisionWithReference / LLMContextRecall)
- judge_llm은 LangchainLLMWrapper로 감싸 주입
- judge는 testee와 **다른 provider** 권장 (self-preference bias 회피)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from langchain_anthropic import ChatAnthropic
from ragas import EvaluationDataset, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import (
    Faithfulness,
    LLMContextPrecisionWithReference,
    LLMContextRecall,
    ResponseRelevancy,
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
        "아래 context에만 근거해 답하라. 근거 없으면 '모르겠습니다'.\n\n"
        f"<context>{ctx_block}</context>\n\n<q>{question}</q>"
    )
    # testee는 OpenAI
    return chat("openai", prompt, temperature=0.0, max_tokens=500), contexts


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--golden", type=Path, required=True)
    ap.add_argument("--collection", required=True)
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--sample", type=int, default=None, help="N개만 샘플링 (CI mini-eval)")
    args = ap.parse_args()

    golden = json.loads(args.golden.read_text(encoding="utf-8"))
    if args.sample:
        golden = golden[: args.sample]

    # Ragas v0.2 — EvaluationDataset 구조
    samples: list[dict] = []
    for item in golden:
        ans, ctx = answer_with_context(item["question"], args.collection, args.top_k)
        samples.append(
            {
                "user_input": item["question"],
                "response": ans,
                "retrieved_contexts": ctx,
                "reference": item.get("ground_truth", ""),
            }
        )
        print(f"✔ {item['question'][:40]}…")

    dataset = EvaluationDataset.from_list(samples)

    # Judge: testee(openai)와 다른 provider
    judge_llm = LangchainLLMWrapper(
        ChatAnthropic(model="claude-sonnet-4-6", temperature=0)
    )

    result = evaluate(
        dataset=dataset,
        metrics=[
            Faithfulness(llm=judge_llm),
            ResponseRelevancy(llm=judge_llm),
            LLMContextPrecisionWithReference(llm=judge_llm),
            LLMContextRecall(llm=judge_llm),
        ],
    )
    print("\n── Ragas scores ──")
    df = result.to_pandas()
    print(df)
    # 평균 요약
    print("\n── 평균 ──")
    for col in (
        "faithfulness",
        "answer_relevancy",
        "llm_context_precision_with_reference",
        "context_recall",
    ):
        if col in df.columns:
            print(f"  {col}: {df[col].mean():.3f}")


if __name__ == "__main__":
    main()
