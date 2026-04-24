# Day 4 — Structured Output Extractor

커리큘럼: `curriculum/week1-day04-structured-output.md`

PDF/이력서에서 구조화된 정보 추출. Pydantic + LLM.

## 체크리스트
- [ ] `schemas.py` — Pydantic v2 모델 (ResumeSummary, Experience, Skill, Person)
- [ ] EmailStr, Literal enum, Nested 모델 포함
- [ ] `extract.py` — PDF → text → LLM (JSON schema) → Pydantic
- [ ] Retry on ValidationError (self-healing, 최대 2회)
- [ ] OpenAI + Anthropic 둘 다
- [ ] `samples/` 이력서 PDF 3개
- [ ] `outputs/` 결과 JSON

## Pydantic 예시
```python
from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class Skill(BaseModel):
    name: str
    level: Literal["beginner", "intermediate", "expert"]

class ResumeSummary(BaseModel):
    name: str
    email: EmailStr
    years_of_experience: int = Field(ge=0, le=60)
    skills: list[Skill]
```
