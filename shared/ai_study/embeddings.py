"""Embedding 공급자 통합. OpenAI / Gemini / 로컬 SBERT."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from ai_study.config import settings

EmbeddingProvider = Literal["openai", "gemini", "local"]


def embed(
    texts: list[str],
    *,
    provider: EmbeddingProvider = "openai",
    model: str | None = None,
) -> list[list[float]]:
    if not texts:
        return []

    if provider == "openai":
        from openai import OpenAI

        client = OpenAI()
        r = client.embeddings.create(
            model=model or settings.openai_embedding_model,
            input=texts,
        )
        return [d.embedding for d in r.data]

    if provider == "gemini":
        from google import genai

        client = genai.Client(api_key=settings.google_api_key)
        out: list[list[float]] = []
        # Gemini는 batch 제한 있음 — 작게 쪼개 호출
        batch = 100
        for i in range(0, len(texts), batch):
            r = client.models.embed_content(
                model=model or settings.gemini_embedding_model,
                contents=texts[i : i + batch],
            )
            out.extend(e.values for e in r.embeddings)
        return out

    if provider == "local":
        model_ = _local_model(model or settings.local_embedding_model)
        return [v.tolist() for v in model_.encode(texts, show_progress_bar=False)]

    raise ValueError(provider)


@lru_cache(maxsize=4)
def _local_model(name: str):
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(name)


def embedding_dim(provider: EmbeddingProvider = "openai", model: str | None = None) -> int:
    """각 provider의 벡터 차원."""
    if provider == "openai":
        m = model or settings.openai_embedding_model
        return {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }.get(m, 1536)
    if provider == "gemini":
        return 768  # text-embedding-004
    if provider == "local":
        return len(_local_model(model or settings.local_embedding_model).encode(["x"])[0])
    raise ValueError(provider)
