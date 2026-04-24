# Decision Log (ADR 간소판)

큰 기술적 결정을 기록한다. "왜 이렇게 짰지?" 물으면 여기 답이 있어야 함.
14일 동안 **10-20개** 누적 목표.

## 📋 포맷

```markdown
## YYYY-MM-DD Day N — <결정 제목>
- **Context**: 어떤 상황/문제
- **Options**: 고려한 대안 2-3개 (각각의 장단)
- **Decision**: 뭘 선택했고 왜
- **Trade-offs**: 이 결정의 약점 (있는 게 정상)
- **Revisit**: 어떤 조건이 되면 다시 볼 것
```

## 🔖 작성 규칙

- 결정한 직후 적어라 — 하루 지나면 이유 잊어버림
- **선택 안 한 이유도 기록** — 6개월 뒤 똑같은 고민 반복 방지
- 거창한 결정만 말고 — "왜 Pydantic v2 쓰기로 했나" 수준도 OK
- 나중에 번복해도 삭제하지 말고 **새 엔트리로 덮어써라** — 역사 보존

---

# 📚 예시 엔트리 (초기)

## 2026-04-24 Day 0 — uv + shared 패키지 구조
- **Context**: 13개 day-프로젝트가 공통 dep (openai/anthropic/gemini/qdrant/...)을 중복 관리하면 버전 지옥
- **Options**:
  1. 각 프로젝트 독립 venv — **(+)** 격리 확실, **(-)** dep 13번 중복
  2. 루트 단일 venv + 모든 코드 한 패키지 — **(+)** 간단, **(-)** 모듈 경계 약함
  3. `shared/` 공통 패키지 + 각 프로젝트는 얇게 참조 — **(+)** 균형, **(-)** editable install 필요
- **Decision**: **(3) shared/ 공통 패키지**
- **Trade-offs**: import 경로 약간 장황. `uv pip install -e ./shared` editable. 프로젝트 간 dep 충돌 시 번거로움
- **Revisit**: 프로젝트 간 SDK 버전 충돌이 3회 이상 → (1)로 전환

## 2026-04-24 Day 0 — Qdrant / Langfuse self-host
- **Context**: Cloud tier를 써도 되지만 관측성·infra 감각이 목표에 포함
- **Options**:
  1. 전부 Cloud (Qdrant Cloud + Langfuse Cloud 무료 tier)
  2. 로컬 Docker
  3. 혼합 (Qdrant 로컬, Langfuse Cloud)
- **Decision**: **로컬 Docker** (2). Mac이 버티는 한
- **Trade-offs**: RAM 부담 (Langfuse는 3 컨테이너 — Postgres+CH+web). M2 16GB면 app 열어놓은 채 여유 없음
- **Revisit**: 발열/성능 문제 발생 시 Langfuse만 Cloud로 이관

---

# 📝 본인 예상 결정 포인트 (템플릿)

## Day 2 — 3-provider 추상화 레벨
- **Context**: 3사 API 호출부를 추상화 vs 그때그때 바꾸기
- **Options**:
  1. 얇은 Protocol (내 프로젝트용)
  2. LiteLLM 같은 기존 추상화
  3. 추상화 없이 분기문
- **Decision**: ?
- **Trade-offs**: ?
- **Revisit**: ?

## Day 4 — Structured Output method
- **Context**: strict native / tool_use trick / Instructor 중 선택
- **Options**:
  1. native (provider 별로 직접) — 성능 최적, 코드 장황
  2. tool_use trick — Anthropic legacy에서만
  3. Instructor 라이브러리 — 편하지만 abstraction 비용
- **Decision**: ?

## Day 6 — 임베딩 모델 선택
- **Context**: 한국어 중심 데이터에 OpenAI 3-small vs multilingual-e5-large vs Voyage
- **Options**: (비용, 품질, 로컬 여부 3축)
- **Decision**: ?

## Day 7 — RAG 프레임워크 기본 선택
- **Context**: `from_scratch` / LangChain LCEL / LlamaIndex 중 포트폴리오에 쓸 것
- **Options**: 각각의 유연성/가독성/커뮤니티 균형
- **Decision**: ?

## Day 8 — Contextual Retrieval 적용 여부
- **Context**: 49% 개선 claim 있지만 ingest 비용 (chunk당 Haiku 호출)
- **Options**: 항상 / 특정 collection만 / 안 씀
- **Decision**: ?

## Day 9 — Eval threshold 기준
- **Context**: CI gate의 faithfulness threshold
- **Options**: 0.80 / 0.85 / 0.90
- **Decision**: ? (본인 golden set 결과 기반)

## Day 10 — Agent framework
- **Context**: LangGraph vs Pydantic AI vs 직접 loop
- **Options**: 각각의 복잡도/유연성 트레이드
- **Decision**: ?

## Day 12 — Langfuse vs LangSmith vs Phoenix
- **Context**: observability 메인 선택
- **Options**: OSS self-host / SaaS / local Phoenix
- **Decision**: ?

## Day 13 — API vs Self-host 경계선
- **Context**: 월 $X에서 self-host 전환이 본인에게 의미 있는가
- **Options**: (본인 워크로드 / 데이터 정책에 따라)
- **Decision**: ?

## Day 14 — 포트폴리오 배포 전략
- **Context**: GitHub 공개 / 배포 플랫폼 (Fly.io / Modal / Local Docker)
- **Options**: 각각 비용/접근성/보안 트레이드
- **Decision**: ?

---

# 🧠 결정 퀄리티 체크

좋은 ADR:
- ✅ Trade-off가 솔직함 (모든 선택에 약점이 있음을 인정)
- ✅ 정량 근거 1개 이상 (수치/실측)
- ✅ Revisit 조건이 구체적 ("월 $X 넘으면" vs "나중에")
- ✅ 읽는 사람이 반대 의견 세울 수 있을 정도로 공정

나쁜 ADR:
- ❌ "최고의 도구라서" — 구체성 없음
- ❌ 대안 1개만 적음 — 실제로 고민 안 한 거
- ❌ Trade-off 없음 — 솔직하지 않음
- ❌ "팀이 익숙해서" — 본인 학습에선 핑계
