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

## 환경 프로필

| 프로필 | LLM | Embedding | Vector DB | Observability |
|---|---|---|---|---|
| dev | gpt-4o-mini | OpenAI | Qdrant local | Langfuse local |
| cheap | Ollama qwen2.5 | local MiniLM | Qdrant local | Langfuse local |
| prod | Claude Sonnet | OpenAI text-embedding-3-large | Qdrant self-host | Langfuse self-host |
| runpod | RunPod vLLM | OpenAI | Qdrant self-host | Langfuse self-host |

`.env`의 `PROFILE=dev|cheap|prod|runpod` 로 스위치.

## Eval CI Gate

```
pytest tests/ + python eval/ci_gate.py
```
- 정답셋 30+ 통과
- faithfulness ≥ 0.75
- answer_relevancy ≥ 0.70
- context_recall ≥ 0.70
실패 시 PR block.

## 안 만드는 것 (Scope 밖)
- 인증/멀티 유저 (토이 앱이니 생략)
- Fine-tuning (extras 트랙)
- GUI로 문서 업로드 (CLI로만)
- 비용 최적화 자동화 (수동 측정만)
