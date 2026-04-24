"""토큰 카운팅 + 간이 비용 추정."""

from __future__ import annotations

from dataclasses import dataclass

import tiktoken


# 2026년 초 기준 대략치. $/1M tokens. 실제 청구는 provider 대시보드 확인.
PRICING: dict[str, tuple[float, float]] = {
    # OpenAI
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "o1": (15.00, 60.00),
    "o1-mini": (3.00, 12.00),
    # Anthropic
    "claude-opus-4-7": (15.00, 75.00),
    "claude-sonnet-4-6": (3.00, 15.00),
    "claude-haiku-4-5": (0.80, 4.00),
    # Gemini
    "gemini-2.5-pro": (1.25, 10.00),
    "gemini-2.5-flash": (0.075, 0.30),
}

# tiktoken은 OpenAI 전용. 다른 provider는 근사치로 동일 encoding 사용.
_ENCODER_CACHE: dict[str, tiktoken.Encoding] = {}


def _enc_for(model: str) -> tiktoken.Encoding:
    key = model
    if key in _ENCODER_CACHE:
        return _ENCODER_CACHE[key]
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        enc = tiktoken.get_encoding("cl100k_base")
    _ENCODER_CACHE[key] = enc
    return enc


def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """근사 토큰 수. OpenAI는 정확, 다른 건 ±15%."""
    return len(_enc_for(model).encode(text))


@dataclass
class CostEstimate:
    model: str
    input_tokens: int
    output_tokens: int
    input_usd: float
    output_usd: float
    total_usd: float

    def __str__(self) -> str:
        return (
            f"{self.model}: "
            f"{self.input_tokens}→{self.output_tokens} tokens "
            f"= ${self.total_usd:.4f} "
            f"(in ${self.input_usd:.4f} + out ${self.output_usd:.4f})"
        )


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> CostEstimate:
    """model의 input/output 토큰 수로 달러 비용 추정."""
    in_rate, out_rate = PRICING.get(model, (0.0, 0.0))
    in_usd = input_tokens * in_rate / 1_000_000
    out_usd = output_tokens * out_rate / 1_000_000
    return CostEstimate(
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        input_usd=in_usd,
        output_usd=out_usd,
        total_usd=in_usd + out_usd,
    )


def pricing_table() -> str:
    lines = [f"{'Model':<25} {'$/1M in':>10} {'$/1M out':>10}"]
    for m, (i, o) in sorted(PRICING.items()):
        lines.append(f"{m:<25} {i:>10.4f} {o:>10.4f}")
    return "\n".join(lines)


if __name__ == "__main__":
    # python -m ai_study.tokens
    print(pricing_table())
    text = "안녕하세요 세계. Hello world. 123 testing."
    print(f"\nSample text tokens (gpt-4o-mini): {count_tokens(text)}")
    est = estimate_cost("claude-sonnet-4-6", 10_000, 2_000)
    print(est)
