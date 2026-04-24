"""Day 1-2: 3-Provider CLI chatbot.

사용:
    python chat.py --provider openai "안녕"
    python chat.py --provider anthropic --stream "파이썬 제너레이터 설명"
    python chat.py --compare "오늘 날씨 어때?"
"""

from __future__ import annotations

import argparse
import sys

from ai_study.llm import chat, chat_stream
from ai_study.logging import logger
from ai_study.tokens import count_tokens, estimate_cost

PROVIDERS = ["openai", "anthropic", "gemini", "ollama"]


def run_once(provider: str, msg: str, system: str | None, stream: bool) -> None:
    print(f"\n── [{provider}] ──")
    if stream:
        out_chars = 0
        for token in chat_stream(provider, msg, system=system):  # type: ignore[arg-type]
            print(token, end="", flush=True)
            out_chars += len(token)
        print()
    else:
        r = chat(provider, msg, system=system)  # type: ignore[arg-type]
        print(r)


def run_compare(msg: str, system: str | None) -> None:
    # 3사 병렬 호출 비교. 단순 구현 — 실제로는 asyncio 권장.
    for p in ["openai", "anthropic", "gemini"]:
        try:
            run_once(p, msg, system, stream=False)
        except Exception as e:
            logger.error(f"{p}: {e}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("message", nargs="*", help="유저 메시지")
    parser.add_argument("--provider", "-p", choices=PROVIDERS, default="openai")
    parser.add_argument("--system", "-s", default=None, help="system prompt")
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("--compare", action="store_true", help="3사 동시 비교")
    parser.add_argument("--estimate", action="store_true", help="요청 비용 추정만")
    args = parser.parse_args()

    msg = " ".join(args.message) or sys.stdin.read().strip()
    if not msg:
        parser.error("메시지 없음")

    if args.estimate:
        in_tok = count_tokens(msg)
        # 답변 토큰은 알 수 없으니 보수적으로 512
        est = estimate_cost("gpt-4o-mini", in_tok, 512)
        print(est)
        return 0

    if args.compare:
        run_compare(msg, args.system)
    else:
        run_once(args.provider, msg, args.system, args.stream)
    return 0


if __name__ == "__main__":
    sys.exit(main())
