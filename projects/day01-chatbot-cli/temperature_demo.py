"""Day 1: Temperature 감각 실험.

동일 프롬프트를 온도 0 / 0.5 / 1.2로 각 3번 호출해 다양성 관찰.
"""

from __future__ import annotations

from ai_study.llm import chat

PROMPT = "Write a single haiku about debugging."


def main() -> None:
    for t in (0.0, 0.5, 1.2):
        print(f"\n── temperature={t} ──")
        for i in range(3):
            try:
                out = chat("openai", PROMPT, temperature=t, max_tokens=80)
                print(f"[{i + 1}] {out.strip()}")
            except Exception as e:  # noqa: BLE001
                print(f"[{i + 1}] ERROR: {e}")


if __name__ == "__main__":
    main()
