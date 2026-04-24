# Day 0 — 사전 준비 + 멘탈 세팅 (2-4시간)

> **Day 1 시작 전 반드시 완주**. 여기서 막히면 Day 1이 이틀이 된다.
> **시간 예산**: 최소 2시간, 현실 3-4시간 (API 결제 + Docker 첫 설치 + 계정 가입 포함)

## 🎯 Day 0 끝나면

1. 3사 API 키가 `.env`에 채워져 `make verify` 통과
2. Docker Desktop 기동 + Qdrant/Langfuse 이미지 pull 완료 (실행은 Day 6/12에)
3. Python 3.11+ + uv 설치 + `shared/` 환경 sync 완료
4. GitHub 레포 생성 (이름만, 실제 push는 Day 14)
5. Claude Desktop / Claude Code / Cursor 중 **최소 1개** 설치 (Day 11 MCP용)
6. Ollama 설치만 완료 (모델 pull은 Day 13)
7. IDE 준비 + 14일 일정 표 개인 캘린더에 차단
8. 멘탈 세팅 — "왜 나는 이걸 하는가" 1문단 저널에

## 📋 순서 (체크하면서 진행)

### 1️⃣ 시스템 도구 (15분)

```bash
# macOS
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 3.11+ 확인 (없으면 설치)
python3 --version
# 3.11 미만이면: brew install python@3.12

# uv (Python deps 관리)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.zshrc   # 또는 새 터미널
uv --version      # 0.5+

# Docker Desktop (수동 설치)
# https://www.docker.com/products/docker-desktop/
docker --version
docker compose version

# git
git --version
```

### 2️⃣ 계정 개설 + 결제 (30-60분)

**상세**: [`setup/3-accounts-checklist.md`](../setup/3-accounts-checklist.md)

| 우선 | Provider | URL | 예상 비용 (14일) |
|---|---|---|---|
| 필수 | OpenAI | https://platform.openai.com | $10-15 |
| 필수 | Anthropic | https://console.anthropic.com | $10-15 |
| 필수 | Google AI Studio | https://aistudio.google.com/apikey | $0 (free tier) |
| 선택 | Tavily | https://tavily.com | $0 (free 1k/mo) |
| 선택 | Cohere | https://dashboard.cohere.com | $0 (trial) |
| Day 13 | RunPod | https://runpod.io | $5-10 |
| 최종 | GitHub | https://github.com | $0 |

**주의사항**
- API 충전 반영까지 **몇 분 걸림**. 첫 호출이 403/429면 10분 뒤 재시도
- Auto-recharge **끄고** 수동 $5 충전 (실수 재난 방지)
- 키는 `.env`에만. 절대 코드에 하드코딩/커밋 금지

### 3️⃣ 프로젝트 클론 + 키 주입 (5분)

```bash
cd /Users/parkjinhui/Desktop/dev/ai-study   # 또는 본인 경로
cp .env.example .env
$EDITOR .env   # 3사 키 최소 OPENAI/ANTHROPIC/GEMINI 채우기
```

### 4️⃣ Python 의존성 (5분)

```bash
# Makefile 단축
make setup

# 또는 수동
cd shared
uv sync
```

### 5️⃣ 연결 점검 (5분)

```bash
make verify
```

3사 API 200 응답 + 샘플 출력. 실패 시:
- 401 → 키 오타/없음. `.env` 재확인
- 403 → 크레딧 미반영. 10분 대기 후 재시도
- 네트워크 → VPN/프록시 점검. 회사 망이면 프록시 환경변수

### 6️⃣ Docker 인프라 pull (10분, 백그라운드)

```bash
make qdrant-up
open http://localhost:6333/dashboard   # 접속 확인
curl http://localhost:6333/collections  # {"result":{"collections":[]},...}
make qdrant-down

# Langfuse는 Day 12에 (디스크/RAM 꽤 씀). 이미지만 미리 pull해두고 싶으면:
docker pull langfuse/langfuse:latest
docker pull clickhouse/clickhouse-server:24.10-alpine
```

### 7️⃣ IDE / 에디터 (5분)

- 추천: **VS Code** 또는 **Cursor** (MCP 연동 테스트도 할 것)
- 필수 extension: Python, Jupyter, Ruff
- 선택: GitHub Copilot, GitLens
- `.vscode/settings.json` 은 취향 따라

### 8️⃣ GitHub 포트폴리오 레포 (5분)

1. github.com에서 새 repo 생성 — 이름 예: `devlog-rag-copilot`
2. **빈** repo (README/license/gitignore 모두 안 만듦) — Day 14에 push할 때 충돌 방지
3. URL을 `notes/daily-log.md` 위에 메모
4. Public or Private — 공개 목표면 Public

### 9️⃣ Claude Desktop (Day 11용, 지금 설치만)

- https://claude.ai/download → macOS/Windows
- Pro 계정 없어도 MCP 연결 가능 (free tier도 됨)
- 설정은 Day 11에

### 🔟 Ollama (Day 13용, 설치만)

```bash
brew install --cask ollama
# 또는 https://ollama.com/download
# 실행은 Day 13. 지금은 설치만.
```

### 🧠 멘탈 세팅 (10분)

**`notes/daily-log.md` 상단에 작성**:
1. "왜 나는 14일 동안 이걸 하는가?" 1-2 문단
2. "14일 끝나면 내가 바뀌어 있을 것" 3가지
3. "실패해도 괜찮은 것 / 절대 포기하지 않을 것" 각 2-3개
4. "나를 방해할 것" 목록 — 슬랙/미팅/야근/갑자기 바빠짐. 대응 계획.

이건 자존심이 아니라 실전이다. 멘탈 리소스도 한정된 자원. Day 5쯤 막히면 이 글이 살려준다.

## ✅ 완료 기준

```bash
make status
```

출력에 모두 있어야:
- ✔ `.env` OK (3개 키)
- ✔ Python ≥ 3.11
- ✔ uv installed
- ✔ Docker daemon running
- ✔ `shared/` synced

## 📅 14일 캘린더 차단

Google Calendar / Apple Calendar에 다음 블록 반복 설정:

- **평일**: 08:30-21:30 (점심 12:30-13:30)
- **토요일**: 오전 3-4h 주간 몰입
- **일요일**: 오전 2h 복습 + 오후 쉬기
- **매일 21:30 이후**: 수면 우선 — 공부 차단

가족/연인/친구한테 "2주 연락 제한" 공유. 응급 제외.

## 🚫 자주 막히는 것 (실전 함정)

1. **Docker Desktop 설치만 하고 앱 실행 안 함** — `docker ps`가 에러면 먼저 Docker Desktop 실행
2. **Python 3.11 미만인데 `python3` 명령어 안 업데이트** — `brew install python@3.12` 후 path 순서 확인
3. **uv sync 실패 (`pyproject.toml not found`)** — 반드시 `cd shared` 후 실행. 루트에선 없음
4. **API 키 넣었는데 403** — 결제 반영 대기 (5-10분). 카드 등록만 하고 충전 안 함? 재확인
5. **macOS Gatekeeper가 Docker/Ollama 차단** — 시스템 설정 > 보안 > "Open anyway"
6. **프록시 뒤에서 pip/uv 실패** — `HTTPS_PROXY=http://...` env
7. **Github Private repo 만들고 Push 권한 없음** — SSH key 등록 or `gh auth login`
8. **.env가 .gitignore에 있는 줄 알고 실수로 add** — `git check-ignore .env` 확인

## 📚 Day 1 전 추천 복습 (20분)

- [`INDEX.md`](../INDEX.md) 훑기
- [`curriculum/00-roadmap.md`](00-roadmap.md) 14일 일람
- [`curriculum/schedule.md`](schedule.md) 시간 블록
- [`curriculum/recovery-playbook.md`](recovery-playbook.md) 뒤처질 때 대응
- [`notes/keywords.md`](../notes/keywords.md) Tier S 용어 15개

## ⭐ Pre-Digested 문서 숙지 (30분) — v3.1 신규

**[`resources/pre-digested.md`](../resources/pre-digested.md)** 를 30분 들여 훑어라. 여기에 있는 것:

- **2026-04 최신 변경**: Anthropic 도메인 이전, 신 모델명(Opus 4.7/Sonnet 4.6/Haiku 4.5), Gemini 3, LangGraph 도메인 이전
- **Day 1-14 핵심 코드 복붙 가능 패턴** — 공식 문서 직접 fetch해서 검증한 코드
- **Qdrant quickstart / LangGraph StateGraph / Langfuse @observe / Anthropic Prompt Caching / Contextual Retrieval 공식 수치 / Modal 배포 / Unsloth LoRA**
- **논문 25편 Day별 배치 + 요약 프롬프트**
- **공식 문서 직링크 테이블** (2026-04 확인됨)

👉 **이 문서 하나 훑으면 Day 1-14 내내 링크 열 필요 50% 감소**.

## 예산 요약

| 항목 | 예상 |
|---|---|
| OpenAI | $10-15 |
| Anthropic | $10-15 |
| Gemini | $0 |
| RunPod (Day 13) | $5-10 |
| **합계** | **$25-40** |

카페인/간식 / 전기세 별도.

---

완료했으면 `curriculum/week1-day01-llm-basics.md`로 출발. **Day 1 시작 전에 7시간 이상 자고 아침 먹고.**
