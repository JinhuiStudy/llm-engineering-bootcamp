"""Day 4: 이력서 PDF → ResumeSummary 추출.

사용:
    python extract.py samples/resume1.pdf
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from pydantic import ValidationError
from pypdf import PdfReader

from ai_study.config import settings
from ai_study.logging import logger
from schemas import ResumeSummary

OUT_DIR = Path(__file__).parent / "outputs"
OUT_DIR.mkdir(exist_ok=True)


def pdf_to_text(path: Path) -> str:
    reader = PdfReader(str(path))
    return "\n\n".join(p.extract_text() or "" for p in reader.pages)


def extract_openai(text: str) -> ResumeSummary:
    """OpenAI Structured Outputs (strict)."""
    from openai import OpenAI

    client = OpenAI()
    r = client.chat.completions.parse(
        model=settings.openai_model if "gpt-4o" in settings.openai_model else "gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extract the resume information faithfully."},
            {"role": "user", "content": text},
        ],
        response_format=ResumeSummary,
    )
    parsed = r.choices[0].message.parsed
    assert parsed is not None, "parsing returned None"
    return parsed


def extract_anthropic(text: str, max_retries: int = 2) -> ResumeSummary:
    """Anthropic — tool_use trick로 strict JSON."""
    import anthropic

    client = anthropic.Anthropic()
    schema = ResumeSummary.model_json_schema()
    tools = [
        {
            "name": "record_resume",
            "description": "Record extracted resume data.",
            "input_schema": schema,
        }
    ]
    attempt = 0
    last_error: str | None = None
    while attempt <= max_retries:
        user = text if last_error is None else (
            f"이전 시도에서 검증 실패: {last_error}\n다시 정확히 작성.\n\n{text}"
        )
        r = client.messages.create(
            model=settings.anthropic_model,
            max_tokens=2048,
            system="Extract the resume accurately. Call record_resume with the data.",
            tools=tools,
            tool_choice={"type": "tool", "name": "record_resume"},
            messages=[{"role": "user", "content": user}],
        )
        tool_uses = [b for b in r.content if getattr(b, "type", "") == "tool_use"]
        if not tool_uses:
            last_error = "no tool_use block returned"
            attempt += 1
            continue
        try:
            return ResumeSummary.model_validate(tool_uses[0].input)
        except ValidationError as e:
            last_error = str(e)
            attempt += 1
            logger.warning(f"validation failed (attempt {attempt}): {e}")
    raise RuntimeError(f"failed after retries: {last_error}")


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python extract.py <pdf_path> [--provider openai|anthropic]")
        return 2
    path = Path(sys.argv[1])
    provider = "openai"
    if "--provider" in sys.argv:
        provider = sys.argv[sys.argv.index("--provider") + 1]

    text = pdf_to_text(path)
    logger.info(f"{path.name}: {len(text)} chars")

    result = extract_openai(text) if provider == "openai" else extract_anthropic(text)
    out = OUT_DIR / f"{path.stem}.json"
    out.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    print(json.dumps(result.model_dump(), ensure_ascii=False, indent=2))
    print(f"\n→ {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
