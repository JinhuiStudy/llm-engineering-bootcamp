"""Day 13: Ollama를 OpenAI SDK로 호출.

전제: `ollama pull qwen2.5:7b` 후 `ollama serve` (자동 실행됨).
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
