# Day 4 — Structured Output Extractor (다중 도메인)

> **연결**: [`curriculum/week1-day04-structured-output.md`](../../curriculum/week1-day04-structured-output.md)
> **의존성**: Day 1-2 providers/
> **다음**: Day 5 tool use도 같은 JSON Schema 계보 — `tool.input_schema = Pydantic.model_json_schema()`

## 🎯 이 프로젝트로

1. **3도메인** (resume/invoice/meeting) × **3 provider** (OpenAI/Anthropic/Gemini) × strict 성공률 실측
2. Pydantic v2 `@field_validator` + `@model_validator(mode='after')` 실전 사용
3. **Self-healing** — ValidationError → 에러를 LLM에 피드백 → 재시도 → 성공률 측정
4. Discriminated Union / Nested / Optional / Literal enum 등 고급 스키마 3사에 다 먹이기
5. Instructor / Outlines / 직접 짜기 3가지 경험 후 선택

## 📁 디렉토리

```
day03-structured-extractor/
├── pyproject.toml
├── schemas/
│   ├── __init__.py
│   ├── common.py              # shared types: Money, DateRange, Address
│   ├── resume.py              # Person, Experience, Skill, ResumeSummary
│   ├── invoice.py             # LineItem, Invoice (total == sum(items) validator)
│   ├── meeting.py             # discriminated union: ActionItem | Decision | Question
│   └── medical.py             # Stretch: Prescription (EU/US format union)
├── extract.py                 # 엔트리: --schema/--provider/--method (strict|tooluse|instructor)
├── methods/
│   ├── strict_native.py       # OpenAI response_format / Anthropic native / Gemini response_schema
│   ├── tool_use_trick.py      # Anthropic tool_use로 스키마 강제
│   ├── instructor_way.py      # instructor 라이브러리
│   └── outlines_local.py      # Ollama + Outlines grammar-constrained (Day 13 prerequisite)
├── self_heal.py               # ValidationError loop (max 3 retry)
├── ingest/
│   ├── pypdf_loader.py
│   ├── pdfplumber_loader.py   # 표 있는 PDF
│   └── vision_loader.py       # 스캔/이미지 PDF → GPT-4o/Claude Vision
├── samples/
│   ├── resume/                # 5개
│   ├── invoice/               # 5개
│   └── meeting/               # 5개
├── outputs/                   # 추출 JSON (gitignore)
├── eval/
│   ├── golden.json            # 20건 수기
│   └── score.py               # field-level exact match + fuzzy (rapidfuzz)
└── README.md
```

## 🚀 시작

```bash
cd projects/day03-structured-extractor
uv sync
uv add pydantic instructor pypdf pdfplumber unstructured rapidfuzz
# 선택 (stretch)
uv add outlines
```

## ✅ 필수 기능

### 스키마
- [ ] `resume.py` — `ResumeSummary(name, email: EmailStr, years_of_experience: int = Field(ge=0, le=60), skills: list[Skill], experiences: list[Experience])` + Skill은 `Literal["beginner","intermediate","expert"]`
- [ ] `invoice.py` — `@model_validator(mode='after')`에서 `total == sum(line.price * line.qty)` 검증
- [ ] `meeting.py` — `Annotated[Union[ActionItem, Decision, Question], Field(discriminator='type')]`
- [ ] `Field(description=...)` **모든 필드 필수** — description 없는 필드는 정확도 -20%

### 3 method × 3 provider
- [ ] `strict_native.py`:
  - OpenAI: `client.beta.chat.completions.parse(response_format=Model)` → `.parsed`
  - Anthropic: native `response_format={"type":"json_schema", ...}`
  - Gemini: `config={"response_mime_type": "application/json", "response_schema": Model}` → `response.parsed`
- [ ] `tool_use_trick.py`: Anthropic tool_use로 `input_schema=Model.model_json_schema()` 강제
- [ ] `instructor_way.py`: `instructor.from_openai(client, mode=Mode.TOOLS)` + `response_model=Model`

### Self-healing
- [ ] `self_heal.py` — `try: Model.model_validate_json(...)` 실패 시 `ValidationError.errors()`를 LLM에 피드백:
  ```
  Your previous output failed validation with errors:
  - field 'email': not a valid email
  - field 'skills[0].level': not in enum
  Please correct and output valid JSON again.
  ```
- [ ] 최대 3회 재시도. Attempt별 토큰 로그

### Eval
- [ ] `golden.json` — 20건 (each: pdf path + expected JSON)
- [ ] `score.py` — **field-level F1**:
  - exact match (name, email, enum)
  - fuzzy (company names, titles) — rapidfuzz `ratio > 85`
  - numeric (years_of_experience) — ±1 tolerance
- [ ] 출력: `{method} × {provider}` 표

## 📊 수치 기준

| 메트릭 | 기준 |
|---|---|
| strict_native 성공률 (JSON 파싱) | 100% |
| strict_native 스키마 준수율 | ≥ 99% (OpenAI strict=true 기준) |
| field-level F1 (OpenAI 4o) | ≥ 0.85 |
| Self-heal 첫 시도 실패율 | ≤ 10% |
| Self-heal 3회 이내 복구율 | ≥ 98% |

## 🧨 실전 함정

1. **`Optional[X]` OpenAI strict에서 터짐** → `X | None` + `json_schema_extra={"nullable": True}` 또는 required로 강제하고 빈 문자열 허용
2. **`$ref` 자동 생성이 strict 호환 안 됨** → `model_json_schema(mode='serialization')` 후 `$defs` flatten 유틸 필요 (or instructor에 맡기기)
3. **Discriminated Union** — OpenAI strict는 지원, Gemini는 덜 완성. 3사 전부 테스트
4. **금액(Decimal) → JSON → float 오차** → `Field(json_schema_extra={"type":"string"})` + `@field_validator`에서 파싱
5. **대량 리스트(list[Item] 100+)** → max_tokens 초과해서 잘림. 청크 호출 + merge
6. **EmailStr vs str(pattern)** — Pydantic EmailStr 있으면 사용, schema 내보낼 때 `format: "email"`
7. **description 없는 필드** → 정확도 급락. 모든 필드 `Field(description="...")`

## 🎁 Stretch

- 🧪 **Vision fallback** — 텍스트 파싱 실패한 PDF를 이미지로 렌더 → Claude Vision으로 읽기
- 🧪 **Outlines + Ollama** — 로컬 Qwen3-8B에 regex/CFG 제약으로 100% JSON 보장
- 🧪 **Schema caching** — system에 schema 넣고 Anthropic `cache_control`로 캐시 (비용 90% 절감)
- 🧪 **Partial streaming** — `instructor.Partial[Model]`로 필드 완성되는 대로 UI 업데이트

## 🔗 다음에 쓰이는 곳

- Day 5: tool_use schema가 곧 Pydantic schema
- Day 7 RAG: Answer(text, citations: list[Citation], confidence: float) 응답 스키마
- Day 14 portfolio: `app/schemas/`의 기반
