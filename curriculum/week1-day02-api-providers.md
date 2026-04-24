# Day 2 — 3대 Provider API 실전 (ULTRA)

> **난이도**: ★★★ (v3)
> **총량**: 읽기 4h + 실습 6h + Prompt Caching 선행 1h + 정리 1h = **12h**.
> **목표**: "OpenAI / Anthropic / Gemini 공식 문서를 보지 않고도 각 SDK로 chat / stream / multi-turn / system prompt / token usage까지 칠 수 있는 수준" + **Prompt Caching 선행 경험** (Day 12에서 풀스펙).
> **논문**: RAG (Lewis 2020) Figure 1 + Abstract

## 🎯 오늘 끝나면

1. 3사 SDK의 **요청 스키마**와 **응답 객체 구조**를 다이어그램 없이 한국어로 설명
2. 동일 기능을 3사 provider로 구현한 얇은 **Provider 추상화 계층** (`ai_study.llm`)을 짜봤다
3. **Streaming의 3사 차이**를 코드 레벨에서 구분: OpenAI chunked JSON SSE / Anthropic `event:` 구분된 SSE(with `message_start`, `content_block_delta`, `message_stop`) / Gemini `AsyncGenerator[GenerateContentResponse]`
4. **429 / 529 / 500 / timeout** 상황을 의도적으로 만들어보고, tenacity로 backoff + jitter 재시도를 붙였다
5. **Token accounting** — 호출 1회마다 `input / output / cache_creation / cache_read` 토큰을 로그에 기록하는 유틸을 갖고 있다

## 📚 자료

### 🔥 필수

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 45m | [OpenAI API Reference](https://platform.openai.com/docs/api-reference) | 공식 API 사전. Chat Completions vs Responses API 섹션을 비교하며 읽을 것. **Responses API는 2024년 후반 등장**, tool/file/reasoning을 first-class로 다룸. |
| 45m | [OpenAI — Migrate to Responses API](https://platform.openai.com/docs/guides/migrate-to-responses) | 신규 프로젝트는 Responses API 권장. stateful conversation, builtin tools, structured output이 훨씬 깔끔. |
| 45m | [Anthropic — Build with Claude](https://docs.anthropic.com/en/docs/build-with-claude/overview) | messages API 중심. **system은 top-level**, messages는 user/assistant만. 중요: prefill assistant message로 출력 제어 가능. |
| 30m | [Anthropic — Client SDKs](https://docs.anthropic.com/en/api/client-sdks) | python/ts sdk 전반. sync vs async, `client.messages.stream()` vs `stream=True` 차이. |
| 30m | [Gemini API Quickstart](https://ai.google.dev/gemini-api/docs/quickstart) | `google-genai` (2024년 신) SDK 기준. `google-generativeai` (구) 는 레거시. |
| 30m | [Gemini — Text Generation](https://ai.google.dev/gemini-api/docs/text-generation) | `contents=[Content(parts=[Part(text=...)])]`의 구조. 대화는 `chats.create(history=...)`. |
| 2h | [Anthropic Courses — anthropic_api_fundamentals](https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals) | **9개 notebook 순서대로 따라치기**. API 기본부터 에러 처리, streaming, token counting, model selection까지 실습 위주. 오늘의 "정답 트랙". |

### ⭐ 강력 권장

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 30m | [OpenAI Cookbook — How to count tokens](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken) | Chat 메시지 하나가 "role + content + 구분자"로 이루어지기 때문에 단순 `len(encode(content))`가 아닌 이유 설명. |
| 30m | [OpenAI Cookbook — Handle rate limits](https://cookbook.openai.com/examples/how_to_handle_rate_limits) | Tenacity + `wait_random_exponential` 표준 패턴. 내일 Day 12와 연결됨. |
| 30m | [Anthropic — Streaming](https://docs.anthropic.com/en/docs/build-with-claude/streaming) | 이벤트 타입 9가지를 외우지 말고 `message_start / content_block_start / content_block_delta / content_block_stop / message_delta / message_stop` 플로우 1개 그림으로. |
| 20m | [LiteLLM unified API](https://docs.litellm.ai/docs/) | "provider 추상화를 직접 짤지, LiteLLM에 맡길지" 결정 근거. **오늘은 직접 짜봐야 감이 옴**, 프로덕션에선 LiteLLM 고려. |

### 🎓 선택

- [OpenAI Responses API + Tool orchestration cookbook](https://cookbook.openai.com/examples/responses_api/responses_api_tool_orchestration) — Day 5 예습.
- [Anthropic cookbook repo](https://github.com/anthropics/anthropic-cookbook) — 나중 재료.
- [aisuite (Andrew Ng)](https://github.com/andrewyng/aisuite) — LiteLLM 경쟁작. 얇음.

## 🔬 실습 (5.5h)

### 프로젝트: 3-Provider CLI 챗봇 + `ai_study.llm` 추상화

위치: `projects/day01-chatbot-cli/`

```
day01-chatbot-cli/
├── .env                    # OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY
├── chat.py                 # argparse로 --provider / --stream / --compare / --cache
├── providers/
│   ├── __init__.py
│   ├── base.py             # Provider(Protocol): chat / stream / count_tokens
│   ├── openai_client.py    # OpenAI Responses API 우선
│   ├── anthropic_client.py
│   └── gemini_client.py
├── usage.py                # Usage 객체 통합 (3사 필드명 다름)
├── errors.py               # 공통 에러 계층 (RateLimit, Auth, Timeout, Server)
├── retry.py                # tenacity 래퍼
└── README.md
```

### 🔥 필수 기능 (6개)

1. **System prompt 지원** — 3사 방식 다르므로 추상화 레이어가 내부에서 변환
   - OpenAI (Chat Completions): `messages[0]` / (Responses): `instructions=`
   - Anthropic: 호출 파라미터 top-level `system=`
   - Gemini: `config={"system_instruction": ...}` or `Client.chats.create(config=...)`
2. **Streaming 모드** (`--stream`)
   - OpenAI: `stream=True` → `chunk.choices[0].delta.content`
   - Anthropic: `client.messages.stream()` context manager → `text_stream` iterable
   - Gemini: `client.models.generate_content_stream(...)` → `for chunk in ...: chunk.text`
3. **Multi-turn 대화 유지** — `history` 리스트, `/reset`, `/save`, `/load` 명령
4. **Token usage 출력** — 매 턴마다 `[input: N | output: M | total: K | est_cost: $0.00xx]`
5. **에러 처리** — 429(retry) / 401(exit with help) / 400(dump request for debug) / 529(backoff) / timeout(retry with longer)
6. **Dry-run 모드** (`--dry`) — 실제 호출 없이 토큰 수와 추정 비용만 출력

### 🔥 Stretch (반드시 2개 이상)

- ⭐ `--compare` — 동일 프롬프트를 **3사 병렬 호출**(asyncio.gather) 후 응답/지연/비용을 표로 정렬
- ⭐ `--cache` — Anthropic `cache_control: {"type": "ephemeral"}`를 system prompt에 걸고, 두 번째 호출에서 `cache_read_input_tokens` 발생 확인
- 🧪 **Raw HTTP 모드** — 1개 provider에 대해서 SDK 없이 `httpx`로 직접 호출(SSE 파싱 포함). SDK가 감춰놓은 것을 체감.
- 🧪 **Logprobs 활용** — OpenAI logprobs로 "모델 자신감(confidence)"을 빨간/노랑/초록 색으로 터미널에 찍기 (rich + logprob to color)
- 🧪 **Function/Tool call 감지** — tool_use가 응답에 있으면 경고 (Day 5 예고편)

### 테스트 시나리오 (스스로 돌려보기)

```bash
python chat.py --provider anthropic --stream
python chat.py --provider openai --compare "서울 날씨 한 줄로"
python chat.py --provider gemini --dry "긴 system prompt 넣고 토큰 추정"
# Rate limit 터뜨리기: 0.1초 간격으로 50회 호출
for i in {1..50}; do python chat.py --provider anthropic "hi" & done
```

### 🧠 배울 점 (실습 중 반드시 관찰)

- **토큰 수 차이**: 같은 "안녕하세요"에 대해 3사 token count가 다르다. Usage 객체의 필드명도 다르다 (`input_tokens` vs `prompt_tokens` vs `prompt_token_count`).
- **Streaming first chunk 도착 시간(TTFT)**: Anthropic이 빠른 편, Gemini도 빠름, OpenAI는 모델/리전에 따라 다름.
- **Anthropic의 `stop_reason`**: `end_turn` / `max_tokens` / `tool_use` / `stop_sequence`. 이 값 체크 안 하면 잘린 응답을 완성된 걸로 착각.
- **Gemini의 `finish_reason`**: `STOP` / `MAX_TOKENS` / `SAFETY` / `RECITATION`. SAFETY 차단 자주 만난다.
- **OpenAI Responses API의 `previous_response_id`**: 서버 측에 대화 상태를 저장해서 클라이언트가 history 안 보내도 됨.

## 💰 비용 체감 실험 (0.5h)

`cheatsheets/api-compare.md`에 **2026년 4월 기준 실측 시세**를 표로 업데이트하라 (API dashboard에서 직접 확인):

```
모델                      in $/1M    out $/1M   비고
gpt-4o-mini              0.15       0.60       cheap workhorse
gpt-4o                   2.50       10.00      quality
claude-haiku-4-5         1.00       5.00       Anthropic workhorse
claude-sonnet-4-6        3.00       15.00      quality flagship
gemini-2.5-flash         0.10       0.40       cheapest
gemini-2.5-pro           1.25       10.00      ...
```

동일 프롬프트 1000번 호출 시 예상 비용을 계산하고, "실험은 flash/mini/haiku, production은 sonnet/4o/pro" 룰을 본인 노트에 기록.

## ✅ 체크리스트

- [ ] 3사 SDK `pip list`로 설치 확인 (`openai`, `anthropic`, `google-genai`)
- [ ] 3사 첫 호출 성공 (`make verify` 통과)
- [ ] Streaming 모드 동작 (터미널에 토큰 단위 출력)
- [ ] Multi-turn 5턴 이상 대화 + `/save` → 재시작 → `/load`
- [ ] 고의로 rate limit 유발 후 tenacity가 지수 백오프로 복구
- [ ] 400 에러 발생 시 request body 덤프해서 원인 디버깅해봤음
- [ ] `--compare` 출력에 3사 응답 + latency + cost 표 정렬
- [ ] `cheatsheets/api-compare.md` 본인이 직접 만든 비교표로 덮어쓰기
- [ ] `notes/keywords.md` — role / streaming / SSE / stop_reason / finish_reason / response_format / tool_choice 추가

## 🧨 자주 틀리는 개념

1. **"System prompt는 messages[0]에 넣어야 한다"** — OpenAI는 맞지만, **Anthropic은 금지**. messages에 system 넣으면 400.
2. **"Anthropic의 `max_tokens`는 optional"** — **false. 필수.** 생략하면 400.
3. **"Streaming 모드에서 usage는 안 나온다"** — 3사 모두 마지막 chunk(OpenAI: `stream_options={"include_usage": True}` 지정 필요)에 usage 포함. 옵션 안 키면 못 얻음.
4. **"Gemini의 SAFETY 차단은 프롬프트만 고치면 됨"** — `safety_settings`로 threshold 완화 가능. 기본이 보수적.
5. **"토큰 카운트 SDK가 정확"** — Anthropic은 `client.messages.count_tokens(...)` 정확한 서버 카운트 제공. OpenAI는 `tiktoken`이 근사(+/-2-3 tok). Gemini는 `count_tokens` 서버 메소드.
6. **"Responses API에서도 `messages`를 쓴다"** — 아니다. Responses는 `input=` 단일 필드 (string or list of turns). 스키마가 다르다.

## 🧪 산출물

- `projects/day01-chatbot-cli/chat.py`, `providers/*.py`, `retry.py`, `usage.py`
- `cheatsheets/api-compare.md` (본인이 실측한 비용표 포함)
- `notes/daily-log.md` — Day 2 회고: "가장 놀란 차이점 1개"

## 📌 핵심 키워드

- role (system/user/assistant/model), Chat Completions vs Responses API, messages vs input
- streaming SSE, `data: {...}` 포맷, chunked transfer, TTFT
- `stop_reason` / `finish_reason`, max_tokens cutoff
- `response_format`, JSON mode vs Structured Outputs (strict)
- Anthropic: top-level `system`, prefill, `cache_control`, `thinking` block (extended thinking)
- OpenAI: Responses API, `previous_response_id`, built-in tools, `instructions`
- Gemini: `Content/Part`, `system_instruction`, `safety_settings`, `thinking_budget`

## 🎁 내일(Day 3) 미리보기
Prompt engineering — Anthropic Interactive Tutorial 9챕터. XML structured / prefill / CoT / self-critique / few-shot. 오늘 만든 챗봇에 프롬프트 패턴 10개 태우는 게 내일 과제.
