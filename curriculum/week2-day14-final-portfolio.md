# Day 14 — 최종 포트폴리오 프로젝트

## 목표
- 13일간 배운 것을 **하나의 production-grade 앱**으로 통합
- GitHub에 공개 가능한 품질로 정리
- 포트폴리오로 면접/실무 전환 시 쓸 수 있는 수준

## 프로젝트: "Devlog RAG Copilot"
(마음에 안 들면 도메인만 바꾸고 같은 구조로 재활용)

### 한 줄 설명
내 기술 블로그 / 문서 / 슬랙 로그 / PDF를 모아 RAG + Agent + MCP로 질의하고, Langfuse로 관측하며, Ollama나 RunPod로도 돌릴 수 있는 개인 AI 도우미.

### 아키텍처
```
┌──────────────┐   ┌───────────┐   ┌───────────────┐
│ Streamlit/CLI│──▶│  FastAPI  │──▶│ LangGraph Agent│
└──────────────┘   └─────┬─────┘   └────────┬──────┘
                         │                  │
                    streaming SSE           │
                                   ┌────────┼────────┐
                                   ▼        ▼        ▼
                              ┌────────┐ ┌──────┐ ┌──────┐
                              │ RAG    │ │Tools │ │MCP   │
                              │ Qdrant │ │Web/FS│ │Server│
                              └────┬───┘ └──────┘ └──────┘
                                   ▼
                              ┌──────────┐
                              │ Reranker │
                              │ +Hybrid  │
                              └──────────┘
                              
         ┌─────────────────────────┐
         │ Langfuse tracing + eval │ ← all 단계
         └─────────────────────────┘
         
 LLM Provider: OpenAI / Anthropic / Ollama / RunPod vLLM (env로 스위치)
```

### 필수 기능 (반드시 포함)
1. **Ingest 파이프라인**: 폴더/URL → chunk → embed → Qdrant
2. **Hybrid retrieval**: dense + BM25 + RRF + cross-encoder rerank
3. **Query transformation**: query rewriting + multi-query
4. **LangGraph agent**: planner → (RAG | tools | both) → reflector → finalizer
5. **Structured output**: Pydantic으로 answer + citations + confidence
6. **Tool use**: 최소 3개 (web_search, calculator, today's date / 로컬 파일 접근)
7. **MCP server**: 위 기능을 MCP tool로도 노출 (Claude Desktop에서 사용 가능)
8. **Observability**: Langfuse trace, cost, latency, prompt versioning
9. **Evaluation**: Ragas 기반 CI 체크 (정답셋 30+)
10. **Multi-provider**: OpenAI / Anthropic / Ollama / RunPod — env로 선택
11. **Streaming 응답** (FastAPI SSE)
12. **Prompt caching** (Anthropic cache_control) — 시스템 프롬프트 재사용
13. **Rate limit 대응** (tenacity backoff)

### Stretch (여력 되면)
- Docker Compose로 원클릭 실행 (app + qdrant + langfuse)
- GitHub Actions CI (lint + eval threshold)
- Semantic cache (동일 의미 쿼리 캐싱)
- Vision (이미지 포함 문서 처리)
- Voice 입력 (Whisper)

### 위치
`projects/final-portfolio/`

### 디렉토리 구조 (참고)
```
final-portfolio/
├── README.md                 # 어떤 프로젝트인지, 아키텍처, 실행법, 데모 gif
├── pyproject.toml            # uv/poetry
├── .env.example
├── docker-compose.yml        # qdrant + langfuse + app
├── app/
│   ├── main.py               # FastAPI entrypoint
│   ├── api/
│   │   ├── chat.py           # /chat (SSE)
│   │   ├── ingest.py         # /ingest
│   │   └── health.py
│   ├── agent/
│   │   ├── graph.py          # LangGraph
│   │   └── nodes/
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── retrievers/
│   │   ├── query_transform/
│   │   └── rerank.py
│   ├── llm/
│   │   ├── registry.py       # provider router
│   │   └── providers/
│   ├── tools/
│   ├── mcp/
│   │   └── server.py
│   ├── observability/
│   │   └── langfuse.py
│   └── schemas/              # Pydantic
├── eval/
│   ├── golden.json
│   ├── run_ragas.py
│   └── ci_gate.py
├── ui/
│   └── streamlit_app.py      # 간단 데모 UI
└── tests/
```

## 14일차 시간 배분 (10h)

| 시간 | 작업 |
|---|---|
| 1h | Day 1-13 프로젝트들 중 재사용할 코드 골라내기 (grep, copy) |
| 3h | app 스켈레톤 + LangGraph agent 조립 |
| 2h | RAG 파이프라인 포팅 + Langfuse 연결 |
| 1h | MCP 서버 붙이기 |
| 1h | 정답셋 30개 만들고 Ragas eval 통과시키기 |
| 1h | README + 데모 스크린샷/gif |
| 1h | git init + 첫 commit + GitHub push + 회고 작성 |

## 회고 (`notes/retrospective.md`에 작성)
- 14일 중 가장 어려웠던 날
- 가장 과대평가된 자료 / 가장 과소평가된 자료
- 실무에서 당장 쓸 수 있다고 느껴지는 기술 3개
- 후속 학습 계획 (fine-tuning / 멀티모달 / 보안 → `curriculum/extras.md` 참고)

## 포트폴리오 READEME 체크리스트
- [ ] 한 줄 소개
- [ ] 왜 만들었는가
- [ ] 아키텍처 다이어그램
- [ ] 사용한 기술 스택 (배지)
- [ ] 실행법 (docker-compose up)
- [ ] 데모 gif 또는 스크린샷 3장+
- [ ] Eval 결과 (Ragas 점수)
- [ ] 한계 및 개선점 (정직하게)
- [ ] 라이선스 (MIT 권장)
