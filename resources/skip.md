# ⚪ 버려도 되는 자료 (중복 / 우선순위 매우 낮음)

**주의: "버린다"는 건 "안 본다"가 아니라 "같은 내용의 더 나은 대안을 이미 봄"이다.** 이 목록은 의사결정 기록.

## 중복 URL (같은 내용의 다른 경로)

| 버릴 것 | 이유 | 대안 |
|---|---|---|
| [openai/openai-cookbook GitHub](https://github.com/openai/openai-cookbook) | GitHub raw 레포 | [developers.openai.com/cookbook](https://developers.openai.com/cookbook) 이 렌더된 버전 |
| [cookbook.openai.com](https://cookbook.openai.com/) | 예전 도메인 | 위와 동일 |
| [platform.claude.com Structured Outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) | docs.anthropic.com의 리다이렉트 대상 | 원래 URL 그대로 사용 (자동 리다이렉트됨) |
| [anthropics/courses/tree/master/prompt_engineering_interactive_tutorial](https://github.com/anthropics/courses/tree/master/prompt_engineering_interactive_tutorial) | 오래된 하위 경로 | [prompt-eng-interactive-tutorial (독립 레포)](https://github.com/anthropics/prompt-eng-interactive-tutorial)가 최신 |
| [chat.lmsys.org](https://chat.lmsys.org/) | LMArena로 리브랜드 | [lmarena.ai](https://lmarena.ai/) |

## 원문 섹션 21 (Claude 분류 프롬프트)
사용자가 원문에 적은 "Claude한테 분류시키는 프롬프트" 섹션은 자료가 아니라 메서드. 우리는 이미 이 파일(`links-classified.md`)에서 그 분류를 수행했으므로 별도로 볼 필요 없음.

## 원문 섹션 22 (Top 20)
우선순위 자료 20개. `00-top20-priority.md`로 분리 완료. 중복 아님이지만, "링크 목록"으로는 별도 불필요.

## 한국어 검색 키워드
자료가 아닌 검색 가이드. `extras.md`에 포함시킴 — 단독 자료로는 스킵.

## 2주 안에 안 볼 것 (= 🟢 나중에로 분류)
아래는 "버리는 건 아니지만 2주 안에는 안 볼 것"이라는 의미:
- CrewAI 관련 (2주 안 multi-agent는 LangGraph/Pydantic AI로 충분)
- Fine-tuning 전체 섹션 (프롬프트/RAG 한계 경험 후)
- 논문 정독 (요약만)
- Chroma/FAISS/Pinecone/pgvector (Qdrant로 대체)
- HF Transformers 저수준 사용 (vLLM/Ollama로 추상화)

이들은 `later.md`에서 추적.

## 요약
2주 하드코어 부트캠프에서 **안 보는 것**:
1. 완전 중복 URL (위 표)
2. 과거 도메인/리다이렉트 URL (자동 해결됨)
3. 메서드/가이드 문단 (자료 아님)

그 외 모든 링크는 🔴/🟡/🟢 중 하나로 배정되어 있다.
