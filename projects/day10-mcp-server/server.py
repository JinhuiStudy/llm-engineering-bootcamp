"""Day 11: 자체 MCP 서버 (FastMCP 고수준 API).

Claude Desktop 연결:
  ~/Library/Application Support/Claude/claude_desktop_config.json 에 추가:

  {
    "mcpServers": {
      "ai-study": {
        "command": "uv",
        "args": ["run", "python", "/절대경로/projects/day10-mcp-server/server.py"]
      }
    }
  }
"""

from __future__ import annotations

from pathlib import Path

from mcp.server.fastmcp import FastMCP

from ai_study.config import settings

mcp = FastMCP("ai-study")


@mcp.tool()
def list_projects() -> list[str]:
    """ai-study/projects 하위 디렉토리 목록."""
    p = settings.root / "projects"
    return sorted(x.name for x in p.iterdir() if x.is_dir())


@mcp.tool()
def read_note(name: str) -> str:
    """notes/ 디렉토리 파일 읽기. 경로 탈출 방지."""
    notes = (settings.root / "notes").resolve()
    target = (notes / name).resolve()
    if not str(target).startswith(str(notes)):
        raise ValueError("outside notes/")
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(name)
    return target.read_text(encoding="utf-8")


@mcp.tool()
def search_pdfs(query: str, top_k: int = 5) -> list[dict]:
    """Day 7 RAG collection에 질의."""
    from ai_study.embeddings import embed
    from ai_study.vectors import search as vsearch

    qv = embed([query])[0]
    hits = vsearch("day7_rag", qv, top_k=top_k)
    return [
        {
            "score": h.score,
            "source": (h.payload or {}).get("source"),
            "page": (h.payload or {}).get("page"),
            "text": (h.payload or {}).get("text", "")[:500],
        }
        for h in hits
    ]


@mcp.resource("notes://keywords")
def keywords_resource() -> str:
    """notes/keywords.md 를 MCP resource로 노출."""
    return (settings.root / "notes" / "keywords.md").read_text(encoding="utf-8")


@mcp.prompt()
def daily_standup(day: int) -> str:
    """오늘 진도 회고용 프롬프트 템플릿."""
    return (
        f"오늘은 Day {day}이다. 다음에 답하라:\n"
        f"1) 체크리스트 중 완료한 것\n2) 남은 것\n3) 내일 최우선\n4) 막힌 점 한 줄"
    )


if __name__ == "__main__":
    mcp.run()
