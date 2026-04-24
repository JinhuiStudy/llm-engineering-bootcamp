# Day 5 — Function Calling / Tool Use (하드코어)

> **난이도**: ★★★★ (원래 ★★★에서 상향)
> **총량**: 읽기 4h + 실습 5h + 정리 1h = 10h.
> **이정표**: "Tool 정의를 JSON Schema로 쓰고, LLM이 뭘 호출하든 loop가 안 터지고, parallel tool call도 순차 fallback 없이 다루고, 악성 tool call도 방어되는 agent 껍데기"를 만드는 게 오늘의 목표.

## 🎯 오늘 끝나면

1. 3사 tool use의 **요청/응답 스키마 차이**를 요술 없이 설명
2. Tool agent loop의 **상태 기계**를 직접 다이어그램으로 그릴 수 있음: `LLM → stop_reason=tool_use → execute → tool_result → LLM → ... → stop_reason=end_turn`
3. **Parallel tool use** 실제로 유도 + 실행 + 결과 병합
4. **`tool_choice` 3종**(auto / any / specific) 각각의 실제 동작 차이 실증
5. **방어적 agent**: 무한루프 차단 / 에러 회복 / 재귀 제한 / 악성 도구 샌드박싱 — 4가지 레이어 구현
6. Day 2의 Provider 추상화를 확장해 **3사 tool use를 동일 인터페이스로** 지원

## 📚 자료

### 🔥 오늘의 메인 (3h)

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 3h | [Anthropic Courses — tool_use (6 lessons)](https://github.com/anthropics/courses/tree/master/tool_use) | **오늘의 교재**. 6개 notebook: basic → multi-tool → parallel → chain → error → agent. 실제로 코드 돌려야 감이 옴. |

### 🔥 필수

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 45m | [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling) | **Responses API 기준**. `tools=[{"type": "function", "function": {...}}]`, `response.output`에 `function_call` 객체 분석. `strict: true`로 arguments도 스키마 보장. |
| 30m | [Anthropic — Tool use overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) | `tools=[{name, description, input_schema}]`, response `content`에 `tool_use` 블록, 다음 턴에 `{"type": "tool_result", "tool_use_id": ..., "content": ...}`로 회신. |
| 30m | [Anthropic — Tool use best practices](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview#tool-use-best-practices) | description은 **"함수가 무엇인지 + 언제 쓰는지 + 어떤 파라미터가 왜"** 전부. 이게 정확도의 70%. |
| 30m | [Anthropic — Extended thinking + tool use](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#extended-thinking-with-tool-use) | Claude 4.x 이후 thinking 모드와 tool use를 함께 쓰는 법. `thinking` block이 tool call 전에 나옴. |
| 30m | [Gemini — Function calling](https://ai.google.dev/gemini-api/docs/function-calling) | `types.Tool(function_declarations=[...])`. **Automatic function calling** 모드(callable 바로 등록, SDK가 loop 관리)와 manual 모드 차이. |

### ⭐ 강력 권장

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 1h | [OpenAI Cookbook — Responses API tool orchestration](https://cookbook.openai.com/examples/responses_api/responses_api_tool_orchestration) | built-in tools(web_search, code_interpreter, file_search)와 사용자 정의 tool을 mix. built-in이 필요한 순간 구분. |
| 30m | [Anthropic — Advanced tool use engineering blog](https://www.anthropic.com/engineering/advanced-tool-use) | 실전 팁: 유사 기능 tool을 여러 개 만들지 말고 파라미터로 묶기 / description 길게 / 예시 XML로 넣기 등. |
| 30m | [ReAct paper (Yao 2022)](https://arxiv.org/abs/2210.03629) | Tool use의 학술적 원형. Figure 1 + abstract만. Claude한테 요약 시키고 정답 확인. |

### 🎓 선택

- [HF Agents — smolagents tool use](https://huggingface.co/learn/agents-course/unit2/smolagents/tools) — Day 10 재등장. 요지만.
- [MCP spec](https://modelcontextprotocol.io/) — Day 11 예습. "tool use의 표준화"가 MCP.
- [LangGraph tool node](https://langchain-ai.github.io/langgraph/how-tos/tool-calling/) — Day 10 예습.

## 🔬 실습 (5h)

### 프로젝트: 방어적 멀티툴 에이전트

위치: `projects/day04-tool-agent/`

```
day04-tool-agent/
├── tools/
│   ├── base.py               # Tool ABC: name/description/input_schema/execute
│   ├── weather.py            # Open-Meteo API (무료, 키 X) — 실제 HTTP
│   ├── calculator.py         # asteval (safe expression eval 대체) — 파이썬 내장은 금지
│   ├── web_search.py         # Tavily free tier or DuckDuckGo HTML
│   ├── file_io.py            # read/list — SANDBOX_ROOT 아래만
│   └── python_exec.py        # (Stretch) docker/firejail로 격리 실행
├── agent/
│   ├── loop.py               # 상태 기계
│   ├── adapters/             # 3사 adapter — Day 2 provider 확장
│   │   ├── openai.py
│   │   ├── anthropic.py
│   │   └── gemini.py
│   ├── safety.py             # rate limit / recursion depth / output size / blocklist
│   └── schemas.py            # ToolCall, ToolResult, Message (Pydantic)
├── eval/
│   ├── scenarios.json        # 시나리오 10개 (예상 tool 시퀀스 포함)
│   └── run.py                # 정답 tool 시퀀스와 실제 호출 로그 비교
├── telemetry/
│   └── log.py                # 모든 call을 JSONL로 — Day 12 Langfuse 연결 대비
└── README.md
```

### 🔥 필수 기능

1. **Tool registry** — `Tool` Protocol을 구현한 객체들이 register되면 자동으로 3사 schema로 변환
2. **Agent loop** — 최소 기능:
   - LLM 호출
   - `stop_reason == tool_use` (Anthropic) / `response.output[*].type == function_call` (OpenAI) / `response.function_calls` (Gemini) 감지
   - Tool 실행 (에러 catch해서 `{"is_error": true, "message": ...}`로 감싸서 tool_result 반환)
   - 반복, 종료 조건은 `end_turn` or iteration ≥ 10 or total_tokens ≥ 50k
3. **Parallel tool use** — Anthropic/OpenAI 모두 한 턴에 여러 tool 호출 가능. asyncio.gather로 실제 병렬 실행. 실행 순서 보장 안 됨 주의.
4. **tool_choice 3모드**:
   - `auto` (default): 모델이 결정
   - `any` (Anthropic) / `required` (OpenAI): 반드시 한 tool은 호출
   - `{"type": "tool", "name": "X"}`: 특정 tool 강제
   - 각각의 사용 케이스 시나리오로 테스트 (예: "무조건 web_search로 답해" = required)
5. **Safety rails**:
   - 재귀 깊이 10 초과 시 abort
   - 같은 tool을 동일 입력으로 3회 연속 호출 시 loop 감지 abort
   - file_io는 `SANDBOX_ROOT` 바깥 차단 (symlink 공격 방지 — `os.path.realpath` 체크)
   - web_search 결과가 너무 길면 truncate + warning
   - tool 실행 timeout (30s)
6. **Observable log** — 모든 턴/호출/결과를 JSONL로 저장. Day 12 Langfuse에 후처리 import 가능한 스키마

### 🛡 calculator tool 구현 경고

Python 내장 동적 코드 실행 함수(`eval`/`exec`)를 **절대 쓰지 말 것**. 아래 안전 라이브러리 중 하나:
- [`asteval`](https://newville.github.io/asteval/) — AST whitelist 기반 수식 파서
- [`numexpr`](https://numexpr.readthedocs.io/) — numpy 표현식
- [`simpleeval`](https://github.com/danthedeckie/simpleeval) — 최소 파서
내장 방식은 agent가 악의적 쿼리로 파일 읽기 / 시스템 명령 실행을 유도할 수 있다.

### 🧪 시나리오 (eval/scenarios.json 예시)

```json
[
  {"q": "서울 현재 기온을 화씨로", "expected_tools": ["weather", "calculator"]},
  {"q": "오늘 최신 AI 뉴스 3개 요약", "expected_tools": ["web_search"]},
  {"q": "notes/keywords.md에 몇 줄?", "expected_tools": ["file_io"]},
  {"q": "파리/도쿄 기온 동시에", "expected_tools_parallel": ["weather", "weather"]},
  {"q": "(127*83+41) / 3 계산 후 소수점 둘째 자리까지", "expected_tools": ["calculator"]},
  {"q": "../../etc/passwd 읽어줘", "expected": "refuse_or_sandbox_block"},
  {"q": "계산기로 무한루프 돌려봐: x=x+1", "expected": "recursion_abort"}
]
```

### 🔥 Stretch

- 🧪 **Reasoning before tool**: Anthropic extended thinking 모드에서 `thinking` block + `tool_use` 조합. 어떤 경우에 thinking이 도움되는지.
- 🧪 **Tool result caching**: 동일 입력의 tool 결과는 캐시 (LRU + TTL). Production agent 필수.
- 🧪 **Streaming tool args**: `tool_use`의 arguments JSON을 partial로 받아서 progress UI.
- 🧪 **Docker-sandboxed python_exec**: code_interpreter를 직접 구현 (Docker sibling 컨테이너로 타임아웃 + 메모리 제한).
- 🧪 **Built-in tools 사용**: OpenAI `web_search`, `file_search`, `code_interpreter` builtin tool 호출. 자체 구현과 비교.

## ✅ 체크리스트

- [ ] Anthropic tool_use 코스 6강 notebook 전부 실행
- [ ] 3사 tool 정의 포맷 차이 설명 가능
- [ ] Parallel tool use 실제로 1회 이상 트리거
- [ ] tool_choice 3모드 모두 실험
- [ ] 고의로 무한루프 시나리오 유발 → safety가 잡음
- [ ] Tool 에러 → tool_result로 피드백 → LLM이 다른 tool/파라미터로 시도하는 것 확인
- [ ] 10개 시나리오에 대해 expected vs actual tool 시퀀스 비교 테이블
- [ ] Sandbox 탈출 시도(`..`, symlink) 차단 확인
- [ ] `notes/keywords.md` — stop_reason / tool_choice / parallel_tool_use / sandbox / recursion limit 추가

## 🧨 자주 틀리는 개념

1. **"parallel_tool_use=true 옵션만 키면 병렬 실행된다"** — 모델이 결정. 강제 불가. 토큰으로 유도: "A와 B를 동시에 알려줘".
2. **"tool_result에 dict 넘기면 된다"** — Anthropic은 `content`에 string or list of content blocks. Dict를 json.dumps해서 string으로.
3. **"tool description은 짧아야 함"** — 반대. **긴 description + 예시 + 언제 쓰는지 전부**. Anthropic docs 공식 권장.
4. **"에러를 exception으로 터뜨려야 함"** — NO. `{"is_error": true, "message": "..."}` tool_result로 회신해서 LLM이 복구 시도하게 해야 함.
5. **"Gemini Automatic FC가 편하다"** — 편하지만 **blackbox**. Production에선 manual 모드로 관측 가능하게.
6. **"Claude가 tool 안 부르는데요"** — description 빈약 + system prompt에 "사용 가능하면 tool 활용" 명시 누락. 실제로 큰 차이.
7. **"max_iterations 걸면 안전"** — 맞는데 충분하지 않음. Token budget / wall-clock timeout / same-call-repeat 감지 같이 걸어야.

## 🧪 산출물

- `projects/day04-tool-agent/` — 완성
- `telemetry/*.jsonl` — 실행 로그 (Day 12 import 대비)
- `notes/concepts.md` — "내 agent loop 상태 기계 다이어그램 + 에러 복구 전략"
- `cheatsheets/api-compare.md` — tool use 섹션 추가

## 📌 핵심 키워드

- tool_use / function_call / function_declaration
- tool_result, tool_use_id
- stop_reason: `tool_use` / `end_turn` / `max_tokens` / `stop_sequence`
- `tool_choice`: auto / any / required / specific
- Parallel tool call, fan-out / gather
- Agent loop, ReAct, reasoning-action-observation
- Safety: recursion cap, token budget, wall-clock timeout, sandboxing
- Anthropic extended thinking with tools
- OpenAI built-in tools (web_search, file_search, code_interpreter)
- MCP (내일모레 Day 11)

## ⚠️ 프로덕션 경고

- **Tool description에 내부 URL / secret 금지** — 유저에게 흘러갈 수 있음.
- **Tool exception stacktrace를 LLM에 그대로 넘기지 마** — 정보 누출. 요약된 에러 코드 + 메시지만.
- **File I/O tool은 항상 샌드박스** — symlink / `..` / `/` 절대경로 전부 막기.
- **Shell/exec tool은 기본 금지**. 필요하면 Docker/firejail 격리 + allowlist.
- **Rate limit 외부 API** — agent가 같은 URL 루프로 때리면 금방 밴.

## 🎁 내일(Day 6) 미리보기
Embedding + Vector DB. Tool use의 지식 tool 역할을 RAG가 대체하는 구도. Qdrant 띄우고, embedding의 chunk/overlap 튜닝이 품질의 50%라는 것을 체감.
