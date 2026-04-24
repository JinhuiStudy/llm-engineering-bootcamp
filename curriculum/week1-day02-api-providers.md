# Day 2 — 3대 Provider API 실전

## 목표
- OpenAI / Anthropic / Gemini API를 각자 직접 호출 (SDK + raw HTTP 양쪽)
- 3사 메시지 포맷, system prompt 위치, 스트리밍 방식 차이 이해
- 같은 기능을 3개 provider로 구현할 수 있는 얇은 래퍼 작성

## 자료

| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [OpenAI API Reference](https://platform.openai.com/docs/api-reference) | 1h |
| 필수 | [Anthropic API — build with claude](https://www.anthropic.com/learn/build-with-claude) | 1h |
| 필수 | [Gemini API Quickstart](https://ai.google.dev/gemini-api/docs/quickstart) | 0.5h |
| 필수 | [Anthropic courses — anthropic_api_fundamentals](https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals) (notebook 따라치기) | 2h |
| 선택 | [OpenAI Cookbook — intro 예제 3개](https://cookbook.openai.com/) | 1h |
| 선택 | [Gemini — text generation](https://ai.google.dev/gemini-api/docs/text-generation) | 0.5h |

## 실습 (4–5h)

### 프로젝트: 3-Provider CLI 챗봇
위치: `projects/day01-chatbot-cli/` (Day 1에서 이어서)

```
day01-chatbot-cli/
├── .env                 # OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY
├── providers/
│   ├── base.py          # Provider 인터페이스 (chat(messages, stream) -> str|Iterator)
│   ├── openai_client.py
│   ├── anthropic_client.py
│   └── gemini_client.py
├── chat.py              # argparse로 --provider openai|anthropic|gemini 스위치
└── README.md
```

### 필수 기능
1. 시스템 프롬프트 지원 (3사 방식 다름 — Anthropic은 top-level `system`, OpenAI/Gemini는 messages 안)
2. Streaming 모드 (`--stream`)
3. 대화 히스토리 유지 (멀티턴)
4. 토큰 사용량 출력 (input/output/total)
5. 에러 (rate limit / auth) 핸들링

### Stretch (여력 되면)
- 동일 프롬프트를 3사에 동시 호출해서 응답 비교하는 `--compare` 모드

## 체크리스트

- [ ] 3사 API 전부 성공 호출
- [ ] Streaming 동작 확인 (터미널에 토큰 단위로 나옴)
- [ ] `cheatsheets/api-compare.md` 작성 (3사 차이점 표)
- [ ] Rate limit error 일부러 유발해보고 어떤 에러 객체가 오는지 확인
- [ ] system/user/assistant role 구조를 3사 모두 설명 가능

## 핵심 키워드 (notes/keywords.md에 추가)
- role (system/user/assistant), completion vs chat, streaming, SSE, max_tokens, stop sequences
- Anthropic: `messages` + top-level `system`, `stop_reason`
- OpenAI: `response_format`, Responses API vs Chat Completions
- Gemini: `generateContent`, `Content/Part`, `safetySettings`
