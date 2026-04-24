# Production LLM Patterns 치트시트

"실험에서 production으로" 넘어갈 때 반드시 챙기는 10가지.

## 1. Prompt Caching (3사 비교)

| Provider | 방식 | 최소 prefix | TTL | 할인 |
|---|---|---|---|---|
| OpenAI | **Implicit** | ~1024 토큰 | 5-10m | ~50% on `cached_tokens` |
| Anthropic | **Explicit** `cache_control: {"type": "ephemeral"}` | 1024 / 2048 (model별) | 5m / 1h (extended) | 읽기 -90%, 쓰기 +25% |
| Gemini | **Explicit** `client.caches.create()` | 32,768 | 사용자 지정 | 프리픽스 기본 요금 할인 |

```python
# Anthropic
system = [
  {"type": "text", "text": "You are..."},
  {"type": "text", "text": LONG_CONTEXT, "cache_control": {"type": "ephemeral"}}
]
# 첫 호출: usage.cache_creation_input_tokens = N
# 재호출: usage.cache_read_input_tokens = N   ← 90% 할인
```

## 2. Streaming (UX 생명)

- SSE로 첫 토큰까지 **TTFT 1-2s 목표**
- FastAPI:
  ```python
  @app.post("/chat")
  async def chat(req):
      async def gen():
          async for chunk in llm.astream(req.messages):
              yield f"data: {json.dumps(chunk)}\n\n"
      return StreamingResponse(gen(), media_type="text/event-stream")
  ```
- Streaming 중 usage 받기: OpenAI `stream_options={"include_usage": True}`, Anthropic은 `message_delta` 이벤트

## 3. Retry (tenacity 표준)

```python
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_exception_type

@retry(
    wait=wait_random_exponential(min=1, max=60),
    stop=stop_after_attempt(6),
    retry=retry_if_exception_type((RateLimitError, APIConnectionError)),
    before_sleep=lambda rs: log.warning(f"retry {rs.attempt_number}")
)
def safe_call(...):
    return client.messages.create(...)
```
- 400은 retry 금지 (요청 자체 오류)
- 429/500/502/503/529만

## 4. Rate Limiting (client-side)

```python
from aiolimiter import AsyncLimiter
limiter = AsyncLimiter(50, 60)  # 분당 50

async with limiter:
    await call()
```
- RPM / TPM 둘 다 관리
- Burst 허용치 고려 (tier별 다름)

## 5. Circuit Breaker

```python
import pybreaker
breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=60)

@breaker
def call():
    return client.messages.create(...)
```
- Closed → 정상. Open → 즉시 실패. Half-open → 재시도 1번.
- Open 상태 때 **fallback 답변** 준비 (캐시된 FAQ, 친절 에러)

## 6. Timeout

```python
async with asyncio.timeout(30):
    await call()
# or
client = Anthropic(timeout=30.0)  # SDK 레벨
```
- Streaming 중엔 per-token timeout 아닌 overall 적용 주의

## 7. Observability (Langfuse / Phoenix / LangSmith)

```python
from langfuse import observe, get_client

@observe(name="rag_pipeline")
def rag(q):
    @observe(name="retrieve", as_type="retriever")
    def ret(q): ...
    @observe(name="generate", as_type="generation")
    def gen(q, ctx): ...
    ...
```
- 모든 LLM 호출 / Tool 호출 / Retrieval을 **span**으로
- 필수 속성: model, prompt_tokens, completion_tokens, cost, latency
- 사용자 식별: session_id, user_id, trace_id
- **PII 마스킹 필수**

## 8. Prompt Versioning

- Langfuse / LangSmith / 자체 DB에 prompt 저장
- Label: `production` / `staging` / `experiment-a`
- Compile time에 variable 주입
- Hot swap — UI에서 수정 → 앱 재배포 없이 반영

## 9. Cost Tracking

```python
# 매 호출
cost = tokens_in * $/1M_in + tokens_out * $/1M_out
log.info(...)
langfuse.update_current_trace(metadata={"cost_usd": cost})
```
- 일/주/월 리포트 자동 생성
- **Alert** 설정 (하루 $20 초과 등)
- User별 quota 관리

## 10. Idempotency

중복 호출 방지:
- OpenAI: `extra_headers={"idempotency-key": key}` (2024 지원)
- 자체 캐시 / Redis로 request_hash → response

## 11. Batch API (50% 절감)

| Provider | 엔드포인트 | SLA | 할인 |
|---|---|---|---|
| OpenAI | `/v1/batches` | 24h | 50% |
| Anthropic | `/v1/messages/batches` | 24h | 50% |
| Gemini | `batch` mode | 24h | 할인 |

대량 classification / extraction / eval에 필수. 실시간은 아님.

## 12. Security — OWASP LLM Top 10

- **Prompt Injection** (Day 3) — sandwich / canary / classifier
- **Sensitive Info Disclosure** — output filter (PII regex + LLM classifier)
- **Insecure Output Handling** — HTML/JS escape, SQL param
- **Model DoS** — rate limit, timeout, token cap
- **Supply Chain** — pinned SDK versions, SBOM
- **Tool abuse** — allowlist + sandbox (Day 5)

## 프로덕션 체크리스트 (배포 전)

- [ ] API key → secrets manager (Vault/AWS SM/1Password)
- [ ] `.env` 커밋 안 됨 (`.gitignore` 점검)
- [ ] Retry + Circuit breaker + Timeout 3종 set
- [ ] Langfuse trace 수집
- [ ] Prompt caching 적용 (system prompt 긴 경우)
- [ ] Streaming TTFT p95 < 3s
- [ ] Ragas CI gate (faithfulness ≥ 0.8)
- [ ] Cost alert daily $X
- [ ] Error rate alert > 5%
- [ ] Latency alert p95 > 10s
- [ ] User session 추적 (session_id)
- [ ] PII 마스킹 in logs
- [ ] License 검토 (모델 / SDK)
- [ ] Rollback plan (이전 prompt 버전 복귀 절차)

## 참고

- [Anthropic — Latency optimization](https://docs.anthropic.com/en/docs/build-with-claude/message-batches)
- [OpenAI — Rate limits](https://platform.openai.com/docs/guides/rate-limits) / [Latency guide](https://platform.openai.com/docs/guides/latency-optimization)
- [Langfuse docs](https://langfuse.com/docs)
- [OpenTelemetry GenAI conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
