# Day 14 — 최종 포트폴리오: Devlog RAG Copilot (Production-Grade)

> **난이도**: ★★★★★ (그대로 유지, 대신 기준이 올라감)
> **총량**: 풀 10h + 밤새지 말기.
> **철학**: "배웠다"가 아니라 "GitHub에 공개해도 부끄럽지 않다"가 기준. README / 아키텍처 / eval 수치 / 데모 gif까지 포함.

## 🎯 Day 14 끝에 가지고 있어야 할 것

1. **공개 가능한 GitHub repo** — MIT, README에 아키텍처 다이어그램 + 데모 gif + Ragas 수치 + 실행법
2. **Docker Compose 원클릭 실행** — `docker compose up -d && ./run-ingest && python app.py`
3. **GitHub Actions CI** — lint + mini-eval threshold gate (Day 9 결과 활용)
4. **Multi-provider RAG + Agent + MCP + Langfuse 통합** — env로 provider switch
5. **정답셋 50+ 기반 Ragas eval 통과** — faithfulness ≥ 0.85
6. **회고 문서** — 14일 중 가장 어려웠던/의외였던 것. 다음 학습 플랜

## 🧩 프로젝트: Devlog RAG Copilot

### 한 줄 설명
내 기술 블로그 / 노트 / PDF / 슬랙 로그를 RAG + LangGraph Agent + MCP로 질의하고, Langfuse로 관측하며, Ollama/RunPod 자유 전환되는 개인 AI 코파일럿.

### 아키텍처

```
┌────────────┐      ┌─────────────┐      ┌──────────────────────┐
│ Streamlit  │─SSE─▶│   FastAPI   │─────▶│  LangGraph Agent     │
│ or CLI     │      │  /chat      │      │  classifier→...      │
└────────────┘      └──────┬──────┘      └─┬─────────┬──────────┘
                           │                │         │
                      /ingest                │         │
                           │      ┌──────────▼───┐  ┌─▼────┐  ┌─────┐
                           │      │  RAG        │  │Tools │  │ MCP │
                           │      │  Hybrid+RR  │  │Web/FS│  │Serv │
                           │      │  Qdrant     │  └──────┘  └─────┘
                           │      └──────┬──────┘
                           │             │
                           ▼             ▼
                    ┌──────────────────────┐
                    │ Langfuse trace+score  │◀── Ragas CI gate
                    └──────────────────────┘

LLM: OpenAI / Anthropic / Ollama / RunPod vLLM   (env switch)
Embed: OpenAI / Voyage / multilingual-e5 (local)
```

### 디렉토리 (준칙)

```
final-portfolio/
├── README.md                    # TOC, architecture, run, demo, eval, license
├── LICENSE (MIT)
├── pyproject.toml / uv.lock
├── .env.example
├── docker-compose.yml           # app + qdrant + langfuse (+ postgres + clickhouse)
├── Dockerfile
├── Makefile
├── app/
│   ├── main.py                  # FastAPI entrypoint
│   ├── api/
│   │   ├── chat.py              # /chat (SSE streaming)
│   │   ├── ingest.py            # /ingest
│   │   └── health.py
│   ├── agent/
│   │   ├── graph.py             # LangGraph StateGraph
│   │   ├── nodes/
│   │   └── state.py
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── pipelines/           # v1/v2/full (Day 8 structure)
│   │   ├── query_transform/
│   │   ├── retrievers/
│   │   ├── rerank.py
│   │   └── contextual.py
│   ├── llm/
│   │   ├── registry.py          # provider router
│   │   └── providers/{openai,anthropic,gemini,ollama,runpod}.py
│   ├── tools/
│   ├── mcp/
│   │   └── server.py            # 자체 MCP server
│   ├── observability/
│   │   └── langfuse.py
│   ├── resilience/
│   │   ├── retry.py
│   │   └── circuit.py
│   ├── caching/
│   │   └── prompt_cache.py
│   └── schemas/                 # Pydantic
├── ui/
│   └── streamlit_app.py
├── eval/
│   ├── golden.json              # 50+ 건
│   ├── run_ragas.py
│   └── ci_gate.py               # threshold 체크
├── scripts/
│   ├── ingest_local.sh
│   └── bench.py
├── tests/
│   ├── test_rag.py
│   └── test_agent.py
├── .github/
│   └── workflows/
│       ├── ci.yml               # lint + unit tests
│       └── eval.yml             # PR마다 mini-eval, main에 nightly full
└── docs/
    ├── architecture.md
    ├── decisions.md             # ADR 3-5개
    └── retrospective.md         # 14일 회고
```

## 📋 기능 체크리스트 (반드시 포함)

### 데이터
- [ ] Ingest CLI — 폴더/URL 단위 → chunk → contextual retrieval prepend → embed → Qdrant
- [ ] PDF / MD / HTML / TXT / Jupyter notebook 지원
- [ ] Metadata: `source`, `page`, `section`, `lang`, `ingested_at`

### RAG
- [ ] Hybrid retrieval (dense + BM25 + RRF)
- [ ] Cross-encoder or Cohere rerank
- [ ] Query transform: rewrite + multi-query (선택적 HyDE)
- [ ] Contextual retrieval (Anthropic 방식)
- [ ] 출처 인용 (Pydantic `Answer(text, citations: list[Citation])`)

### Agent
- [ ] LangGraph StateGraph
- [ ] classifier → (direct|rag|tool|complex) 라우팅
- [ ] Reflection loop (max 2)
- [ ] Checkpointing (Sqlite/Postgres)
- [ ] HITL interrupt on sensitive tools

### Structured Output
- [ ] Pydantic 응답 스키마 `Answer(text, citations, confidence: float)`
- [ ] strict=true (OpenAI) / native (Anthropic) / response_schema (Gemini) 모두 호환

### Tools
- [ ] Web search (Tavily/Brave)
- [ ] Calculator (safe expr)
- [ ] Today's date / time zone
- [ ] File read (sandbox)
- [ ] (Stretch) Python exec (docker-isolated)

### MCP
- [ ] 위 기능들을 MCP tool/resource로 노출
- [ ] Claude Desktop/Code에서 사용 가능 (config 포함)

### Observability
- [ ] Langfuse trace (노드 / LLM / retriever / tool 모두 span)
- [ ] Prompt versioning (Langfuse prompt)
- [ ] Cost/latency/error rate dashboard
- [ ] Ragas score attach to trace

### Eval (CI gate)
- [ ] Golden 50+ 건 (Day 9 30 + Day 14 20 추가)
- [ ] `faithfulness ≥ 0.85` gate
- [ ] PR마다 sample 20건, nightly full

### Multi-provider
- [ ] env `LLM_PROVIDER=openai|anthropic|ollama|runpod`
- [ ] env `EMBED_PROVIDER=openai|voyage|local-e5`
- [ ] 동일 코드로 provider 전환 (runtime)

### Production hardening
- [ ] FastAPI SSE streaming
- [ ] Anthropic prompt caching on long system prompt
- [ ] tenacity retry on 429/529
- [ ] aiolimiter + pybreaker
- [ ] request ID + structured logging

### Docs
- [ ] README.md (TOC / overview / architecture ASCII / screenshots / run / eval table)
- [ ] ARCHITECTURE.md (detailed)
- [ ] decisions.md (3-5 ADR — 왜 LangGraph, 왜 Qdrant, 왜 Langfuse 등)
- [ ] retrospective.md (14일 회고)

### Stretch (욕심)
- [ ] Docker multi-arch (amd64 + arm64)
- [ ] Fly.io / Modal deploy 가이드
- [ ] Semantic cache (Redis + embedding)
- [ ] Vision (이미지 포함 문서)
- [ ] Voice (Whisper input)
- [ ] Guardrails (LlamaFirewall / Prompt-Guard)

## ⏱ 14일차 10시간 타임박스

| 블록 | 시간 | 작업 |
|---|---|---|
| 1h | 08:30-09:30 | Day 1-13 프로젝트에서 재사용 파일 grep + 리스트 | 
| 2h | 09:30-11:30 | `final-portfolio/` 스켈레톤 + FastAPI skeleton + docker-compose |
| 2h | 12:30-14:30 | LangGraph agent + RAG pipeline 포팅 |
| 1.5h | 14:30-16:00 | Langfuse + MCP + multi-provider 조립 |
| 1h | 16:00-17:00 | Golden 50+ 건 보강 + Ragas eval 통과 |
| 1h | 18:00-19:00 | README + architecture diagram (ASCII or excalidraw) + 데모 gif (asciinema 추천) |
| 1h | 20:00-21:00 | GitHub Actions CI + push + 레포 공개 |
| 0.5h | 21:00-21:30 | 회고 + license + stars 부탁 |

**중단없이 가려면 13일 동안 재사용 가능한 코드를 의식해서 썼어야 함.** 여기까지 왔으면 이미 70% 된 것.

## 📊 최종 Eval 목표

| 메트릭 | 목표 |
|---|---|
| Ragas Faithfulness | ≥ 0.85 |
| Ragas Answer Relevancy | ≥ 0.85 |
| Ragas Context Precision | ≥ 0.80 |
| Ragas Context Recall | ≥ 0.80 |
| Unanswerable 거절률 | ≥ 0.85 |
| p50 end-to-end | ≤ 5s |
| p95 end-to-end | ≤ 12s |
| Prompt cache hit ratio (시스템 prompt) | ≥ 70% |
| CI mini-eval 실행시간 | ≤ 5min |

## 🖼 README 필수 섹션

```markdown
# Devlog RAG Copilot

> Personal AI copilot for my tech notes, blogs, PDFs.
> Multi-provider RAG + LangGraph Agent + MCP + Langfuse.

![demo](docs/demo.gif)

## Why
(1문단)

## Architecture
![arch](docs/architecture.png)

## Stack
- [Badges ...]
- Python 3.11, FastAPI, LangGraph, Qdrant, Langfuse, Ragas

## Run
```bash
cp .env.example .env
docker compose up -d
uv run python scripts/ingest_local.sh ./data/pdfs
uv run streamlit run ui/streamlit_app.py
```

## Eval
| Metric | Score |
|---|---|
| Faithfulness | 0.87 |
| Answer Relevancy | 0.89 |
| ...

## Limitations
(정직하게 3가지)

## Roadmap
- [ ] Fine-tuning on domain
- [ ] Vision support
- [ ] Multi-user deployment

## License
MIT
```

## ✅ 최종 체크리스트

- [ ] GitHub repo 공개 + MIT license
- [ ] `docker compose up -d` 로 qdrant + langfuse + app 전부 뜸
- [ ] README에 demo gif 또는 3+ 스크린샷
- [ ] ARCHITECTURE.md 다이어그램
- [ ] decisions.md ADR 3개+
- [ ] retrospective.md 14일 회고 (아래 가이드)
- [ ] Ragas threshold 통과
- [ ] CI action 실동 (PR test)
- [ ] MCP config 포함 (Claude Desktop에서 불러서 스크린샷)
- [ ] Multi-provider env 4종 모두 동작 (`openai / anthropic / ollama / runpod`)
- [ ] Streamlit UI 접속 가능
- [ ] repo topic 태그 (`llm`, `rag`, `langgraph`, `mcp`, `langfuse`)

## 🗒 회고 가이드 (retrospective.md)

1. **14일 중 가장 어려웠던 날** — 그 이유와 어떻게 돌파했는지 or 어떻게 우회했는지
2. **가장 과대평가된 자료** / **가장 과소평가된 자료** — 각 1개
3. **실무에서 당장 쓸 수 있다고 느낀 기술 3개**
4. **예상과 달리 간단했던 것 / 복잡했던 것**
5. **프로덕션에 쓰기 전 반드시 보강해야 할 3가지** — 정직하게
6. **다음 2주 학습 계획** (`curriculum/extras.md` 참고) — security / batch / fine-tuning / vision 중 선택

## 🧨 자주 틀리는 마무리

1. **"기능 욕심"** — 체크리스트 Stretch는 욕심. 필수만 먼저, Stretch는 repo 올리고 나서 며칠 더.
2. **"데모 영상 없이 push"** — 면접관은 영상부터 봄. 30초 asciinema/loom 있으면 인상 3배.
3. **"Eval 수치 없이 공개"** — 숫자 없으면 "그럴싸한 데모"로만 보임. threshold 통과 스크린샷 / 표를 반드시.
4. **"LICENSE 없이 push"** — MIT 1줄 부족으로 아무도 fork 못함.
5. **"돈 터뜨린 채 demo 공개"** — API key rotate + .env 커밋 안 한 거 재확인.

## 🧪 최종 산출물

- `github.com/<yourname>/devlog-rag-copilot` — 공개 repo
- `docs/retrospective.md` — 회고
- `notes/daily-log.md` — Day 14 섹션: "오늘 끝냈다. 내일부터 확장 트랙"
- `notes/decisions.md` — 핵심 ADR 3-5개

## 🎁 Day 15+
[`curriculum/extras.md`](extras.md):
- Security / OWASP LLM Top 10 / Prompt Guard
- Guardrails AI / NeMo Guardrails
- Deploy (Fly.io / Modal / Docker Swarm)
- Batch API (50% cost)
- Fine-tuning (LoRA / QLoRA / DPO)
- Vision RAG / Voice
- Semantic cache
- Multi-agent (CrewAI / supervisor)

**이 14일이 끝이 아니라 시작.**
