"""Day 13: 3가지 백엔드 속도/비용 벤치."""

from __future__ import annotations

import time
from dataclasses import dataclass

from ai_study.llm import chat
from ai_study.tokens import count_tokens, estimate_cost

QUESTIONS = [
    "RAG를 한 문단으로 설명하라.",
    "Transformer의 self-attention이 왜 효과적인가?",
    "Vector DB를 왜 쓰는가?",
]


@dataclass
class Result:
    provider: str
    avg_latency: float
    tokens_total: int
    estimated_cost_usd: float


def bench(provider: str, model: str | None = None) -> Result:
    total_t, total_tok = 0.0, 0
    for q in QUESTIONS:
        t0 = time.time()
        out = chat(provider, q, model=model, max_tokens=256)  # type: ignore[arg-type]
        total_t += time.time() - t0
        total_tok += count_tokens(q, model or "gpt-4o-mini") + count_tokens(out, model or "gpt-4o-mini")
    avg = total_t / len(QUESTIONS)
    est = estimate_cost(model or "gpt-4o-mini", total_tok // 2, total_tok // 2)
    return Result(provider=provider, avg_latency=avg, tokens_total=total_tok, estimated_cost_usd=est.total_usd)


if __name__ == "__main__":
    for p in ["openai", "anthropic", "ollama"]:
        try:
            r = bench(p)
            print(f"{r.provider:<10} avg={r.avg_latency:.2f}s  tok={r.tokens_total}  ${r.estimated_cost_usd:.4f}")
        except Exception as e:  # noqa: BLE001
            print(f"{p:<10} ERROR: {e}")
