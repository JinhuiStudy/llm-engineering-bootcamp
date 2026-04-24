# Day 12 — Observability + Productionization

## 목표
- LLM 앱의 **trace / cost / latency / prompt version**을 관측
- Langfuse로 Day 9/10 프로젝트에 tracing 붙이기
- Phoenix로 보조적 eval 관측
- Rate limit / streaming / prompt caching 3사 차이와 대응 패턴 체화

## 자료

### Observability
| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [Langfuse docs](https://langfuse.com/docs) | 1.5h |
| 필수 | [Langfuse tracing](https://langfuse.com/docs/tracing) | 1h |
| 필수 | [Langfuse prompt management](https://langfuse.com/docs/prompt-management/overview) | 1h |
| 필수 | [Langfuse scores / evals](https://langfuse.com/docs/scores/overview) | 0.5h |
| 선택 | [Arize Phoenix](https://docs.arize.com/phoenix) | 1h |
| 선택 | [LangSmith](https://docs.smith.langchain.com/) | 선택 |

### Production
| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [OpenAI — rate limits](https://platform.openai.com/docs/guides/rate-limits) | 0.5h |
| 필수 | [OpenAI Cookbook — handle rate limits](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_handle_rate_limits.ipynb) | 0.5h |
| 필수 | [OpenAI Cookbook — stream completions](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb) | 0.5h |
| 필수 | [OpenAI — prompt caching](https://platform.openai.com/docs/guides/prompt-caching) | 0.5h |
| 필수 | [Anthropic — prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) | 0.5h |
| 필수 | [Anthropic — streaming](https://docs.anthropic.com/en/docs/build-with-claude/streaming) | 0.5h |
| 필수 | [Gemini — caching](https://ai.google.dev/gemini-api/docs/caching) | 0.5h |
| 선택 | [OpenAI — latency optimization](https://platform.openai.com/docs/guides/latency-optimization) | 0.5h |

## 실습 (4.5h)

### 프로젝트: Observability 통합
위치: `projects/day11-observability/`

```
day11-observability/
├── docker-compose.yml       # Langfuse self-hosted (Postgres + Clickhouse)
├── instrument.py            # Langfuse SDK decorator/wrapper
├── retrofit/
│   ├── rag_traced.py        # Day 8 RAG에 @observe decorator 추가
│   ├── agent_traced.py      # Day 10 LangGraph agent에 tracing
│   └── tool_traced.py
├── rate_limit/
│   ├── retry_backoff.py     # tenacity 기반 지수 백오프
│   └── semaphore.py         # 동시 요청 제한
├── caching/
│   └── prompt_cache_demo.py # Anthropic cache_control 시연
└── README.md
```

### 요구사항
1. **Langfuse self-hosted** 로컬 띄우기 (docker-compose, 무료)
2. Day 8 RAG 파이프라인 모든 step에 trace
3. Day 10 LangGraph 각 노드에 trace
4. Dashboard에서 trace / cost / latency 확인
5. Prompt를 Langfuse에서 관리 (versioning)
6. Day 9 Ragas 결과를 Langfuse score로 기록
7. **Rate limit 대응**: `tenacity`로 exponential backoff + jitter
8. **Prompt caching**: Anthropic에 긴 system prompt 붙여 cache hit 확인 (usage에서 `cache_creation_input_tokens`, `cache_read_input_tokens` 확인)

### Stretch
- Phoenix로 동일 trace 병행 관측
- Alert 룰 (예: latency > 10s 시 로그)

## 체크리스트

- [ ] Langfuse dashboard에 본인 trace 뜨는 것 확인
- [ ] 한 요청의 cost / latency 브레이크다운 할 수 있음
- [ ] Prompt를 코드에서 분리해 Langfuse에서 가져오도록 수정
- [ ] Rate limit error 재현 → retry 정책으로 극복
- [ ] Anthropic prompt caching으로 토큰 비용 50%+ 절감 확인

## 핵심 키워드
- Trace, span, observation, session, user_id (관측 식별자)
- Latency p50/p95/p99, time-to-first-token (TTFT), tokens-per-second
- Cost tracking (model별 $/1M tokens)
- Prompt versioning, A/B prompt, rollback
- Rate limit: RPM, TPM, backoff, jitter, circuit breaker
- Streaming (SSE), chunked transfer
- Prompt caching (Anthropic cache_control, OpenAI implicit caching, Gemini explicit cache)
