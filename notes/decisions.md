# Decision Log

큰 기술적 결정을 기록한다. 나중에 "왜 이렇게 짰지?" 물으면 여기 답이 있어야 한다.

## 포맷 (ADR 간소판)

```
## YYYY-MM-DD Day N — <결정 제목>
- Context: 어떤 상황/문제
- Options: 고려한 대안 2-3개
- Decision: 뭘 선택했고 왜
- Trade-offs: 이 결정의 약점 (있는 게 정상)
- Revisit: 어떤 조건이 되면 다시 볼 것
```

---

## 예시 (초기 기록)

### 2026-04-24 Day 0 — uv + shared 패키지 구조
- Context: 13개 day-프로젝트가 공통 dep(openai/anthropic/gemini/qdrant/...)을 중복 관리하면 버전 지옥.
- Options:
  1. 각 프로젝트 독립 venv
  2. 루트 단일 venv + 모든 코드 한 패키지
  3. `shared/` 공통 패키지 + 각 프로젝트는 얇게 참조
- Decision: (3) `shared/`.
- Trade-offs: import 경로 약간 장황. editable install 해야 함.
- Revisit: 프로젝트 간 dep 요구가 충돌하기 시작하면 (1)로 전환.

### 2026-04-24 Day 0 — Qdrant / Langfuse self-host
- Context: Cloud tier를 써도 되지만 관측성은 엔지니어링 실력에 크게 기여.
- Options:
  1. 전부 Cloud (Qdrant Cloud + Langfuse Cloud 무료 tier)
  2. 로컬 Docker
  3. 혼합
- Decision: 로컬 Docker. 내 Mac이 버티는 한.
- Trade-offs: RAM 부담. Langfuse는 컨테이너 5개라 무거움.
- Revisit: 발열/성능 문제 발생 시 Langfuse만 Cloud로.

---

<!-- 아래는 각자 추가할 것 -->

## YYYY-MM-DD Day N — <제목>
- Context:
- Options:
- Decision:
- Trade-offs:
- Revisit:
