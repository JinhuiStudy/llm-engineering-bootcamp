# Day 5 — Function Calling / Tool Use

## 목표
- Tool definition 작성법 3사 통일된 멘탈 모델 확보
- Tool call loop 패턴 직접 구현 (call → execute → feedback → next call)
- Parallel tool use와 forced tool choice 구분

## 자료

| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [Anthropic tool_use 코스 — 6 lessons](https://github.com/anthropics/courses/tree/master/tool_use) — **오늘의 메인** | 3h |
| 필수 | [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling) | 1h |
| 필수 | [Anthropic — tool use overview](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) | 0.5h |
| 선택 | [Anthropic — advanced tool use blog](https://www.anthropic.com/engineering/advanced-tool-use) | 0.5h |
| 선택 | [Gemini — Function calling](https://ai.google.dev/gemini-api/docs/function-calling) | 0.5h |
| 선택 | [OpenAI Responses API tool orchestration cookbook](https://developers.openai.com/cookbook/examples/responses_api/responses_api_tool_orchestration) | 1h |

## 실습 (4h)

### 프로젝트: 멀티툴 에이전트
위치: `projects/day04-tool-agent/`

```
day04-tool-agent/
├── tools/
│   ├── weather.py      # get_weather(city) — mock or Open-Meteo free API
│   ├── calculator.py   # safe eval
│   ├── web_search.py   # DuckDuckGo 또는 Tavily free tier
│   └── file_io.py      # read_file / list_dir (샌드박스 내에서만)
├── agent.py            # tool loop 구현
├── tools_schema.py     # 각 tool의 JSON schema
└── README.md
```

### 요구사항
1. 각 tool을 Python 함수 + JSON schema 로 등록
2. Agent loop: LLM 호출 → tool_use 있으면 실행 → tool_result 전달 → 반복 → final text 나오면 종료
3. 최대 반복 횟수 제한 (예: 10)
4. 실패한 tool call 시 에러 메시지를 tool_result로 되돌려주고 재시도
5. **Parallel tool use** 케이스 처리 (여러 tool을 한 번에 부르는 경우)
6. 로그에 모든 tool call을 남기기 (추후 Day 12 Langfuse에 연결)

### 테스트 쿼리
- "서울 날씨 알려주고 화씨로 변환해줘" → weather + calculator 연쇄
- "오늘 AI 뉴스 3개 요약" → web_search + LLM 요약
- "tools/ 디렉토리 파일 목록 보여줘" → file_io

### Stretch
- Tool 실행을 별도 subprocess로 격리
- Tool call 히스토리를 JSON 파일로 저장

## 체크리스트

- [ ] Anthropic tool_use 코스 6강 전부 notebook 실행 완료
- [ ] 3사 tool 정의 포맷 차이 설명 가능 (OpenAI `tools`, Anthropic `tools` + `tool_use/tool_result`, Gemini `function_declarations`)
- [ ] Parallel tool use 실제로 발생시켜봤음
- [ ] `tool_choice` 옵션으로 강제 호출해봤음 (`"any"`, `"tool"`, `{"type": "tool", "name": "..."}`)
- [ ] Agent가 무한루프에 빠지는 케이스 재현 + 방어

## 핵심 키워드
- tool_use / tool_result, function calling, parallel tool calls, tool_choice
- system prompt가 tool 선택에 미치는 영향
- ReAct 패턴 (reasoning + acting) — 내일 논문 요약 읽기
- Anthropic의 `stop_reason: "tool_use"` vs "end_turn"
- JSON Schema `required`, `enum`, `description`이 tool 선택 정확도에 미치는 영향
