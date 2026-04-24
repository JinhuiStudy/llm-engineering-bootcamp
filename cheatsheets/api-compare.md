# API 비교 치트시트 — OpenAI / Anthropic / Gemini

## 한눈에

| 항목 | OpenAI | Anthropic | Gemini |
|---|---|---|---|
| SDK (Python) | `openai` | `anthropic` | `google-genai` |
| Chat entry | `client.chat.completions.create` or `client.responses.create` | `client.messages.create` | `client.models.generate_content` |
| System prompt | messages[0].role="system" | `system=` top-level | `system_instruction=` |
| Role 이름 | system/user/assistant | user/assistant (system 별도) | user/model |
| Streaming | `stream=True` | `stream=True` or `.stream()` | `stream=True` |
| Tools 키 | `tools=[...]` | `tools=[...]` + `tool_use`/`tool_result` 블록 | `tools=[types.Tool(...)]` |
| Structured output | `response_format={"type":"json_schema", ...}` (strict) | native SO or tool_use trick | `response_schema=Pydantic` |
| Prefill 지원 | ❌ | ✅ (assistant messages 이어쓰기) | ❌ |
| XML 선호도 | 중립 | 강함 | 중립 |
| Prompt caching | implicit (prefix auto) | explicit `cache_control` | explicit `cachedContents` |
| Batch API | ✅ | ✅ (message batches) | ✅ |
| Vision | ✅ | ✅ | ✅ (최강) |
| Audio in/out | ✅ (realtime/audio-preview) | 부분 | ✅ (Live API) |
| 최대 context | 400k (GPT 계열) | 200k (standard), 1M (beta) | 1M+ (표준) |

## 호출 뼈대 비교 (동일 "hello"를 3사로)

### OpenAI
```python
from openai import OpenAI
client = OpenAI()
r = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Say hi"},
    ],
)
print(r.choices[0].message.content)
print(r.usage)  # prompt_tokens, completion_tokens
```

### Anthropic
```python
import anthropic
client = anthropic.Anthropic()
r = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=512,
    system="You are helpful.",
    messages=[{"role": "user", "content": "Say hi"}],
)
print(r.content[0].text)
print(r.usage)  # input_tokens, output_tokens, cache_*
```

### Gemini
```python
from google import genai
client = genai.Client()
r = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hi",
    config={"system_instruction": "You are helpful."},
)
print(r.text)
print(r.usage_metadata)
```

## Tool/Function 비교

### OpenAI
```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "...",
        "parameters": {"type": "object", "properties": {...}, "required": [...]},
    }
}]
# 응답: message.tool_calls[*].function.{name, arguments}
```

### Anthropic
```python
tools = [{
    "name": "get_weather",
    "description": "...",
    "input_schema": {"type": "object", "properties": {...}, "required": [...]},
}]
# 응답: content 배열에 {"type": "tool_use", "name": ..., "input": ..., "id": ...}
# 다음 턴: {"role": "user", "content": [{"type": "tool_result", "tool_use_id": ..., "content": ...}]}
```

### Gemini
```python
from google.genai import types
tool = types.Tool(function_declarations=[
    types.FunctionDeclaration(name="get_weather", description="...", parameters={...})
])
# 응답: response.function_calls[*].{name, args}
# Automatic function calling도 지원 (callable 바로 전달)
```

## Structured Output 비교

### OpenAI (strict JSON Schema)
```python
from pydantic import BaseModel
class Person(BaseModel):
    name: str; age: int

r = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[...],
    response_format=Person,
)
# r.choices[0].message.parsed → Person 인스턴스
```

### Anthropic (tool_use 트릭 or native)
```python
# 방법 1: tool_use로 강제
tools = [{"name": "record_person", "input_schema": Person.model_json_schema(), ...}]
# 방법 2: strict=True tool use (최신 SDK)
```

### Gemini (response_schema)
```python
r = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="...",
    config={"response_mime_type": "application/json", "response_schema": Person},
)
# r.parsed → Person
```

## 비용 / 성능 감각 (표준 모델 기준, 2026년 초)

| 티어 | OpenAI | Anthropic | Gemini |
|---|---|---|---|
| Flagship | GPT-4o, o-series | Claude Opus 4.x | Gemini Pro |
| Workhorse | GPT-4o-mini | Claude Sonnet 4.x | Gemini Flash |
| Tiny | GPT-4o-nano? | Claude Haiku 4.x | Gemini Flash-Lite |

**엄지 룰**:
- 빠른 실험 / 비용: Haiku / 4o-mini / Flash
- 품질 중요: Sonnet / 4o / Pro
- 최상급 reasoning: Opus / o-series / Pro with thinking

## Rate Limit 대응 (공통)

```python
from tenacity import retry, stop_after_attempt, wait_random_exponential

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
def safe_call(...):
    return client.messages.create(...)
```

## Prompt Caching 감각

- **OpenAI**: prefix 재사용이면 자동 (implicit). 5분 후 만료. 할인 ~50%.
- **Anthropic**: `cache_control: {"type": "ephemeral"}` 명시. 5분 만료. 할인 ~90% 읽기, 쓰기 +25%.
- **Gemini**: `client.caches.create(...)` → cache name을 contents에 사용. TTL 지정 가능. 유료 context caching은 할인 상당.

**공통 전략**: 긴 system prompt / RAG context prefix에 캐시 걸기.

## 디버깅 체크리스트 (3사 공통)

- [ ] 모델명 정확한가 (deprecate된 모델 쓰지 마)
- [ ] API 키 환경변수에
- [ ] `max_tokens` 충분한가
- [ ] 응답 객체 구조 찍어봤나 (print로 일단 dump)
- [ ] `usage`로 토큰 확인
- [ ] 429 → retry / 401 → key 확인 / 400 → 요청 스키마
- [ ] Stream 처리 시 exception 핸들 꼼꼼히
