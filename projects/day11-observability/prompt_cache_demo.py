"""Day 12: Anthropic prompt caching 시연.

큰 system prompt를 `cache_control`로 캐시하고, 같은 prefix의 2번째 호출에서
cache_read_input_tokens가 발생하는지 확인.
"""

from __future__ import annotations

import anthropic

from ai_study.config import settings

# 긴 system prompt — Haiku 4.5 / Opus 4.x 최소 캐시 크기는 4096 tokens.
# 약 1200 단어 반복으로 4500+ 토큰 확보 (한국어 기준 여유 있게).
# (pre-digested.md의 "Prompt Caching 최소 토큰" 표 참고)
LONG_SYSTEM = (
    "당신은 엔지니어링 멘토다. 아래 가이드라인을 엄격히 지킨다.\n"
    + "- 규칙: 답변은 간결하고 근거 기반으로. 외부 지식 남용 금지. "
      "Context 없으면 '모르겠다'고 답한다. 코드 예시는 최소화, 설명 우선. "
      "언어는 한국어. 단답 지양, 2-3 문장. "
    * 1200
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
    from ai_study.tokens import count_tokens
    print(f"system prompt 추정 토큰: {count_tokens(LONG_SYSTEM):,} (목표: 4096+)")
    print("첫 호출:", call("RAG를 한 줄로 설명해."))
    print("두번째  :", call("Agent의 핵심을 한 줄로."))
    # 두번째에서 cache_read_input_tokens 가 큰 값이어야 cache hit
    # 최소 토큰 미달이면 silent하게 cache_creation/cache_read 둘 다 0.
