# Devlog RAG Copilot — Architecture

## 구성도 (텍스트)

```
┌─────────────────────────────────────────────────────────┐
│   Client  (CLI / Streamlit / Claude Desktop via MCP)    │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP (SSE streaming)
                        ▼
              ┌─────────────────────┐
              │   FastAPI (main.py) │
              │  /chat  /ingest     │
              │  /health            │
              └──────────┬──────────┘
                         │
                         ▼
             ┌──────────────────────────┐
             │    LangGraph Agent       │
             │ planner→route→draft→refl │
             └───┬──────────┬───────────┘
                 │          │
       RAG       │          │     Tools
                 ▼          ▼
   ┌─────────────────┐    ┌──────────────┐
   │ Query Transform │    │  web_search  │
   │  (rewrite/hyde/ │    │  calculator  │
   │   multi_query)  │    │  date, file  │
   └────────┬────────┘    └──────────────┘
            │
            ▼
   ┌────────────────────┐
   │ Hybrid Retriever   │
   │ dense + BM25 + RRF │
   └────────┬───────────┘
            │
            ▼
   ┌────────────────────┐
   │  Cross-encoder     │
   │  Reranker          │
   └────────┬───────────┘
            │
            ▼
   ┌────────────────────┐
   │  Qdrant Collection │
   └────────────────────┘

 관측: Langfuse trace 모든 step
 LLM: OpenAI / Anthropic / Ollama / RunPod env로 스위치
 Eval: Ragas CI gate (faithfulness > 0.8 등)
```

## 데이터 흐름
1. 사용자 질문 → FastAPI `/chat`
2. LangGraph `planner`가 RAG 필요 여부 분류
3. RAG 필요 시 → query_transform → hybrid → rerank → top-5
4. Tool 필요 시 → 병렬 tool call
5. `drafter`가 context+tool_results로 초안
6. `reflector`가 비평 → 부족 시 retriever로 재시도 (최대 2회)
7. `finalizer`가 Pydantic `FinalAnswer` 반환
8. SSE로 클라이언트에 스트리밍

## 핵심 인터페이스

```python
# app/schemas/final_answer.py
class Citation(BaseModel):
    source: str
    page: int | None
    snippet: str

class FinalAnswer(BaseModel):
    answer: str
    citations: list[Citation]
    confidence: float = Field(ge=0, le=1)
    model: str
    tokens_used: int
```

## 환경 프로필 (2026-04 / v3)

| 프로필 | LLM | Embedding | Vector DB | Observability |
|---|---|---|---|---|
| dev | gpt-4o-mini | OpenAI text-embedding-3-small | Qdrant local | Langfuse local |
| cheap | Ollama qwen3:8b | local multilingual-e5-large | Qdrant local | Langfuse local |
| prod | claude-sonnet-4-6 | OpenAI text-embedding-3-large | Qdrant self-host | Langfuse self-host |
| runpod | RunPod vLLM Qwen3-8B | OpenAI | Qdrant self-host | Langfuse self-host |
| finetuned | Day 13 LoRA adapter (RunPod) | OpenAI | Qdrant self-host | Langfuse self-host |

`.env`의 `PROFILE=dev|cheap|prod|runpod|finetuned` 로 스위치.

## Eval CI Gate (v3 상향)

```
pytest tests/ + python eval/ci_gate.py
```
- 정답셋 **50+** 통과 (Day 9 확장)
- **faithfulness ≥ 0.85** (v2 0.75 → v3 상향)
- **answer_relevancy ≥ 0.85**
- **context_precision ≥ 0.80**
- **context_recall ≥ 0.80**
- **unanswerable 거절률 ≥ 0.85**

PR: sample 20건 mini-eval, main nightly full. threshold 미달 시 PR block.

## v3 통합 기능 (Day 14 Mega Portfolio)

- 🖼 **Vision RAG** (Day 7) — 표/차트 PDF를 Vision API fallback
- 🎤 **Voice input** (Day 10) — Whisper → agent
- 🤖 **Multi-agent** (Day 9) — Supervisor + Researcher + Writer + Critic
- 🎯 **Fine-tuned LoRA** (Day 13) — Qwen3-8B 본인 도메인
- 🛡 **Guardrails 3겹** (Day 3 + Day 11) — Prompt-Guard + Guardrails AI + NeMo
- 🌐 **Deployed on Modal** (Day 12) — public URL
- 📜 **Contextual Retrieval** (Day 8) — Anthropic 2024-09 기법 (49% 개선)

## 안 만드는 것 (Scope 밖, v3)

- 인증/멀티 유저 (토이 앱이니 생략)
- GUI로 문서 업로드 (CLI로만)
- 비용 최적화 자동화 (수동 측정만)
- 대규모 분산 훈련 (Day 14 개념만 — Tensor/Pipeline/Data parallel)
