"""Day 12: Langfuse @observe decorator 최소 예제.

전제: Langfuse self-host 기동 + .env에 LANGFUSE_* 키 주입 완료.
"""

from __future__ import annotations

from langfuse import Langfuse, observe

from ai_study.config import settings

# 자동 초기화 (env LANGFUSE_HOST/PUBLIC_KEY/SECRET_KEY 사용)
lf = Langfuse(
    host=settings.langfuse_host,
    public_key=settings.langfuse_public_key,
    secret_key=settings.langfuse_secret_key,
)


@observe()
def retrieve(query: str) -> list[str]:
    return [f"fake-doc-{i}" for i in range(3)]


@observe()
def generate(query: str, docs: list[str]) -> str:
    return f"답: {len(docs)}개 문서 근거로 '{query}'에 대해 답함"


@observe()
def rag_pipeline(query: str) -> str:
    docs = retrieve(query)
    return generate(query, docs)


if __name__ == "__main__":
    print(rag_pipeline("벡터 DB가 뭐야?"))
    lf.flush()
    print(f"→ {settings.langfuse_host} Tracing 탭 확인")
