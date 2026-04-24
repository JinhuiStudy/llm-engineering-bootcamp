"""샌드박스 내 file 조회. ai-study 디렉토리 밖 접근 금지."""

from __future__ import annotations

from pathlib import Path

from ai_study.config import settings

SANDBOX = settings.root.resolve()


def list_files(path: str) -> list[str]:
    p = Path(path).resolve()
    if not str(p).startswith(str(SANDBOX)):
        raise PermissionError(f"{p} is outside sandbox {SANDBOX}")
    if not p.exists():
        raise FileNotFoundError(p)
    if p.is_file():
        return [str(p)]
    return sorted(str(x.relative_to(SANDBOX)) for x in p.iterdir())
