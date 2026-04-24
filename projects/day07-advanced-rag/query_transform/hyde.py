"""HyDE: Hypothetical Document Embeddings.

짧은 가설 답변을 생성 → 그걸로 검색. 질문과 문서의 어휘 불일치를 완화.
"""

from __future__ import annotations

from ai_study.llm import chat


HYDE_PROMPT = """아래 질문에 답한다고 가정하고, 검색 대상 문서에 있을 법한 짧은 답변(2-4문장)을 작성하라.
정확성보다 '문서 어휘와 비슷함'이 중요하다.

질문: {q}
가상 답변:"""


def hyde(query: str) -> str:
    return chat("openai", HYDE_PROMPT.format(q=query), temperature=0.2, max_tokens=200)
