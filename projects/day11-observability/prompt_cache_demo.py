"""Day 12: Anthropic prompt caching 시연.

큰 system prompt를 `cache_control`로 캐시하고, 같은 prefix의 2번째 호출에서
cache_read_input_tokens가 발생하는지 확인.
"""

from __future__ import annotations

import anthropic

from ai_study.config import settings

# 1000+ tokens 정도의 긴 system prompt (캐시 가능 최소 크기 넘겨야 함)
LONG_SYSTEM = (
    "당신은 엔지니어링 멘토다. 아래 가이드라인을 엄격히 지킨다.\n" + "- 규칙 " * 400
)


def call(user: str) -> dict:
    client = anthropic.Anthropic()
    r = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=256,
        system=[
            {
                "type": "text",
                "text": LONG_SYSTEM,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": user}],
    )
    u = r.usage
    return {
        "input": u.input_tokens,
        "output": u.output_tokens,
        "cache_creation": getattr(u, "cache_creation_input_tokens", 0),
        "cache_read": getattr(u, "cache_read_input_tokens", 0),
    }


if __name__ == "__main__":
    print("첫 호출:", call("RAG를 한 줄로 설명해."))
    print("두번째  :", call("Agent의 핵심을 한 줄로."))
    # 두번째에서 cache_read_input_tokens 가 큰 값이어야 cache hit
