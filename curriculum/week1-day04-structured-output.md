# Day 4 — Structured Output + Pydantic (하드코어)

> **난이도**: ★★★ (원래 ★★에서 상향)
> **총량**: 읽기 4h + 실습 5h + 정리 1h = 10h.
> **철학**: 프로덕션 LLM 앱의 80%는 **"구조화된 입출력을 100% 보장"**으로 결정된다. 오늘이 그 기초.

## 🎯 오늘 끝나면

1. JSON Schema / Pydantic v2 / 3사 SDK를 유기적으로 연결 — "Pydantic 모델 하나로 3사에 동일한 구조화 출력"을 강제할 수 있음
2. **Strict vs non-strict mode** 차이 실증 (strict=false는 거의 의미 없음)
3. Self-healing 파이프라인: Pydantic validation 실패 → 에러를 LLM에 피드백 → 재시도 → 성공
4. **복잡 스키마** (nested / union / discriminated union / Literal enum / conditional required)를 3사에서 다 먹이는지 테스트
5. `instructor` / `langchain` / `outlines` 세 가지 생태계의 차이 설명

## 📚 자료

### 🔥 필수 (4h)

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 1h | [OpenAI — Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs) | `strict: true` — JSON Schema 준수 **100% 보장** (GPT-4o-2024-08-06 이후). 단, schema 제약: `additionalProperties: false`, 모든 필드가 required(Optional은 union with null), `$ref` 제한 등. |
| 1h | [Anthropic — Structured Outputs](https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs) | **2026년 초 GA 기능**. `response_format={"type": "json_schema", ...}` 또는 legacy tool_use 트릭. 두 방법 비교. |
| 30m | [Gemini — Structured Output](https://ai.google.dev/gemini-api/docs/structured-output) | `response_schema=PydanticModel`, `response_mime_type="application/json"`. Pydantic 객체 그대로 받기 (`response.parsed`). |
| 1.5h | [Pydantic v2 docs — Models / Validators / Serialization](https://docs.pydantic.dev/latest/) | v2 기준. `BaseModel`, `Field`, `@field_validator`, `@model_validator`, `model_validate_json`, `model_dump_json`, `TypeAdapter`, `RootModel`. **v1 코드는 다 버리기**. |

### 🔥 강력 권장

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 1h | [Instructor docs](https://python.useinstructor.com/) | Pydantic + OpenAI/Anthropic/Gemini + retry + streaming + partial output을 묶은 **사실상 표준 라이브러리**. 소스코드 가볍게 읽어볼 가치. |
| 30m | [Instructor — Cookbook examples](https://python.useinstructor.com/examples/) | 실전 예제 20+ (분류/추출/checking/citations). 오늘 과제 설계 참조. |
| 30m | [Outlines docs](https://dottxt-ai.github.io/outlines/) | **Regex/CFG 레벨로** 출력 강제. Local LLM과 결합(Day 13 연결). grammar-constrained decoding 원리. |

### 🎓 선택

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 30m | [OpenAI Cookbook — Structured outputs](https://cookbook.openai.com/examples/structured_outputs_intro) | introspection / function result / classification 3 예제. |
| 20m | [Pydantic AI — Structured Responses](https://ai.pydantic.dev/results/) | Pydantic팀의 agent 프레임워크. 나중 Day 10에 재등장. |
| — | [JSON Schema Spec — 2020-12](https://json-schema.org/draft/2020-12/schema) | 레퍼런스. 막힐 때만 꺼내 봄. |

## 🔬 실습 (5h)

### 프로젝트: 다중 도메인 정보 추출기

위치: `projects/day03-structured-extractor/`

```
day03-structured-extractor/
├── schemas/
│   ├── resume.py           # 이력서: Person, Experience, Skill, ResumeSummary
│   ├── invoice.py          # 인보이스: LineItem, Invoice (금액 합계 validator)
│   ├── meeting.py          # 회의록 → action items (discriminated union으로 task 종류 분기)
│   └── medical.py          # (Stretch) 약 처방전 → 약물 목록 + 용량 (EU format vs US format union)
├── extract.py              # 엔트리. --schema resume|invoice|meeting --provider openai|anthropic|gemini
├── self_heal.py            # validation error → feedback → retry
├── samples/                # 5개씩 샘플 PDF/이미지
├── outputs/                # 추출된 JSON
├── eval/
│   ├── golden.json         # 수기 작성 ground truth 20개
│   └── score.py            # field-level exact match + fuzzy
└── README.md
```

### 🔥 필수 기능

1. **Pydantic v2 모델** — 각 도메인에 최소:
   - `Field(description=...)` — LLM이 읽음. **description 안 쓴 필드는 정확도 -20%**.
   - `Literal[...]` enum
   - `@field_validator`로 email/phone/금액 형식 검증
   - `@model_validator(mode='after')`로 cross-field 검증 (예: invoice total == sum(line_items))
   - Nested 모델 (Experience 안에 Achievement 리스트)
2. **3사 adapter** — 하나의 Pydantic 모델 → OpenAI/Anthropic/Gemini에 각각 맞게 변환 후 호출
3. **Self-healing** — ValidationError 발생 시 에러 메시지를 user message로 다시 붙여 retry (최대 3회). Attempt별 토큰 로그.
4. **strict 성공률 측정** — `strict=true` vs `strict=false` 각 20회씩 돌려서 "JSON 파싱 성공률", "스키마 완전 준수율", "의미상 정답률" 3단계로 분리
5. **Streaming 추출** — Instructor `Partial[Model]`로 필드가 완성되는 대로 점진 출력 (UX 체감)
6. **Eval harness** — `eval/golden.json` 20건 대비 field-level F1 score 계산

### 🔥 Stretch

- 🧪 **PDF 파싱**: `pypdf` (순한 PDF) → `pdfplumber` (표 있음) → `unstructured` (이미지/스캔) 단계적 선택.
- 🧪 **Vision fallback**: 텍스트 파싱 실패 시 페이지를 PNG로 렌더 → Claude/GPT-4o Vision으로 직접 읽기.
- 🧪 **Discriminated union**: `Union[MeetingActionItem, MeetingDecision, MeetingQuestion]` — `type` 필드로 분기. 3사 다 제대로 먹이는지 테스트.
- 🧪 **Schema caching** — 매 호출마다 schema 전송하지 말고 Anthropic `cache_control`로 캐시.
- 🧪 **Outlines 실험** — Ollama 로컬 모델에 regex/CFG 제약을 걸어 JSON을 **문법 레벨에서** 강제. 결과 품질 비교.

## ⚔️ 실전 함정 (꼭 만나게 될 것)

### 1. `Optional[X]` 처리
- Pydantic: `name: Optional[str] = None`
- OpenAI strict mode: "모든 필드 required" → `name: Union[str, None]` + `null` 명시적 허용하거나, `additionalProperties: false` + enum으로 우회
- 해결: **`Optional`을 쓰지 말고 `X | None = None` + `json_schema_extra={"nullable": True}`** or 그냥 required로 강제하고 LLM이 빈 문자열 내게

### 2. `$ref` 제약
- OpenAI strict는 `$ref` 제한적 지원. Pydantic은 nested 모델을 자동으로 `$ref`로 풀음 → strict 호환 위해 `model_json_schema(mode='serialization')` 후 inline
- 해결: Instructor가 내부에서 해결. 직접 짜면 `$defs` flatten 유틸 필요.

### 3. Discriminated Union
- `tagged_union`이 OpenAI에 어떻게 먹히는지 실측. Anthropic tool_use 트릭이 더 깔끔할 수 있음.

### 4. Number precision
- Pydantic `float` → JSON → 부동소수점 오차. 금액은 `Decimal` + `Field(json_schema_extra={"type": "string"})` 고려.

### 5. 대량 리스트 (>100 항목)
- `list[Item]` 수백 개면 max_tokens 초과 → 잘림 → JSON 파싱 실패. **청크 단위로 호출 후 merge** 패턴. (Day 11 Batch API로도 해결 가능)

## ✅ 체크리스트

- [ ] OpenAI strict mode 성공 (성공률 100%는 schema 제약 만족해야)
- [ ] Anthropic native structured output (최신 SDK) 동작
- [ ] Anthropic tool_use 트릭 방식도 구현해두고 차이 이해
- [ ] Gemini `response_schema=PydanticModel`로 `response.parsed` 받음
- [ ] Pydantic validator로 email/금액/날짜 포맷 잡음
- [ ] Self-healing 1회 이상 작동 (validation error → retry → 성공 로그)
- [ ] 20건 golden 대비 field-level F1 계산
- [ ] strict vs non-strict 성공률 차이 수치화 (예: 100% vs 85%)
- [ ] `notes/concepts.md` — "왜 tool_use로도 structured output이 되는가" 정리

## 🧨 자주 틀리는 개념

1. **"JSON mode와 Structured Outputs는 같다"** — 아니다. OpenAI JSON mode는 **"JSON이긴 함"**만 보장. Structured Outputs(`type: json_schema`, `strict: true`)는 **스키마까지 준수** 보장.
2. **"Pydantic 있으면 LLM 신뢰해도 됨"** — validation은 "형식"만 잡음. **사실(factuality)은 별개**. 이력서에서 "경력 5년"이라 실제로 적혀있는데 LLM이 "10년"이라 뽑아도 Pydantic은 통과.
3. **"strict=true면 LLM이 느려진다"** — 첫 호출엔 schema compile로 수초 지연, 이후 캐시. 정상 latency는 non-strict와 비슷.
4. **"Anthropic structured output = tool_use trick"** — **2026년 초부터는 native `response_format` 존재**. 신규 코드는 native, legacy만 tool_use.
5. **"LLM이 enum 바깥 값을 뱉지 않음"** — strict=true에서만 보장. non-strict는 가끔 벗어남.
6. **"description 없어도 이름만 좋으면 됨"** — 필드명 + description 둘 다 먹여야 정확도 최고.

## 🧪 산출물

- `projects/day03-structured-extractor/` 완성 (3개 도메인)
- `eval/golden.json` + `score.py` — 정답 대비 F1
- `results/` — strict vs non-strict 비교표, 3-provider 성공률표
- `notes/concepts.md` — "structured output 설계 원칙 5개" 본인 언어로

## 📌 핵심 키워드

- JSON Schema (Draft 2020-12), `$ref`, `$defs`, `additionalProperties`, `required`
- Pydantic v2: `BaseModel`, `Field`, `@field_validator`, `@model_validator`, `model_validate_json`, `model_dump_json`, `RootModel`, `TypeAdapter`, `discriminator`
- OpenAI: `response_format={"type": "json_schema", "json_schema": {...}, "strict": true}`, `client.beta.chat.completions.parse` 자동
- Anthropic: native `response_format` (신) / tool_use-as-schema (legacy), `input_schema`
- Gemini: `response_schema=PydanticModel`, `response_mime_type`, `response.parsed`
- Instructor: `client = instructor.from_openai(...)`, `response_model=T`, `Partial[T]`, `Iterable[T]`, `Maybe[T]`
- Outlines: grammar-constrained decoding, regex/CFG 제약
- Self-healing / auto-retry / validation feedback

## 🎁 내일(Day 5) 미리보기
Function Calling / Tool Use. 오늘 만든 Pydantic schema가 tool definition과 같은 뿌리(JSON Schema)임을 실감. Tool agent loop 구현.
