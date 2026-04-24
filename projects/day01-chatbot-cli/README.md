# Day 1-2 — 3-Provider CLI Chatbot (+ Provider 추상화)

> **연결**: [`curriculum/week1-day01-llm-basics.md`](../../curriculum/week1-day01-llm-basics.md) · [`curriculum/week1-day02-api-providers.md`](../../curriculum/week1-day02-api-providers.md)
> **의존성**: Day 0 세팅 완료 (`.env` 3 API keys, `make verify` 통과)
> **다음**: Day 3 Prompt Lab이 이 CLI 위에서 돌아감

## 🎯 이 프로젝트로 확실히 될 것

1. 3사 SDK를 **손코드**로 불러 쓸 수 있음 (문서 없이 85%)
2. Streaming / Multi-turn / Token usage / Error handling이 **한 인터페이스**로 묶임
3. 토큰 해부학 — 같은 문장이 3사 다르게 tokenize됨을 수치로
4. Temperature/Top-p/Top-k가 logprob 분포를 어떻게 바꾸는지 실측
5. Rate limit / 429 / 529 / timeout 의도 재현 후 tenacity로 극복

## 📁 디렉토리

```
day01-chatbot-cli/
├── pyproject.toml                # uv 프로젝트
├── .env                          # OPENAI_API_KEY / ANTHROPIC_API_KEY / GOOGLE_API_KEY
├── chat.py                       # CLI 엔트리 — argparse로 모드 스위치
├── tokens.py                     # Task 1: 3사 토큰 비교 + 비용 추정
├── temperature_demo.py           # Task 2: sampling 그리드 + 다양성 점수
├── logprobs_demo.py              # Task 3 (Day 1): OpenAI logprobs 엔트로피
├── providers/
│   ├── __init__.py
│   ├── base.py                   # Protocol: chat / stream / count_tokens / price
│   ├── openai_client.py          # Responses API 우선, Chat Completions fallback
│   ├── anthropic_client.py       # messages + top-level system + prefill 지원
│   └── gemini_client.py          # google-genai 기준
├── usage.py                      # 3사 usage 필드 통합 → Usage dataclass
├── errors.py                     # 공통 에러 계층 (RateLimit/Auth/Timeout/Server/BadRequest)
├── retry.py                      # tenacity 래퍼 + 로그
├── history.py                    # multi-turn 저장/복원 (JSON)
├── prices.py                     # 모델별 $/1M in·out 테이블 (실측 기반)
├── results/                      # 실험 결과 저장 (gitignore)
└── README.md
```

## 🚀 시작

```bash
cd projects/day01-chatbot-cli
uv init
uv add openai anthropic google-genai tiktoken python-dotenv rich tenacity httpx
# 또는 공용 shared/ 환경 그대로 쓰고 싶으면 uv sync (workspace 설정시)

cp ../../.env ./.env          # 루트 .env를 재사용
```

## ✅ 필수 기능 체크리스트

### 토큰/샘플링 실습 (Day 1)
- [ ] `tokens.py` — `tiktoken cl100k_base` / `o200k_base` + Anthropic `count_tokens` + Gemini `count_tokens`로 5종 텍스트(한국어 500자 / 영어 500단어 / Python 코드 / JSON / 이모지 혼합) 카운트 + CPT 표 출력
- [ ] 같은 텍스트에 대해 **비용 추정 컬럼** 추가 (prices.py 사용)
- [ ] `temperature_demo.py` — temperature × top_p × top_k 6개 그리드 × 프롬프트 3종 × 5회. 결과 간 Levenshtein distance로 다양성 점수화
- [ ] `logprobs_demo.py` — OpenAI logprobs에서 top-5 token의 확률 + 분포 엔트로피 (`-Σ p log p`)
- [ ] `notes/concepts.md`에 "같은 '안녕하세요'의 3사 토큰 수" 표

### Provider 추상화 (Day 2)
- [ ] `providers/base.py` — `class Provider(Protocol)` with `chat(messages, *, stream=False, temperature=0.7, max_tokens=1024) -> Response | Iterator[str]`
- [ ] OpenAI 어댑터: Responses API 우선. Chat Completions는 legacy flag로
- [ ] Anthropic 어댑터: top-level `system=`, `max_tokens` 필수, `prefill` 옵션
- [ ] Gemini 어댑터: `system_instruction`, `Content/Part` 구조, safety_settings 완화 옵션
- [ ] `usage.py` — `class Usage(input_tokens, output_tokens, cache_creation, cache_read)` 3사 매핑
- [ ] `errors.py` — 공통 `RateLimitError / AuthError / TimeoutError / BadRequestError`로 3사 예외 변환

### CLI (`chat.py`)
- [ ] `--provider openai|anthropic|gemini` (default: anthropic)
- [ ] `--model` 모델 override
- [ ] `--stream` 스트리밍 모드
- [ ] `--system "..."` 시스템 프롬프트 주입
- [ ] `--compare "prompt"` — 3사 동시 호출, 결과 + latency + cost 표 (asyncio.gather)
- [ ] `--cache` — Anthropic cache_control 적용 long system prompt 시연
- [ ] `--dry` — 실제 호출 없이 토큰/비용만 예측
- [ ] `/save <file>` / `/load <file>` — 히스토리 저장/복원
- [ ] `/reset` — 히스토리 초기화
- [ ] 매 턴 `[in: N | out: M | total: K | $: 0.00xx | ms: ###]`

### Resilience (Day 2)
- [ ] `retry.py` — tenacity `@retry(wait=wait_random_exponential(min=1,max=60), stop=stop_after_attempt(6), retry=retry_if_exception_type((RateLimitError, APIConnectionError)))`
- [ ] 고의 부하 스크립트: `./scripts/flood.sh 50` — 50회 동시 호출로 429 유발 → retry 성공률 기록
- [ ] SDK에 monkey-patch로 fake 500 주입 → backoff 동작 확인

## 📊 수치 기준 (넘어야 할 선)

| 메트릭 | 기준 |
|---|---|
| `make verify` 통과 | 100% |
| 3사 동일 프롬프트 응답 성공률 | 100% (10연속) |
| `--stream` TTFT (Haiku) | ≤ 2s |
| `--compare`의 3사 병렬 latency (p50) | ≤ 가장 느린 단일 호출 * 1.1 |
| 고의 429 유발 시 retry 극복 | ≥ 90% |
| Temperature 0 동일 프롬프트 출력 일치율 | ≥ 95% (5회) |

## 🧨 실전 함정

1. **Anthropic `max_tokens` 누락** → 400. 필수 파라미터.
2. **Gemini `SAFETY` finish_reason** → finish_reason 먼저 체크. content가 빈 게 정상.
3. **OpenAI Responses API `input=` vs Chat `messages=`** 혼동. 추상화 레이어에서 분기.
4. **Streaming 중 usage 안 나옴** → OpenAI는 `stream_options={"include_usage": True}` 필수.
5. **tiktoken이 Anthropic/Gemini 토큰과 다름** → 모델별 tokenizer 맞춰야 정확.
6. **Rate limit retry 시 400 섞임** → `retry_if_exception_type` 정확히.
7. **.env 재로딩 안 됨** → uv run 때마다 `python-dotenv`의 `override=True` 확인.

## 🎁 Stretch

- 🧪 Raw HTTP 모드 — 1 provider만 httpx 직접 호출 (SSE 파싱 포함)
- 🧪 Logprob 색상 렌더링 — rich로 token별 confidence를 배경색으로
- 🧪 `--tool` 미리보기 — tool_use가 응답에 있으면 경고 (Day 5 전초)
- 🧪 Anthropic Extended Thinking — `thinking: {"type": "enabled", "budget_tokens": 2000}`

## 🔗 이 프로젝트가 다음에 쓰이는 곳

- Day 3: Prompt Lab이 `providers/*` 를 그대로 import
- Day 5: tool use 추가 (이 CLI가 agent로 진화)
- Day 14: `providers/registry.py`로 포팅되어 final portfolio의 LLM 라우터
