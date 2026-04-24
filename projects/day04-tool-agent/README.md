# Day 5 — 방어적 멀티툴 에이전트

> **연결**: [`curriculum/week1-day05-function-calling.md`](../../curriculum/week1-day05-function-calling.md)
> **의존성**: Day 1-2 providers/, Day 4 Pydantic schema 감각
> **다음**: Day 10 LangGraph agent의 `tool_caller` 노드가 이 모듈 재사용, Day 11 MCP server로 이식

## 🎯 이 프로젝트로

1. 3사 tool use의 **요청/응답 스키마 차이**를 손코드로 다룸
2. Tool agent loop의 **상태 기계** (LLM → tool_use → execute → tool_result → ...) 직접 짬
3. **Parallel tool use** 실제로 트리거 + asyncio.gather 실행
4. **Safety rails 4-layer**: recursion cap / token budget / wall-clock timeout / same-call-repeat detector
5. 악성 시나리오 (`../etc/passwd`, 무한 루프) 의도 재현 후 방어

## 📁 디렉토리

```
day04-tool-agent/
├── pyproject.toml
├── tools/
│   ├── __init__.py
│   ├── base.py                  # Tool Protocol: name / description / input_schema / execute
│   ├── weather.py               # Open-Meteo (무료, 키 없음) — 실제 HTTPx 호출
│   ├── calculator.py            # asteval 기반 safe expression 파서
│   ├── web_search.py            # Tavily or DuckDuckGo HTML scraping
│   ├── file_io.py               # read/list — SANDBOX_ROOT 아래만 + realpath 검사
│   └── python_exec.py           # Stretch: docker sibling container
├── agent/
│   ├── __init__.py
│   ├── loop.py                  # 상태 기계 메인
│   ├── schemas.py               # ToolCall, ToolResult, Message (Pydantic)
│   ├── safety.py                # Safety rail 4-layer
│   ├── adapters/
│   │   ├── openai.py            # Responses API tools 형식
│   │   ├── anthropic.py         # messages + tool_use blocks
│   │   └── gemini.py            # types.Tool(function_declarations=[...])
│   └── telemetry.py             # JSONL log → Day 12 Langfuse import 포맷
├── eval/
│   ├── scenarios.json           # 15 시나리오 (expected_tools 포함)
│   └── run.py
├── logs/                        # gitignore
├── cli.py                       # python cli.py --provider anthropic "서울 날씨"
└── README.md
```

## 🚀 시작

```bash
cd projects/day04-tool-agent
uv sync
uv add httpx asteval tavily-python   # tavily 없으면 DuckDuckGo
```

## ✅ 필수 기능

### Tool 구현
- [ ] `weather.py` — `get_weather(city: str, units: Literal["C","F"] = "C")` — Open-Meteo geocoding + forecast
- [ ] `calculator.py` — `asteval.Interpreter()` 로 수식 파싱 실행. Python 내장 동적 코드 실행 함수는 금지. 연산자/함수 whitelist
- [ ] `web_search.py` — Tavily (key 있으면) / DuckDuckGo HTML 파싱 (없으면). top_k 5 반환
- [ ] `file_io.py` — read_file / list_dir. `os.path.realpath(path).startswith(SANDBOX_ROOT)` 아니면 refuse
- [ ] 각 tool은 `Tool` Protocol 구현: `name`, `description` (긴 설명 + 언제 쓰는지), `input_schema: dict (JSON Schema)`, `async execute(args) -> ToolResult`

### Agent Loop
- [ ] `loop.py`:
  ```python
  async def run(question: str, tools: dict, provider: str, max_iter: int = 10):
      messages = [{"role": "user", "content": question}]
      for i in range(max_iter):
          response = await adapter.call(provider, messages, tools)
          if response.stop_reason == "end_turn":
              return response
          for call in response.tool_uses:
              safety.check(call, history)  # recursion/repeat/sandbox
              result = await execute_with_timeout(call, tools, timeout=30)
              messages.append(...)
      raise RuntimeError("max iterations")
  ```
- [ ] Parallel tool use — 한 턴에 여러 `tool_use` block → `asyncio.gather`
- [ ] 에러 catch → `{"type":"tool_result","tool_use_id":...,"content":"ERROR: ...","is_error":True}`로 LLM에 반환 (throw 안 함)

### Safety Rails
- [ ] `safety.py`:
  - `max_iterations` 10
  - `total_tokens > 50_000` → abort
  - `asyncio.timeout(60)` wall-clock
  - `same_call_detector`: 최근 3 call이 동일 (name + args hash) → abort
  - `sandbox_check`: file path → realpath → SANDBOX_ROOT prefix
  - `url_blocklist`: metadata URLs (169.254.169.254, localhost:22 등)

### tool_choice 모드
- [ ] `auto` (default) 실험
- [ ] `any` / `required` 강제
- [ ] `{"type": "tool", "name": "weather"}` specific 강제

### Eval
- [ ] `scenarios.json` (15개): 단순 RAG fallback / tool 1개 / tool 체인 / parallel / 악성 (`../etc/passwd`) / 무한루프 / tool 에러 복구
- [ ] `run.py` — 각 시나리오의 expected tool sequence vs actual. JSON으로 리포트

## 📊 수치 기준

| 메트릭 | 기준 |
|---|---|
| 15 시나리오 expected 일치율 | ≥ 80% |
| 악성 시나리오 차단율 | 100% |
| Tool 에러 발생 시 복구 (다른 tool/args 시도) | ≥ 70% |
| Parallel 트리거 유발 케이스 | ≥ 1 |
| 무한 루프 케이스에서 abort 발생까지 | ≤ 12 iter |

## 🧨 실전 함정

1. **Anthropic tool_result는 `content: str` 또는 list of content blocks** — dict 넘기면 400
2. **OpenAI Responses API의 tool 응답 경로** — `response.output[*]` 중 `type == "function_call"` 블록
3. **Gemini Automatic FC가 편하지만 blackbox** — manual 모드에서 `response.function_calls` 직접 파싱
4. **tool description 짧게 쓰면 안 부름** — `"""함수 X를 호출한다"""` 대신 "이 함수는 ... 언제 부르면 좋고 ... 예시: ..." 길게
5. **JSON arguments 파싱 에러** — strict mode 안 쓰면 LLM이 가끔 invalid JSON. `json.loads` try/except + retry
6. **symlink 공격** — `Path.resolve()` or `os.path.realpath`. `os.path.abspath`는 부족
7. **web_search 결과가 너무 길어 토큰 폭발** — 상위 N개 + 요약. 원문 저장은 별도 DB
8. **parallel_tool_use 강제 불가** — 프롬프트로 유도 ("A와 B를 동시에 조회하라")

## 🎁 Stretch

- 🧪 Extended thinking + tool — `thinking` block이 tool call 전에 와서 reasoning 투명화
- 🧪 Tool result LRU cache — 같은 args는 캐시
- 🧪 Streaming tool args — partial JSON 받으면서 progress 표시
- 🧪 `python_exec.py` — docker sibling container로 isolated Python
- 🧪 OpenAI built-in tools (web_search / file_search / code_interpreter) 호출해서 자체 구현과 비교

## 🔗 다음에 쓰이는 곳

- Day 10: LangGraph `tool_caller` 노드 = `agent/loop.py` 로직
- Day 11: 이 tool들을 FastMCP `@mcp.tool()`로 wrap
- Day 12: `telemetry.py` JSONL → Langfuse span
- Day 14: `app/tools/`
