# Day 14 — Final Portfolio: Devlog RAG Copilot

> **연결**: [`curriculum/week2-day14-final-portfolio.md`](../../curriculum/week2-day14-final-portfolio.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md)
> **의존성**: Day 1-13 재활용 가능한 모든 코드
> **목표**: GitHub 공개 품질 + MIT + docker-compose 원클릭 + CI + Ragas threshold 통과

## 🎯 공개 기준 (OK/NG 판정)

| 기준 | OK | NG |
|---|---|---|
| Architecture diagram | 이미지/ASCII 있음 | 없음 |
| docker-compose up | 한 번에 app+qdrant+langfuse 기동 | 수동 스텝 |
| README demo | gif/screenshot 3+ | 텍스트만 |
| Eval 수치 | faithfulness ≥ 0.85 표 | 없음 |
| CI | PR마다 mini-eval 통과/실패 표시 | 없음 |
| Multi-provider | env 스위치로 4종 검증 | 1종만 |
| MCP | Claude Desktop에서 tool 호출 스크린샷 | 없음 |

## 📁 최소 디렉토리

```
final-portfolio/
├── README.md                       # 공개 README (아래 섹션 체크리스트 참고)
├── LICENSE                         # MIT
├── ARCHITECTURE.md                 # 이 디렉토리 별도
├── pyproject.toml / uv.lock
├── .env.example
├── docker-compose.yml              # app + qdrant + langfuse + postgres + clickhouse
├── Dockerfile
├── Makefile                        # make install / up / eval / test / demo
├── app/
│   ├── main.py                     # FastAPI entrypoint
│   ├── api/
│   │   ├── chat.py                 # /chat (SSE streaming)
│   │   ├── ingest.py               # /ingest
│   │   └── health.py
│   ├── agent/
│   │   ├── graph.py                # LangGraph (Day 10 이식)
│   │   └── nodes/
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── pipelines/
│   │   │   ├── baseline.py
│   │   │   └── full_stack.py       # Day 8 winner
│   │   ├── query_transform/
│   │   ├── retrievers/
│   │   ├── rerank.py
│   │   └── contextual.py
│   ├── llm/
│   │   ├── registry.py             # provider router (LLM_PROVIDER env)
│   │   └── providers/
│   │       ├── openai.py
│   │       ├── anthropic.py
│   │       ├── gemini.py
│   │       ├── ollama.py
│   │       └── runpod.py
│   ├── tools/                      # Day 5 이식
│   ├── mcp/
│   │   └── server.py               # Day 11 이식
│   ├── observability/
│   │   ├── langfuse.py
│   │   └── decorators.py
│   ├── resilience/
│   │   ├── retry.py
│   │   └── circuit.py
│   ├── caching/
│   │   └── prompt_cache.py
│   └── schemas/                    # Pydantic Answer/Citation/...
├── ui/
│   └── streamlit_app.py
├── eval/
│   ├── golden.json                 # 50+ 건
│   ├── run_ragas.py
│   └── ci_gate.py
├── scripts/
│   ├── ingest_local.sh
│   └── bench.py
├── tests/
│   ├── test_rag.py
│   └── test_agent.py
├── .github/workflows/
│   ├── ci.yml                      # lint + tests
│   └── eval.yml                    # PR: mini, main: nightly full
└── docs/
    ├── architecture.png            # 다이어그램 (excalidraw export)
    ├── demo.gif                    # asciinema or loom
    ├── decisions.md                # 3-5 ADR
    └── retrospective.md            # 14일 회고
```

## ⏱ 14일차 10h 타임박스

| 시간 | 작업 |
|---|---|
| 08:30-09:30 | Day 1-13 재활용 선별 (grep으로 함수/클래스 목록) |
| 09:30-11:30 | 스켈레톤 + FastAPI + docker-compose |
| 12:30-14:30 | LangGraph + RAG 포팅 |
| 14:30-16:00 | Langfuse + MCP + multi-provider |
| 16:00-17:00 | Golden 50+ + Ragas 통과 |
| 18:00-19:00 | README + architecture diagram + demo gif |
| 20:00-21:00 | GitHub Actions + push + 공개 |
| 21:00-21:30 | 회고 + license + repo topics |

## ✅ 필수 기능 매트릭스

### 데이터 & RAG
- [ ] Ingest CLI — 폴더/URL → chunk → contextual prepend → embed → Qdrant
- [ ] PDF/MD/HTML/TXT/Jupyter 지원
- [ ] Metadata: source/page/section/lang/ingested_at
- [ ] Hybrid retrieval (dense + BM25 + RRF)
- [ ] Cross-encoder or Cohere rerank
- [ ] Query rewrite + multi-query
- [ ] Contextual Retrieval (Anthropic)
- [ ] Pydantic Answer with citations + confidence

### Agent & Tools
- [ ] LangGraph StateGraph (classifier→retriever/tools→reflector→finalizer)
- [ ] Reflection loop max 2
- [ ] SqliteSaver checkpoint
- [ ] HITL interrupt on write/external tools
- [ ] Day 5 tools: web_search / calculator / today / file_read (sandbox)

### MCP
- [ ] FastMCP server `app/mcp/server.py`
- [ ] Claude Desktop config 포함
- [ ] README에 등록 방법 + 스크린샷

### LLM Multi-provider
- [ ] `LLM_PROVIDER=openai|anthropic|ollama|runpod` env 스위치
- [ ] `EMBED_PROVIDER=openai|voyage|local-e5`
- [ ] 4 provider 모두 smoke test 통과

### Observability
- [ ] Langfuse trace (노드/LLM/tool/retriever 모두 span)
- [ ] Prompt Langfuse에서 fetch (hot swap 가능)
- [ ] Cost/latency/error dashboard
- [ ] Ragas score → trace attach

### Eval (CI gate)
- [ ] Golden 50+ 건 (Day 9 30 + 20 추가)
- [ ] `faithfulness ≥ 0.85` gate
- [ ] PR mini-eval 20건, nightly full

### Production hardening
- [ ] FastAPI SSE streaming
- [ ] Anthropic prompt caching
- [ ] tenacity retry on 429/529
- [ ] aiolimiter + pybreaker + timeout
- [ ] Structured logging + request ID
- [ ] PII 마스킹

### Docs
- [ ] README (공개 섹션 전부 — 아래)
- [ ] ARCHITECTURE.md
- [ ] decisions.md (ADR 3-5)
- [ ] retrospective.md

## 🖼 공개 README 섹션 체크리스트

```markdown
# Devlog RAG Copilot
> one-liner

![demo](docs/demo.gif)

## Why
(1 문단)

## Architecture
![arch](docs/architecture.png)

## Stack
[badges...]
- Python 3.11, FastAPI, LangGraph, Qdrant, Langfuse, Ragas, MCP

## Quickstart
```bash
cp .env.example .env  # API keys
docker compose up -d
./scripts/ingest_local.sh ./data/pdfs
uv run uvicorn app.main:app --reload
# or: uv run streamlit run ui/streamlit_app.py
```

## Eval
| Metric | Score |
|---|---|
| Faithfulness | 0.87 |
| Answer Relevancy | 0.89 |
| Context Precision | 0.82 |
| Context Recall | 0.84 |

## MCP (Claude Desktop)
```json
{
  "mcpServers": {
    "devlog": {"command":"uv","args":["run","python","-m","app.mcp.server"]}
  }
}
```
![mcp](docs/mcp-screenshot.png)

## Multi-provider
`LLM_PROVIDER=openai|anthropic|ollama|runpod`

## Limitations
- (정직하게 3가지)

## Roadmap
- [ ] Vision RAG
- [ ] Multi-user
- [ ] Fine-tuned domain model

## License
MIT
```

## 📊 최종 수치 목표

| 메트릭 | 목표 |
|---|---|
| Ragas Faithfulness | ≥ 0.85 |
| Ragas AnsRel | ≥ 0.85 |
| Ragas CtxP/CtxR | ≥ 0.80 |
| Unanswerable 거절률 | ≥ 0.85 |
| p50 E2E | ≤ 5s |
| p95 E2E | ≤ 12s |
| Prompt cache hit ratio | ≥ 70% |
| CI mini-eval 시간 | ≤ 5분 |

## 🧨 마지막 함정

1. **기능 욕심** — Stretch는 푸쉬 뒤 며칠 더. 지금은 필수만
2. **데모 영상 없이 push** — 30초 asciinema/loom 필수. 면접관 3배 인상
3. **Eval 숫자 없이 공개** — 그럴싸한 데모로만 보임
4. **LICENSE 없음** — fork/star 불가능
5. **.env 커밋** — 배포 전 `git log -p -- .env` 확인 + 키 rotate
6. **Docker 이미지에 key 포함** — multi-stage build, build args 사용
7. **README가 코드 blob** — 3-5분에 읽히는 구조로 정리
8. **ARCHITECTURE.md == 코드 복붙** — 다이어그램 + why + trade-off

## 🎁 Stretch (V2 후속)

- Docker multi-arch (amd64 + arm64)
- Fly.io / Modal deploy
- Semantic cache (Redis + embedding)
- Vision RAG
- Voice (Whisper)
- Guardrails (LlamaFirewall / Prompt-Guard)

## 🔗 후속

[`curriculum/extras.md`](../../curriculum/extras.md):
- OWASP LLM Top 10
- Batch API (50%)
- Fine-tuning (LoRA/QLoRA/DPO)
- Multi-agent / CrewAI
- pgvector / Weaviate / Pinecone 교체
