"""환경변수 로딩. 루트 .env를 자동 발견."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


def _find_root() -> Path:
    cur = Path(__file__).resolve()
    for parent in [cur, *cur.parents]:
        if (parent / ".env").exists() or (parent / ".env.example").exists():
            return parent
    return cur.parents[2]  # shared/ai_study/config.py → shared/ → root


ROOT = _find_root()
load_dotenv(ROOT / ".env", override=False)


@dataclass(frozen=True)
class Settings:
    # keys
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")

    # default models
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # embedding
    openai_embedding_model: str = os.getenv(
        "OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"
    )
    gemini_embedding_model: str = os.getenv(
        "GEMINI_EMBEDDING_MODEL", "text-embedding-004"
    )
    local_embedding_model: str = os.getenv(
        "LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )

    # infra
    qdrant_url: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")

    # observability
    langfuse_host: str = os.getenv("LANGFUSE_HOST", "http://localhost:3000")
    langfuse_public_key: str = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    langfuse_secret_key: str = os.getenv("LANGFUSE_SECRET_KEY", "")

    # cloud
    runpod_api_key: str = os.getenv("RUNPOD_API_KEY", "")
    runpod_endpoint_id: str = os.getenv("RUNPOD_ENDPOINT_ID", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")

    # behavior
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    default_temperature: float = float(os.getenv("DEFAULT_TEMPERATURE", "0.2"))
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "60"))

    root: Path = ROOT

    def has_openai(self) -> bool:
        return bool(self.openai_api_key) and not self.openai_api_key.startswith("sk-...")

    def has_anthropic(self) -> bool:
        return bool(self.anthropic_api_key) and not self.anthropic_api_key.startswith(
            "sk-ant-..."
        )

    def has_gemini(self) -> bool:
        return bool(self.google_api_key)


settings = Settings()
