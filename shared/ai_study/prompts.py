"""Prompt template helpers — Jinja2 기반 최소 래퍼.

사용:
    from ai_study.prompts import render
    msg = render("rag_answer", context=ctx, question=q)

prompt 파일 경로 탐색 우선순위:
1. 같은 프로젝트의 `prompts/` 디렉토리
2. `ROOT/prompts/`
3. 환경변수 `PROMPT_DIR`
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from ai_study.config import settings


@lru_cache(maxsize=1)
def _env() -> Environment:
    search = []
    if os.getenv("PROMPT_DIR"):
        search.append(Path(os.environ["PROMPT_DIR"]))
    # cwd/prompts (day별 프로젝트)
    search.append(Path.cwd() / "prompts")
    # root/prompts
    search.append(settings.root / "prompts")
    loader = FileSystemLoader([str(p) for p in search if p.exists()] or [str(settings.root)])
    return Environment(
        loader=loader,
        undefined=StrictUndefined,  # 누락 변수면 에러 (silent 금지)
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render(template_name: str, **kwargs) -> str:
    """`{template_name}.txt` 또는 `{template_name}.j2` 를 찾아 렌더."""
    env = _env()
    for ext in (".txt", ".j2", ""):
        name = template_name + ext
        try:
            return env.get_template(name).render(**kwargs)
        except Exception:  # noqa: BLE001
            continue
    raise FileNotFoundError(f"No prompt template for '{template_name}' in search paths")


def render_string(template: str, **kwargs) -> str:
    """인라인 template string 렌더."""
    return _env().from_string(template).render(**kwargs)
