"""AI Study Bootcamp — 연결 점검.

.env에 API 키 넣은 후 실행:
    make verify
또는
    cd shared && uv run python ../setup/2-verify.py

각 provider에 최소한의 호출을 보내고 응답을 요약한다.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
NC = "\033[0m"


def ok(msg: str) -> None:
    print(f"{GREEN}✔{NC} {msg}")


def fail(msg: str) -> None:
    print(f"{RED}✗{NC} {msg}")


def warn(msg: str) -> None:
    print(f"{YELLOW}⚠{NC} {msg}")


def check_openai() -> bool:
    key = os.getenv("OPENAI_API_KEY", "")
    if not key or key.startswith("sk-..."):
        fail("OPENAI_API_KEY 없음")
        return False
    try:
        from openai import OpenAI

        client = OpenAI()
        r = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": "Say 'ok' in one word."}],
            max_completion_tokens=10,
        )
        txt = (r.choices[0].message.content or "").strip()
        ok(f"OpenAI [{r.model}] → {txt!r}  ({r.usage.total_tokens} tokens)")
        return True
    except Exception as e:
        fail(f"OpenAI 실패: {e}")
        return False


def check_anthropic() -> bool:
    key = os.getenv("ANTHROPIC_API_KEY", "")
    if not key or key.startswith("sk-ant-...") or key == "sk-ant-...":
        fail("ANTHROPIC_API_KEY 없음")
        return False
    try:
        import anthropic

        client = anthropic.Anthropic()
        r = client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5"),
            max_tokens=20,
            messages=[{"role": "user", "content": "Say 'ok' in one word."}],
        )
        txt = r.content[0].text.strip() if r.content else ""
        ok(
            f"Anthropic [{r.model}] → {txt!r}  "
            f"(in={r.usage.input_tokens} out={r.usage.output_tokens})"
        )
        return True
    except Exception as e:
        fail(f"Anthropic 실패: {e}")
        return False


def check_gemini() -> bool:
    key = os.getenv("GOOGLE_API_KEY", "")
    if not key:
        fail("GOOGLE_API_KEY 없음")
        return False
    try:
        from google import genai

        client = genai.Client(api_key=key)
        r = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents="Say 'ok' in one word.",
        )
        ok(f"Gemini [{os.getenv('GEMINI_MODEL')}] → {r.text.strip()!r}")
        return True
    except Exception as e:
        fail(f"Gemini 실패: {e}")
        return False


def check_qdrant() -> bool:
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    try:
        import httpx

        r = httpx.get(f"{url}/collections", timeout=3)
        if r.status_code == 200:
            ok(f"Qdrant {url} → {r.json().get('result', {}).get('collections', [])}")
            return True
        fail(f"Qdrant {url} → HTTP {r.status_code}")
    except Exception as e:
        warn(f"Qdrant {url} 연결 불가 ({e.__class__.__name__}) — Day 6 전까지는 OK")
    return False


def check_ollama() -> bool:
    url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1").replace("/v1", "")
    try:
        import httpx

        r = httpx.get(f"{url}/api/tags", timeout=3)
        if r.status_code == 200:
            models = [m["name"] for m in r.json().get("models", [])]
            ok(f"Ollama {url} → {models or '(모델 없음, Day 13에 pull)'}")
            return True
    except Exception as e:
        warn(f"Ollama {url} 미실행 ({e.__class__.__name__}) — Day 13 전까지는 OK")
    return False


def main() -> int:
    print("── LLM Provider ──")
    results = [
        check_openai(),
        check_anthropic(),
        check_gemini(),
    ]
    print("\n── Local infra (optional) ──")
    check_qdrant()
    check_ollama()

    print()
    passed = sum(results)
    total = len(results)
    if passed == total:
        print(f"{GREEN}── {passed}/{total} provider 통과. Day 1 시작 가능. ──{NC}")
        return 0
    print(f"{RED}── {passed}/{total} provider 실패. .env 점검 후 재시도. ──{NC}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
