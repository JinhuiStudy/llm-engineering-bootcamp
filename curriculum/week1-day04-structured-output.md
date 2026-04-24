# Day 4 — Structured Output + Pydantic

## 목표
- LLM 출력을 100% parseable JSON으로 강제하는 법 체화
- Pydantic 모델을 JSON Schema로 변환해 3사에 주입
- "타입 안전 LLM 호출" 패턴을 자기 프로젝트에 이식 가능

## 자료

| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [OpenAI — Structured Outputs guide](https://platform.openai.com/docs/guides/structured-outputs) | 1h |
| 필수 | [Anthropic — Structured Outputs](https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs) | 1h |
| 필수 | [Gemini — Structured Output](https://ai.google.dev/gemini-api/docs/structured-output) | 0.5h |
| 필수 | [Pydantic docs — 모델/Validator](https://docs.pydantic.dev/) (v2 기준) | 1.5h |
| 선택 | [Instructor 라이브러리 README](https://github.com/jxnl/instructor) — Pydantic + LLM 패턴의 사실상 표준 | 1h |

## 실습 (4h)

### 프로젝트: PDF/이력서 정보 추출기
위치: `projects/day03-structured-extractor/`

```
day03-structured-extractor/
├── schemas.py          # Pydantic models: Person, Experience, Skill, ResumeSummary
├── extract.py          # PDF → text → LLM → Pydantic 객체
├── samples/            # 이력서 샘플 PDF 2-3개
├── outputs/            # 추출된 JSON
└── README.md
```

### 요구사항
1. Pydantic `ResumeSummary` 모델 정의 (name, email, years_of_experience, skills: list[Skill], experiences: list[Experience])
2. `Skill`에 `level: Literal["beginner", "intermediate", "expert"]` 같은 enum 포함
3. Validator로 email 형식 체크 (v2 기준 `EmailStr`)
4. LLM이 JSON만 뱉도록 강제 — 파싱 실패 시 자동 재시도 (최대 2회)
5. OpenAI / Anthropic 둘 다 지원 (Gemini는 여력 되면)

### 고급 과제
- Nested 스키마 (Experience 안에 achievements: list[Achievement])
- `Optional` 필드를 LLM이 생략했을 때 default 값 주입
- Invalid JSON 반환됐을 때 Pydantic error를 LLM에 다시 던져서 고치게 시키기 (self-healing)

## 체크리스트

- [ ] OpenAI `response_format={"type": "json_schema", ...}` 동작 확인
- [ ] Anthropic tool_use 방식 JSON 추출 동작 확인 (Anthropic은 native structured outputs도 있음)
- [ ] Pydantic v2 모델 정의 (v1은 은퇴)
- [ ] Invalid JSON 케이스에서 자동 재시도 로직 확인
- [ ] `notes/concepts.md`에 "왜 tool_use로도 structured output이 되는지" 정리

## 핵심 키워드
- JSON Schema (draft-07, 2020-12), strict mode, $ref, additionalProperties
- Pydantic v2 (`BaseModel`, `Field`, `model_validate`, `model_dump_json`)
- OpenAI: `response_format`, Structured Outputs vs JSON mode
- Anthropic: native structured outputs, tool_use as structured output trick
- Instructor 라이브러리 (Pydantic + retry + streaming)
