"""AI Study Bootcamp — shared utilities.

import 예:
    from ai_study.llm import chat, chat_stream
    from ai_study.tokens import count_tokens, estimate_cost, pricing_table
    from ai_study.embeddings import embed, embedding_dim
    from ai_study.vectors import ensure_collection, upsert_texts, search
    from ai_study.prompts import render, render_string
    from ai_study.langfuse_client import observe, get_langfuse, flush
    from ai_study.retry import with_retry
    from ai_study.logging import logger
    from ai_study.config import settings
"""

from ai_study.config import settings

__all__ = ["settings"]
__version__ = "0.2.0"
