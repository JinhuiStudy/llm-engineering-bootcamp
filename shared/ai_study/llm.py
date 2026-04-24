"""Provider-agnostic chat wrapper.

3사(OpenAI/Anthropic/Gemini) + Ollama를 단일 인터페이스로. Day 2부터 쓸 공용 코드.
구조화 출력이나 tool use가 필요한 단계에서는 provider SDK를 직접 쓰는 게 낫다 —
이건 "어떤 provider든 일단 텍스트 한 번 받아와" 용도.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Literal

from ai_study.config import settings
from ai_study.logging import logger
from ai_study.retry import with_retry

Provider = Literal["openai", "anthropic", "gemini", "ollama"]


@with_retry
def chat(
    provider: Provider,
    user: str,
    *,
    system: str | None = None,
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int = 1024,
) -> str:
    """한 번의 chat 호출로 최종 텍스트만 반환.

    스트리밍/tool use/structured output이 필요하면 provider SDK 직접 써라.
    """
    temperature = settings.default_temperature if temperature is None else temperature

    if provider == "openai":
        from openai import OpenAI

        client = OpenAI()
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})
        r = client.chat.completions.create(
            model=model or settings.openai_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        text = r.choices[0].message.content or ""
        logger.debug(
            f"openai usage: in={r.usage.prompt_tokens} out={r.usage.completion_tokens}"
        )
        return text

    if provider == "anthropic":
        import anthropic

        client = anthropic.Anthropic()
        r = client.messages.create(
            model=model or settings.anthropic_model,
            max_tokens=max_tokens,
            system=system or "",
            messages=[{"role": "user", "content": user}],
            temperature=temperature,
        )
        text = r.content[0].text if r.content else ""
        logger.debug(
            f"anthropic usage: in={r.usage.input_tokens} out={r.usage.output_tokens}"
        )
        return text

    if provider == "gemini":
        from google import genai

        client = genai.Client(api_key=settings.google_api_key)
        config: dict = {"temperature": temperature, "max_output_tokens": max_tokens}
        if system:
            config["system_instruction"] = system
        r = client.models.generate_content(
            model=model or settings.gemini_model,
            contents=user,
            config=config,
        )
        return r.text or ""

    if provider == "ollama":
        # OpenAI 호환 엔드포인트 — openai SDK 그대로 재사용
        from openai import OpenAI

        client = OpenAI(base_url=settings.ollama_base_url, api_key="ollama")
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})
        r = client.chat.completions.create(
            model=model or settings.ollama_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return r.choices[0].message.content or ""

    raise ValueError(f"Unknown provider: {provider}")


def chat_stream(
    provider: Provider,
    user: str,
    *,
    system: str | None = None,
    model: str | None = None,
    temperature: float | None = None,
    max_tokens: int = 1024,
) -> Iterator[str]:
    """스트리밍. 토큰(혹은 chunk) 단위 yield. CLI 체감용."""
    temperature = settings.default_temperature if temperature is None else temperature

    if provider == "openai" or provider == "ollama":
        from openai import OpenAI

        base_url = settings.ollama_base_url if provider == "ollama" else None
        api_key = "ollama" if provider == "ollama" else None
        client = OpenAI(base_url=base_url, api_key=api_key) if base_url else OpenAI()
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})
        stream = client.chat.completions.create(
            model=model
            or (settings.ollama_model if provider == "ollama" else settings.openai_model),
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                yield delta
        return

    if provider == "anthropic":
        import anthropic

        client = anthropic.Anthropic()
        with client.messages.stream(
            model=model or settings.anthropic_model,
            max_tokens=max_tokens,
            system=system or "",
            messages=[{"role": "user", "content": user}],
            temperature=temperature,
        ) as stream:
            for text in stream.text_stream:
                yield text
        return

    if provider == "gemini":
        from google import genai

        client = genai.Client(api_key=settings.google_api_key)
        config: dict = {"temperature": temperature, "max_output_tokens": max_tokens}
        if system:
            config["system_instruction"] = system
        for chunk in client.models.generate_content_stream(
            model=model or settings.gemini_model,
            contents=user,
            config=config,
        ):
            if chunk.text:
                yield chunk.text
        return

    raise ValueError(f"Unknown provider: {provider}")


if __name__ == "__main__":
    # 빠른 smoke test: python -m ai_study.llm
    import sys

    prov = sys.argv[1] if len(sys.argv) > 1 else "openai"
    msg = " ".join(sys.argv[2:]) or "In one sentence, why is the sky blue?"
    print(f"[{prov}] {msg}\n→", end=" ", flush=True)
    for token in chat_stream(prov, msg):  # type: ignore[arg-type]
        print(token, end="", flush=True)
    print()
