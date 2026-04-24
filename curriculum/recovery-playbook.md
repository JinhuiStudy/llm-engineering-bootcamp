# 리스크 / 복구 플레이북 (v3 ULTRA 반영)

뒤처지는 건 정상. **12-14시간 × 14일**은 현실적으로 몇 번은 삐끗한다. **삐끗해도 완주하는 규칙.**

> v2(10h 기준)에서 v3(12-14h)로 밀도 증가 → 번아웃 위험 ↑. 이 문서 평소에도 1번 훑어두기.

## 🚨 트리거 → 대응

### Trigger 1: 하루 10h도 못 채우는 게 이틀 연속
**원인**: 피로 누적, 특정 개념 막힘, 번아웃 초입
**대응**:
1. 그날 필수 체크리스트만 완료 (**Stretch + 논문 Figure 전부 버림**)
2. 잠 8h+ 보장
3. 다음 날 오전 블록은 "읽기"만 — 실습 오후로 밀기
4. 주제가 계속 막히면 Day 순서를 재편 (아래 "선택적 건너뛰기")

### Trigger 2: 특정 Day 실습이 안 끝남 (예: Day 8 고급 RAG, Day 13 Fine-tuning)
**원인**: 프로젝트 범위가 너무 넓음
**대응**:
1. Must-have (필수 체크리스트)만 남기고 나머지 **내일로 ship**
2. `daily-log.md`에 "미완료: X, Y. Day N+1에 이어서" 명시
3. 다음 Day 시작 시 20분 "어제 이월" 블록 삽입
4. 3일 연속 미완이면 Day 순서 대폭 압축 (아래 "C 모드")

### Trigger 3: API 크레딧 고갈
**원인**: 실험 횟수 많음, 큰 모델 남발
**대응**:
1. Flash/Haiku 4.5/4o-mini 등 **작은 모델로 일괄 전환**
2. `shared/ai_study/tokens.py` → `make pricing`으로 비용 사전 추정 습관
3. **Prompt caching 적극** 사용 (Day 12 내용 앞당기기) — Anthropic 90% 절감
4. **Batch API** — Day 11 내용 앞당기기, 50% 절감
5. 마지막 수단: Ollama로 그날의 LLM 호출 전부 로컬화

### Trigger 4: Docker/Qdrant/Langfuse 안 뜸
**원인**: 포트 충돌, 볼륨 권한, 이미지 pull 실패
**대응**:
1. `docker ps -a` + `docker logs <name>` 로그 그대로 검색
2. 볼륨 초기화 (`make clean-docker` 또는 `rm -rf infra/<x>/volumes`)
3. 버전 고정 (latest → 명시적 버전)
4. **우회**: Qdrant 대신 Chroma in-memory / Langfuse 대신 Phoenix
5. 최후: 해당 Day의 인프라 실습을 cloud 버전 (Qdrant Cloud, Langfuse Cloud 무료 tier)로 전환

### Trigger 5: 키 쓰였는데 응답 품질이 이상함
**원인**: 모델명 오타, 무료 tier 제한, rate-limit로 잘림
**대응**:
1. 모델명 **정확히 확인** — 2026-04 기준 `claude-sonnet-4-6`, `gpt-4o-mini`, `gemini-2.5-flash` (`gemini-3-flash-preview`도 가능)
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

### Trigger 7 (v3 신규): Day 13 Fine-tuning GPU 훈련 실패
**원인**: OOM, dependency, template mismatch, Spot 인스턴스 interrupt
**대응**:
1. **VRAM OOM** → QLoRA 4-bit + `--max-model-len 4096` 낮춤
2. **Unsloth 설치 실패** → Linux+CUDA 필수. Mac은 불가능. RunPod Pod만
3. **Chat template 불일치** → Unsloth Qwen3 notebook 그대로 복붙
4. **Spot interrupt** → `save_steps=50`으로 checkpoint 자주 → 재개
5. **최후 수단**: Day 13을 개념 학습만 → Day 14 portfolio에는 Fine-tuned 빼고 base model만

### Trigger 8 (v3 신규): Day 12 Modal 배포 실패
**원인**: 크레딧 없음, secret 주입 실패, cold start timeout
**대응**:
1. Modal free tier는 충분 (월 $30 credit)
2. `modal secret create api-keys` 먼저
3. Cold start 길면 `@modal.function(keep_warm=1)` (비용 ↑)
4. 최후: Fly.io로 대체 or 그냥 local Docker 실행

---

## 📉 전체 일정 뒤처짐 → 모드 축소

### A 모드 (정상): 14일 전부 + Stretch + 논문 25편
원래 v3 ULTRA 계획.

### B 모드 (1-2일 뒤처짐): 14일 / Stretch 버림
- 필수 체크리스트만
- Day 순서 유지
- Stretch + 논문 Figure 읽기 → **Claude 요약만 신뢰**
- Advanced Topics Rapid Fire (Day 14)는 3개만 (MoE / Speculative / FlashAttention)

### C 모드 (3일 이상 뒤처짐): v2로 다운그레이드
v3 ULTRA 추가분을 **"나중"**으로 이동:
- Day 3 Prompt-Guard 2 → 14일 이후
- Day 7 Vision RAG → 14일 이후
- Day 9 Multi-agent → LangGraph Supervisor 1개만
- Day 10 Voice → Whisper 간단 smoke만
- Day 11 Batch API + Guardrails 3겹 → MCP만 + 기본 safety
- Day 12 Deploy → Langfuse만 (Modal은 14일 이후)
- Day 13 Fine-tuning → Local LLM + RunPod만 (v2 수준)
- Day 14 Advanced Topics → 개념 1-2개만

→ v2 수준 10h × 14일 / total 140h

### D 모드 (완전 붕괴): 코어만 (7-10일)
**가장 중요한 것만** — LLM 엔지니어 최소 역량:
1. 3-provider chat wrapper (Day 2)
2. Structured output (Day 4)
3. Tool use (Day 5)
4. 기본 RAG 하나 (Day 7 수준)
5. Eval 최소 1개 돌려보기 (Day 9)
6. Langfuse trace 1번 찍기 (Day 12)
→ 실제로 7-8일이면 가능

---

## 🧘 회복 루틴

### 번아웃 사전 경고
- 웃음 사라짐
- 코드 보기 싫음
- 사소한 에러에 화
- 오전 시작이 10시 넘어감 (v3에서는 09시가 기준)

→ 즉시 **하루 전체 쉬기**. 14일이 15일이 되는 게 뒤처짐이 아니라 붕괴보다 낫다.

### 회복일 사용법
- 공부 자료 열지 않기
- 자연광
- 긴 운동 1회
- 잠 충분히
- 회복일 저녁에 `daily-log.md`에 "회복일: 이유 + 내일 재개 플랜"만 짧게

### 컨디션 자가진단 (매일 밤)
- 수면 시간 (**7h 이하면 경고** — v3는 집중 강도 높음)
- 오늘 한 시간 대비 몰입률 (1-5)
- 내일 시작 에너지 (1-5)
→ 3 이하 연속 2일 = 속도 줄이기

---

## 🛑 Don'ts

- ❌ 오늘 못 끝낸 걸 내일 자정 넘어 마무리 (Day 13/14 극한 모드 예외)
- ❌ "내일부터 더 열심히"로 오늘 회피
- ❌ 특정 공식 문서를 원문으로 읽기 싫다고 한글 블로그 반나절
- ❌ Day 10 agent가 안 돌아간다고 Day 9 eval을 건너뛰기 (오히려 eval이 답 지시해줌)
- ❌ 포트폴리오에 미운영 기능 끼워넣기 ("될지도 모르니" 배제)
- ❌ **v3 ULTRA 전부 완주 욕심** — C 모드 후퇴 부끄럽지 않다

## ✅ Do's

- ✔ 매일 커밋 (작아도)
- ✔ 에러 메시지 풀 카피해서 노트로
- ✔ "내일 나"에게 3줄 메모 남기기
- ✔ 완료 기준 사전 정의
- ✔ 막히면 Claude/문서에 질문 — 자존심 쓰지 말 것
- ✔ `resources/pre-digested.md` 먼저 확인 (링크 열기 전)
