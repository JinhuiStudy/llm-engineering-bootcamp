"""Day 13: Ollama를 OpenAI SDK로 호출.

전제: `ollama pull qwen3:8b` 후 `ollama serve` (자동 실행됨).
.env의 OLLAMA_MODEL 로 모델 교체 가능 (기본 qwen3:8b).
"""

from __future__ import annotations

import sys

from ai_study.llm import chat, chat_stream


def main() -> None:
    msg = " ".join(sys.argv[1:]) or "파이썬 GIL을 한 문단으로 설명."
    print("── ollama (local) ──")
    for t in chat_stream("ollama", msg):
        print(t, end="", flush=True)
    print()

    print("\n── openai (cloud) ──")
    print(chat("openai", msg))


if __name__ == "__main__":
    main()
