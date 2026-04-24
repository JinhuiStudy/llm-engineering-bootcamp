# 리스크 / 복구 플레이북

뒤처지는 건 정상. 10시간 × 14일은 현실적으로 몇 번은 삐끗한다. **삐끗해도 완주하는 규칙.**

## 🚨 트리거 → 대응

### Trigger 1: 하루 8h도 못 채우는 게 이틀 연속
**원인**: 피로 누적, 특정 개념 막힘, 번아웃 초입
**대응**:
1. 그날 필수 체크리스트만 완료 (stretch 전부 버림)
2. 잠 8h+ 보장
3. 다음 날 오전 블록은 "읽기"만 — 실습 오후로 밀기
4. 주제가 계속 막히면 Day 순서를 재편 (아래 "선택적 건너뛰기")

### Trigger 2: 특정 Day 실습이 안 끝남 (예: Day 8 고급 RAG)
**원인**: 프로젝트 범위가 너무 넓음
**대응**:
1. Must-have (필수 체크리스트)만 남기고 나머지 **내일로 ship**
2. `daily-log.md`에 "미완료: X, Y. Day N+1에 이어서" 명시
3. 다음 Day 시작 시 20분 "어제 이월" 블록 삽입
4. 3일 연속 미완이면 Day 순서 대폭 압축 (아래 "C 모드")

### Trigger 3: API 크레딧 고갈
**원인**: 실험 횟수 많음, 큰 모델 남발
**대응**:
1. Flash/Haiku/4o-mini 등 **작은 모델로 일괄 전환**
2. `shared/ai_study/tokens.py`로 비용 사전 추정 습관
3. Prompt caching 적극 사용 (Day 12 내용 앞당기기)
4. 마지막 수단: Ollama로 오늘의 LLM 호출 전부 로컬화

### Trigger 4: Docker/Qdrant/Langfuse 안 뜸
**원인**: 포트 충돌, 볼륨 권한, 이미지 pull 실패
**대응**:
1. `docker ps -a` + `docker logs <name>` 로그 그대로 붙여 넣고 검색
2. 볼륨 초기화 (`rm -rf infra/<x>/volumes`)
3. 버전 고정 (latest → 명시적 버전)
4. **우회**: Qdrant 대신 Chroma in-memory / Langfuse 대신 Phoenix
5. 최후: 해당 Day의 인프라 실습을 cloud 버전 (Qdrant Cloud, Langfuse Cloud 무료 tier)로 전환

### Trigger 5: 키 쓰였는데 응답 품질이 이상함
**원인**: 모델명 오타, 무료 tier 제한, rate-limit로 잘림
**대응**:
1. 모델명 **정확히 확인** (deprecate 되면 응답이 쓰레기)
2. `r.usage`로 토큰 찍어서 잘림 여부 (completion_tokens == max_tokens 근접 시 잘림)
3. `max_tokens` 올리거나 요청 쪼개기

### Trigger 6: 집중력 완전 붕괴 (오후에 멍)
**원인**: 일시적 과부하
**대응**:
1. **30분 산책** 강제
2. 커피/당 X (리바운드)
3. 물 500ml
4. 복귀해서 제일 쉬운 체크리스트 1개부터 (entry barrier ↓)
5. 그래도 안 되면 오후 블록 조기 마감 + 내일 아침 먼저

---

## 📉 전체 일정 뒤처짐 → 모드 축소

### A 모드 (정상): 14일 전부 + stretch
원래 계획.

### B 모드 (1-2일 뒤처짐): 14일 / stretch 버림
- 필수 체크리스트만
- Day 순서 유지
- stretch 아이디어 전부 14+ 트랙으로 이동

### C 모드 (3일 이상): 압축 로드맵
다음 순서로 Day 병합:
- Day 1 + Day 2 → 1일 (LLM 기초 + API 최소)
- Day 3 유지 (Prompt)
- Day 4 + Day 5 → 1일 (Structured + Tool 기초만)
- Day 6 + Day 7 → 1일 (Embedding + 기본 RAG 합치기)
- Day 8 + Day 9 → 1일 (Advanced RAG + Eval 최소)
- Day 10 유지 (Agent)
- Day 11 축소 (MCP는 개념 + 간단 server 1개만)
- Day 12 축소 (Langfuse만, Phoenix 스킵)
- Day 13 축소 (Ollama만, RunPod은 다음주)
- Day 14 포트폴리오 (기능 축소)

→ 실질 10일로 압축 가능.

### D 모드 (완전 붕괴): 코어만
**가장 중요한 것만** — LLM 엔지니어 최소 역량:
1. 3-provider chat wrapper (Day 2)
2. Structured output (Day 4)
3. Tool use (Day 5)
4. 기본 RAG 하나 (Day 7 수준)
5. Eval 최소 1개 돌려보기 (Day 9)
6. Langfuse trace 1번 찍기 (Day 12)
→ 실제로 7-8일이면 가능.

---

## 🧘 회복 루틴

### 번아웃 사전 경고
- 웃음 사라짐
- 코드 보기 싫음
- 사소한 에러에 화
- 오전 시작이 10시 넘어감

→ 즉시 **하루 전체 쉬기**. 14일이 15일이 되는 게 뒤처짐이 아니라 붕괴보다 낫다.

### 회복일 사용법
- 공부 자료 열지 않기
- 자연광
- 긴 운동 1회
- 잠 충분히
- 회복일 저녁에 `daily-log.md`에 "회복일: 이유 + 내일 재개 플랜"만 짧게

### 컨디션 자가진단 (매일 밤)
- 수면 시간 (6h 이하면 경고)
- 오늘 한 시간 대비 몰입률 (1-5)
- 내일 시작 에너지 (1-5)
→ 3 이하 연속 2일 = 속도 줄이기

---

## 🛑 Don'ts

- ❌ 오늘 못 끝낸 걸 내일 자정 넘어 마무리
- ❌ "내일부터 더 열심히"로 오늘 회피
- ❌ 특정 공식 문서를 원문으로 읽기 싫다고 한글 블로그 반나절
- ❌ Day 10 agent가 안 돌아간다고 Day 9 eval을 건너뛰기 (오히려 eval이 답 지시해줌)
- ❌ 포트폴리오에 미운영 기능 끼워넣기 ("될지도 모르니" 배제)

## ✅ Do's

- ✔ 매일 커밋 (작아도)
- ✔ 에러 메시지 풀 카피해서 노트로
- ✔ "내일 나"에게 3줄 메모 남기기
- ✔ 완료 기준 사전 정의
- ✔ 막히면 Claude/문서에 질문 — 자존심 쓰지 말 것
