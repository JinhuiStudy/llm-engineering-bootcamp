# Day 12 — Observability + Productionization (하드코어)

> **난이도**: ★★★★ (원래 ★★★에서 상향)
> **총량**: 읽기 4h + 실습 5h + 정리 1h = 10h.
> **철학**: "관측 안 되면 프로덕션 아님." 비용/지연/에러율을 **초 단위로** 볼 수 없으면 모델/프롬프트/retriever 중 뭐가 죽었는지 모른다. 오늘이 하드코어 엔지니어링 날.

## 🎯 오늘 끝나면

1. Langfuse self-hosted (docker-compose) 로컬 실행 + 본인 trace 대시보드
2. Day 10 agent 전체 flow (classifier → planner → retriever → tool_caller → reflector → finalizer)의 **노드별 trace**가 Langfuse에 뜸
3. **Prompt versioning** — 코드가 아니라 Langfuse에서 prompt 받아쓰기 (hot swap 가능)
4. **Scores attach** — Ragas eval 결과를 trace에 점수로 부착 (Day 9와 연결)
5. **Rate limit / Backoff / Timeout / Circuit breaker** 4개 패턴 구현
6. **Prompt caching** — Anthropic `cache_control` + OpenAI implicit + Gemini `cachedContents` 3사 실전 실측 (50%+ 비용 절감 검증)
7. **Streaming + TTFT 측정** — 사용자 체감 latency의 진짜 지표

## 📚 자료

### 🔥 필수 — Observability

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 1h | [Langfuse docs — Getting started](https://langfuse.com/docs) | 아키텍처(Postgres + Clickhouse) + self-host 가이드. 클라우드는 free tier도 충분. |
| 1h | [Langfuse — Tracing](https://langfuse.com/docs/tracing) | `@observe` decorator / OTel instrumentation / LangChain callback. Day 10 agent에 바로 적용. |
| 45m | [Langfuse — Prompt Management](https://langfuse.com/docs/prompt-management/overview) | prompt를 UI에서 관리. version/label/variables. A/B 기본 지원. |
| 30m | [Langfuse — Scores](https://langfuse.com/docs/scores/overview) | model-based eval + user feedback. Ragas 결과를 score로 저장. |
| 30m | [Arize Phoenix docs](https://docs.arize.com/phoenix) | OSS 관측. Local에서 `pip install arize-phoenix` 한 줄. LangSmith 비슷한 UX. |
| 30m | [OpenInference / OpenTelemetry for LLM](https://opentelemetry.io/docs/instrumentation/python/) | 표준 tracing 규약. Langfuse / Phoenix / Datadog 모두 호환. |

### 🔥 필수 — Production

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 30m | [OpenAI — Rate limits](https://platform.openai.com/docs/guides/rate-limits) | RPM/TPM 구분 + tier별 한도 + 429 response body 구조. |
| 20m | [OpenAI Cookbook — How to handle rate limits](https://cookbook.openai.com/examples/how_to_handle_rate_limits) | Tenacity `wait_random_exponential(min=1, max=60) + stop_after_attempt(6)`. |
| 30m | [OpenAI — Prompt caching](https://platform.openai.com/docs/guides/prompt-caching) | Implicit. 1024 tokens 이상 prefix가 5-10분 캐시. 자동. ~50% 할인. |
| 30m | [Anthropic — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) | Explicit `cache_control: {"type": "ephemeral"}`. system/message/tool 각각. 5분(standard) / 1시간(extended) TTL. 쓰기 +25%, 읽기 -90%. |
| 20m | [Anthropic — Streaming](https://docs.anthropic.com/en/docs/build-with-claude/streaming) | 이벤트 타입 전체. `usage`는 `message_delta`에. |
| 30m | [Gemini — Context caching](https://ai.google.dev/gemini-api/docs/caching) | `client.caches.create(model, contents, ttl)` → cache name을 contents 대신 전달. 유료. 최소 32k 토큰. |
| 30m | [OpenAI — Latency optimization](https://platform.openai.com/docs/guides/latency-optimization) | TTFT 줄이기 / model 선정 / batching / prompt compression. |

### ⭐ 강력 권장

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 20m | [tenacity docs](https://tenacity.readthedocs.io/) | `@retry` decorator + `retry_if_exception_type` + callback hooks. |
| 20m | [aiolimiter / asyncio-throttle](https://github.com/mjpieters/aiolimiter) | Client-side rate limiter. `Limiter(rate, per)` 쉬움. |
| 20m | [Circuit breaker pattern (Martin Fowler)](https://martinfowler.com/bliki/CircuitBreaker.html) | Closed/Open/Half-open 3상태. `pybreaker`로 구현. |
| 20m | [LangSmith docs](https://docs.smith.langchain.com/) | LangChain 생태계 순정. Langfuse OSS와 기능 겹침 많음. |
| 20m | [Helicone docs](https://docs.helicone.ai/) | Gateway proxy 방식 관측. Code change 거의 없이 적용. |

### 🎓 선택

- [OpenLLMetry](https://github.com/traceloop/openllmetry) — OTel 표준 LLM spans.
- [LiteLLM proxy](https://docs.litellm.ai/docs/proxy) — unified gateway + logging + caching + load balancer.

## 🔬 실습 (5h)

### 프로젝트: Observable & Resilient Retrofit

위치: `projects/day11-observability/`

```
day11-observability/
├── docker-compose.yml           # Langfuse (Postgres + Clickhouse)
├── env.example
├── instrument/
│   ├── langfuse_client.py       # singleton
│   ├── decorators.py            # @observe_node, @observe_llm
│   └── phoenix_side.py          # Phoenix 병행 관측 (선택)
├── retrofit/
│   ├── agent_traced.py          # Day 10 agent — 모든 노드 @observe
│   ├── rag_traced.py            # Day 8 pipeline — 모든 step @observe
│   └── tools_traced.py          # Day 5 tools
├── resilience/
│   ├── retry_backoff.py         # tenacity
│   ├── rate_limiter.py          # aiolimiter client-side
│   ├── circuit_breaker.py       # pybreaker
│   └── timeout.py               # asyncio.timeout wrapper
├── caching/
│   ├── anthropic_cache.py       # cache_control 실측
│   ├── openai_cache.py          # implicit 확인 (cache_hit ratio)
│   ├── gemini_cache.py          # 32k+ 프리픽스 caches.create
│   └── bench.py                 # 3사 캐시 비용 절감 표
├── streaming/
│   └── ttft_bench.py            # TTFT 측정 (first chunk 도착까지)
├── prompt_mgmt/
│   ├── upload_prompts.py        # Langfuse에 업로드
│   └── fetch_and_use.py         # 실행 시점 fetch
├── score_attach/
│   └── ragas_to_langfuse.py     # Day 9 결과 score로
├── alerts/
│   └── simple_rules.py          # latency > 10s / error rate > 5% 로그
└── README.md
```

### 🔥 필수 기능

1. **Langfuse self-host 실행** — `docker-compose up -d` → `localhost:3000` 접속 → org/project 생성 → API key 발급
2. **Day 10 agent trace** — 노드 시작/끝마다 span, LLM 호출은 generation span. Attributes: model / temperature / tokens in/out / cost / latency
3. **Day 8 RAG trace** — query_transform / retrieve / rerank / generate 각 단계 span. retrieved chunks의 source/score를 metadata로
4. **Prompt 분리** — 하드코딩된 system prompt를 Langfuse prompt로 이관 → `client.get_prompt("rag_system", label="production").compile(...)` 로 사용
5. **Score attach** — Day 9 Ragas 결과를 trace_id와 매핑해 `langfuse.score(trace_id, name="faithfulness", value=0.87)` 기록
6. **Resilience 4 patterns**:
   - tenacity: 429/529 재시도, `wait_random_exponential`, max 6회
   - aiolimiter: `Limiter(rate=50, per=60)` (분당 50)
   - pybreaker: 연속 5 실패 → open 60초
   - asyncio timeout: 호출별 30초
   - **에러 시나리오** 재현 (SDK monkey-patch로 fake 429 → retry → 성공; fake 500 → breaker trip)
7. **Prompt caching 3사 실측**:
   - Anthropic: 5000 token system prompt에 `cache_control`. 첫 호출 `cache_creation_input_tokens` 확인, 두 번째 `cache_read_input_tokens` 확인.
   - OpenAI: 같은 prefix 연속 호출 → `usage.prompt_tokens_details.cached_tokens`
   - Gemini: `caches.create` 후 여러 호출
   - 비용표: baseline vs cached — 정확한 $ 차이
8. **TTFT 측정** — streaming 시 첫 토큰까지 시간. 3사 각 5회 + mean/p50/p95
9. **Grafana / Looker 대신 Langfuse 내장 dashboard** — cost by model / latency p95 / error rate chart

### 🧪 시나리오 (Alerts)

- latency > 10s on any node → WARN
- error rate > 5% in 1min window → CRITICAL
- cache hit rate < 50% on cached prompt → INFO (잘못 설정했을 가능성)

### 🔥 Stretch

- 🧪 **Phoenix 병행** — OpenInference로 동일 app에 Langfuse + Phoenix 둘 다 보냄. UX 비교 후 선호 결정
- 🧪 **LiteLLM proxy** — 앞단에 proxy 두고 unified logging
- 🧪 **User session tracking** — `session_id` + `user_id`로 trace 그룹핑. 한 사용자의 전체 여정 보기
- 🧪 **Cost budget alert** — 일일 $20 초과하면 fail-closed
- 🧪 **Batch API** — 대량 eval을 OpenAI/Anthropic Batch로 돌려 50% 절감 실측

## ⚖️ 수치 기준

| 메트릭 | 기준 |
|---|---|
| Langfuse trace 생성 성공률 | >99% |
| Prompt caching 적용 시 비용 감소 | 40-80% (prefix 비중 따라) |
| Tenacity retry로 429 극복률 | >90% |
| Circuit breaker trip 및 복구 확인 | 1회 이상 |
| TTFT p50 / p95 기록 | 3사 모두 |

## ✅ 체크리스트

- [ ] Langfuse dashboard에 **본인 trace 최소 20개** 뜸
- [ ] Day 10 agent의 **모든 노드 span** + LLM generation span 연결 확인
- [ ] Prompt을 Langfuse에서 fetch해 실행 (hot swap test: UI에서 prompt 수정 → 재실행 시 반영)
- [ ] Ragas score (Day 9) 3건 이상 score로 부착
- [ ] Tenacity / aiolimiter / pybreaker / timeout 4개 모두 실동작 증명
- [ ] Anthropic prompt caching 적용 후 `cache_read_input_tokens > 0` 로그
- [ ] OpenAI `cached_tokens` 필드 확인
- [ ] Gemini cache 생성 + 사용 확인
- [ ] TTFT 측정 스크립트 + 3사 평균표
- [ ] `cheatsheets/` 에 `production-patterns.md` 신규 생성 (선택)
- [ ] `notes/decisions.md` — "Langfuse vs LangSmith vs Phoenix 내 선택" 한 문단

## 🧨 자주 틀리는 개념

1. **"실수로 `@observe` 전부 anthropic 호출에 걸면 token 2배"** — 한 번만. nested observation은 autolink.
2. **"Prompt caching 걸면 무조건 절감"** — prefix가 **1024 (OpenAI) / 1024 (Anthropic minimum) 토큰 이상**이어야. 짧으면 적용 안 됨.
3. **"5분 TTL이면 5분마다 쓰기 비용"** — hit 될 때마다 TTL 갱신됨 (Anthropic). 지속 사용 시 계속 캐시.
4. **"Langfuse는 네트워크 비용 부담"** — async batch send, app latency 영향 거의 0. 꺼두는 게 더 문제.
5. **"Circuit breaker 있으면 안전"** — open 동안 fallback 로직 (캐시된 답변 / 친절 에러) 없으면 UX 붕괴.
6. **"TTFT만 줄이면 UX 좋아짐"** — 절반의 진실. 짧은 답변은 total latency, 긴 답변은 tokens/sec. 둘 다 모니터.
7. **"모든 요청에 retry 걸면 안전"** — 5xx/429만. 400은 request 자체가 틀렸으니 retry 무의미. `retry_if_exception_type(RateLimitError)` 정교하게.

## 🧪 산출물

- `projects/day11-observability/` — 완성
- `docker-compose.yml` 로 Langfuse 실동
- 3사 prompt caching 절감 벤치 표 (`caching/bench.md`)
- `cheatsheets/production-patterns.md` (신규, 선택)
- `notes/decisions.md` — 관측/프롬프트 관리 의사결정 기록

## 📌 핵심 키워드

- Trace / Span / Observation / Session / User ID
- OpenTelemetry, OpenInference (LLM semantic conventions)
- Latency: TTFT (Time-To-First-Token) / TBT (Time-Between-Tokens) / E2E
- Cost: $ per 1M tokens, tracked per model
- Prompt versioning: label (`production` / `staging`), variables, compile
- Rate limit: RPM (requests per minute) / TPM (tokens per minute)
- Backoff: exponential, jitter, cap
- Circuit breaker: Closed → Open → Half-open
- Idempotency keys (중복 호출 안전)
- Prompt caching:
  - Anthropic: explicit `cache_control: {"type": "ephemeral"}`, `cache_creation_input_tokens`, `cache_read_input_tokens`, 5min / 1h TTL
  - OpenAI: implicit, `usage.prompt_tokens_details.cached_tokens`, ~50% 할인
  - Gemini: explicit `client.caches.create()`, 32k+ prefix
- Streaming: SSE, chunked, partial parse
- Batch API (OpenAI/Anthropic/Gemini) — 50% 할인, 24h SLA

## ⚠️ 프로덕션 주의

- **Langfuse self-host 데이터 보관** — Clickhouse partition 설정 필수, 안 하면 몇 달 뒤 디스크 폭발
- **Secrets in traces 금지** — API key / PII 마스킹
- **Alert fatigue** — 너무 많으면 무시하게 됨. 3-5개 핵심 룰만
- **Cost alert 설정** — 개발 중 agent loop 잘못되면 하루에 $수백 나갈 수 있음
- **Prompt Labels** — `production` / `staging` 라벨 못 붙인 prompt는 절대 배포 프로덕션에 쓰지 않기

## 🎁 내일(Day 13) 미리보기
Local LLM + RunPod. API 비용이 부담이거나 데이터 이탈 금지일 때. Ollama / vLLM / GGUF / RunPod Serverless. "언제 self-host?" 의사결정 기준.
