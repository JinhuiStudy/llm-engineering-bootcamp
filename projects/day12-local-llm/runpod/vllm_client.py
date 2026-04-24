"""Day 13: RunPod Serverless vLLM endpoint을 OpenAI SDK로 호출.

전제: RunPod에서 worker-vllm template으로 endpoint 배포 완료.
`.env`에 RUNPOD_API_KEY, RUNPOD_ENDPOINT_ID 주입.
"""

from __future__ import annotations

from openai import OpenAI

from ai_study.config import settings


def client() -> OpenAI:
    if not settings.runpod_api_key or not settings.runpod_endpoint_id:
        raise RuntimeError("RUNPOD_* 환경변수 누락")
    base_url = f"https://api.runpod.ai/v2/{settings.runpod_endpoint_id}/openai/v1"
    return OpenAI(base_url=base_url, api_key=settings.runpod_api_key)


def chat_runpod(model: str, user: str, max_tokens: int = 300) -> str:
    r = client().chat.completions.create(
        model=model,  # endpoint 생성 시 지정한 HuggingFace repo (e.g. "Qwen/Qwen2.5-7B-Instruct")
        messages=[{"role": "user", "content": user}],
        max_tokens=max_tokens,
        temperature=0.2,
    )
    return r.choices[0].message.content or ""


if __name__ == "__main__":
    import sys

    model = sys.argv[1] if len(sys.argv) > 1 else "Qwen/Qwen2.5-7B-Instruct"
    msg = " ".join(sys.argv[2:]) or "Explain vector databases in one paragraph."
    print(chat_runpod(model, msg))
