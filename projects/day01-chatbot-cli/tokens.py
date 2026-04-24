"""Day 1 실습: 토큰 감각 잡기.

한국어/영어/숫자 텍스트의 토큰 수 비교.
"""

from __future__ import annotations

from ai_study.tokens import count_tokens, estimate_cost, pricing_table

SAMPLES = {
    "한국어 짧": "안녕하세요 세계",
    "한국어 문단": "오늘은 날씨가 매우 좋아서 산책하러 공원에 갔습니다. 벚꽃이 만개해 있었고, "
                "많은 사람들이 사진을 찍고 있었습니다. 나는 벤치에 앉아 한참을 구경했습니다.",
    "영어 짧": "Hello world",
    "영어 문단": "The quick brown fox jumps over the lazy dog. "
                "This sentence contains every letter in the English alphabet.",
    "코드": "def factorial(n: int) -> int:\n    return 1 if n <= 1 else n * factorial(n - 1)",
    "혼합": "def greet(name: str) -> str:\n    return f'안녕, {name}!'",
    "숫자": "1 2 3 4 5 6 7 8 9 10 100 1000 10000",
}


def main() -> None:
    print("── Token 카운트 (gpt-4o-mini 기준) ──\n")
    print(f"{'Sample':<15} {'Tokens':>7} {'Chars':>7} {'Ch/Tok':>7}")
    print("-" * 42)
    for name, text in SAMPLES.items():
        n_tok = count_tokens(text)
        n_char = len(text)
        ratio = n_char / n_tok if n_tok else 0
        print(f"{name:<15} {n_tok:>7} {n_char:>7} {ratio:>7.2f}")

    print("\n── 10k input + 2k output 비용 비교 ──\n")
    for m in ["gpt-4o-mini", "claude-haiku-4-5", "gemini-2.5-flash",
              "gpt-4o", "claude-sonnet-4-6", "gemini-2.5-pro"]:
        print(estimate_cost(m, 10_000, 2_000))

    print("\n── 전체 가격표 ──\n")
    print(pricing_table())


if __name__ == "__main__":
    main()
