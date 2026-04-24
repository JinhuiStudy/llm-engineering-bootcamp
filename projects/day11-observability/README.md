# Day 12 — Observability + Production Retrofit

> **연결**: [`curriculum/week2-day12-observability.md`](../../curriculum/week2-day12-observability.md) · [`cheatsheets/production-patterns.md`](../../cheatsheets/production-patterns.md)
> **의존성**: Day 10 agent + Day 8 RAG + Day 9 Ragas
> **다음**: Day 14 portfolio에 trace/cost/latency dashboard 통합

## 🎯 이 프로젝트로

1. Langfuse self-host docker-compose 가동 → 본인 trace 대시보드
2. Day 10 agent 전체 노드에 `@observe` span
3. **Prompt versioning** — Langfuse에서 fetch → hot swap
4. **Scores attach** — Day 9 Ragas 결과를 trace에 부착
5. **Resilience 4-layer**: tenacity / aiolimiter / pybreaker / asyncio timeout
6. **3사 prompt caching 실측** — Anthropic / OpenAI / Gemini 각자 비용 절감 표
7. **TTFT 측정** — 3사 streaming 첫 토큰 지연

## 📁 디렉토리

```
day11-observability/
├── pyproject.toml
├── docker-compose.yml               # Langfuse + Postgres + Clickhouse
├── env.example
├── instrument/
│   ├── langfuse_client.py
│   ├── decorators.py                # @observe_node, @observe_llm, @observe_retriever
│   └── phoenix_side.py              # (선택) Phoenix 병행 관측
├── retrofit/
│   ├── agent_traced.py              # Day 10 agent — 모든 노드 @observe
│   ├── rag_traced.py                # Day 8 pipeline — step별 span
│   └── tools_traced.py              # Day 5 tools
├── resilience/
│   ├── retry_backoff.py             # tenacity
│   ├── rate_limiter.py              # aiolimiter (분당 RPM/TPM)
│   ├── circuit_breaker.py           # pybreaker 3상태
│   └── timeout.py                   # asyncio.timeout
├── caching/
│   ├── anthropic_cache.py           # cache_control: ephemeral, 5m / 1h
│   ├── openai_cache.py              # implicit prefix (cached_tokens 확인)
│   ├── gemini_cache.py              # client.caches.create (32k+)
│   └── bench.md                     # 비용 절감 표
├── streaming/
│   └── ttft_bench.py                # 3사 × 5회 → p50/p95
├── prompt_mgmt/
│   ├── upload_prompts.py            # Langfuse에 prompt 업로드
│   └── fetch_and_use.py
├── score_attach/
│   └── ragas_to_langfuse.py
├── alerts/
│   └── simple_rules.py              # latency > 10s 등 WARN/CRITICAL 로그
└── README.md
```

## 🚀 시작

```bash
cd projects/day11-observability
cp env.example .env   # LANGFUSE_HOST=http://localhost:3000 ...
docker compose up -d
open http://localhost:3000    # 최초 org/project 생성 → API key 발급

uv sync
uv add langfuse tenacity aiolimiter pybreaker
```

## ✅ 필수 기능

### Langfuse 기동
- [ ] docker-compose로 Postgres + Clickhouse + Langfuse web 3컨테이너 up
- [ ] localhost:3000 접속, org/project 생성, PK/SK 받아 `.env`
- [ ] `langfuse_client.py`에서 `Langfuse()` 싱글톤

### Agent/RAG retrofit
- [ ] `agent_traced.py` — 모든 노드에 `@observe(name="classifier", as_type="span")`
- [ ] LLM 호출은 `@observe(as_type="generation")` + `langfuse.update_current_observation(input=..., output=..., model=..., usage=...)`
- [ ] Retriever는 `as_type="retriever"` — retrieved chunks metadata에
- [ ] Tool은 `as_type="tool"`
- [ ] 사용자 식별: `langfuse.update_current_trace(user_id=..., session_id=...)`

### Prompt versioning
- [ ] `upload_prompts.py` — 하드코딩된 system prompts를 Langfuse에 업로드. label=`production`/`staging`
- [ ] `fetch_and_use.py`:
  ```python
  prompt = langfuse.get_prompt("rag_system", label="production")
  compiled = prompt.compile(context=ctx, question=q)
  ```
- [ ] UI에서 prompt 수정 → 재배포 없이 반영 (hot swap) 확인

### Score attach
- [ ] `ragas_to_langfuse.py`:
  ```python
  for row in ragas_results:
      langfuse.score(
          trace_id=row["trace_id"],
          name="faithfulness",
          value=row["faithfulness"],
          comment="Ragas evaluator_llm=sonnet-4.6"
      )
  ```

### Resilience 4
- [ ] `retry_backoff.py`:
  ```python
  @retry(
    wait=wait_random_exponential(min=1, max=60),
    stop=stop_after_attempt(6),
    retry=retry_if_exception_type((RateLimitError, APIConnectionError)),
    before_sleep=lambda rs: log.warning(f"retry {rs.attempt_number}")
  )
  ```
- [ ] `rate_limiter.py` — `AsyncLimiter(50, 60)` 분당 50
- [ ] `circuit_breaker.py` — `CircuitBreaker(fail_max=5, reset_timeout=60)` + fallback
- [ ] `timeout.py` — `async with asyncio.timeout(30)`

### Error 시뮬레이션
- [ ] SDK monkey-patch로 가짜 429 주입 → retry 극복 확인
- [ ] 가짜 500 연속 5번 → breaker open → 60s 후 half-open → closed

### Prompt Caching 3사 실측
- [ ] `anthropic_cache.py`:
  ```python
  system = [
    {"type":"text","text":"You are..."},
    {"type":"text","text": LONG_CONTEXT_5000_TOKENS, "cache_control":{"type":"ephemeral"}}
  ]
  # 첫 호출: usage.cache_creation_input_tokens = N
  # 재호출: usage.cache_read_input_tokens = N
  ```
- [ ] `openai_cache.py` — 같은 prefix 10회 → `usage.prompt_tokens_details.cached_tokens` 추이
- [ ] `gemini_cache.py`:
  ```python
  cache = client.caches.create(
    model="gemini-2.5-flash",
    contents=long_prefix,
    ttl="3600s"
  )
  # 이후 model 호출 시 cached_content=cache.name
  ```
- [ ] `bench.md` 표: baseline $ vs cached $ — 비용 절감률

### TTFT
- [ ] `ttft_bench.py`:
  - 3사 × 5회 streaming
  - 첫 chunk 도착 시점 기록 → p50/p95
  - 결과 표:
    ```
    Provider  | TTFT p50 | TTFT p95 | tok/s
    claude-haiku-4-5  | 1.1s | 2.3s | 82
    gpt-4o-mini       | 0.9s | 1.8s | 90
    gemini-flash      | 0.8s | 1.5s | 100
    ```

### Alerts
- [ ] `simple_rules.py` — latency > 10s / error rate > 5% / cache hit < 50% → stdout WARN

## 📊 수치 기준

| 메트릭 | 기준 |
|---|---|
| Langfuse dashboard trace 수집 | 20+ traces |
| Prompt fetch 성공 | 100% |
| Ragas score attach 확인 | 3+ scores |
| 가짜 429 → retry 극복 | ≥ 90% |
| Breaker trip/recovery 확인 | 1회 이상 |
| Anthropic prompt caching 비용 절감 | ≥ 40% |
| TTFT p50 (Anthropic/OpenAI/Gemini) | ≤ 2s |

## 🧨 실전 함정

1. **Langfuse Clickhouse 디스크 폭발** — partition TTL 설정 필수 (기본 없음)
2. **`@observe` 중첩 호출** — autolink 되지만 예외에 민감. flush() 명시적 호출 필요할 때
3. **Prompt caching prefix 1024 토큰 미만** — OpenAI/Anthropic 둘 다 적용 안 됨
4. **Anthropic `cache_control` 위치** — system 또는 message content block, tools에도 가능. 캐시할 것 끝에
5. **Breaker open 때 fallback 없음** — UX 붕괴. 친절 에러 메시지 또는 캐시된 답변 준비
6. **Rate limiter도 async** — sync client에 async limiter 쓰면 무의미
7. **Retry가 400도 재시도하면 악순환** — `retry_if_exception_type` 정확히
8. **PII가 trace에 그대로** — output sanitizer / PII mask 필수

## 🎁 Stretch

- 🧪 **Phoenix 병행** — OpenInference로 같은 span을 Langfuse + Phoenix에 동시
- 🧪 **LiteLLM proxy** — 앞단에 proxy 두고 unified logging + caching
- 🧪 **Batch API** — 대량 eval을 OpenAI batch endpoint로 → 50% 절감
- 🧪 **Cost budget alert** — 하루 $20 초과 시 fail-closed (app 자동 중지)
- 🧪 **User session replay** — session_id로 전체 여정 재생

## 🔗 다음에 쓰이는 곳

- Day 13: local LLM (Ollama/RunPod)에도 동일 trace
- Day 14: `app/observability/` + `app/resilience/` 이식
