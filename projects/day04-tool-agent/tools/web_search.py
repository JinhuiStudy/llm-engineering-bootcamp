"""Tavily (유료 무료 1000/mo) 우선, 없으면 간이 scraping."""

from __future__ import annotations

from ai_study.config import settings


def web_search(query: str, max_results: int = 3) -> list[dict]:
    if settings.tavily_api_key:
        from tavily import TavilyClient

        client = TavilyClient(api_key=settings.tavily_api_key)
        r = client.search(query=query, max_results=max_results)
        return [
            {"title": it["title"], "url": it["url"], "content": it.get("content", "")[:400]}
            for it in r.get("results", [])
        ]

    # Fallback: DuckDuckGo HTML scrape. 실무에서는 권장 X.
    import httpx
    from urllib.parse import quote

    r = httpx.get(
        f"https://duckduckgo.com/html/?q={quote(query)}",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10,
    )
    # 파싱 로직은 직접 작성 (실습 과제)
    return [{"title": "TODO", "url": "", "content": r.text[:200]}][:max_results]
