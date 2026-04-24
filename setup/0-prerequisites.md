# 사전 준비 — Day 1 시작 전 0~2시간

**이 문서 끝낼 때까지는 커리큘럼 시작하지 말 것.** 여기서 막히면 Day 1이 2일이 된다.

## 체크리스트 (순서대로)

### 1. 시스템 도구 (15분)

```bash
# Homebrew (이미 있으면 skip)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 3.11+ 확인
python3 --version  # 3.11 이상이면 OK

# uv (Python 의존성 관리 — pip/poetry보다 10배 빠름)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Docker Desktop — 수동 설치
# https://www.docker.com/products/docker-desktop/
docker --version
docker compose version

# git
git --version
```

### 2. API 계정 + 키 (20분)

| Provider | URL | 비용 |
|---|---|---|
| OpenAI | https://platform.openai.com/api-keys | 카드 필요, $5 충전 권장 |
| Anthropic | https://console.anthropic.com/settings/keys | 카드 필요, $5 충전 권장 |
| Google AI Studio | https://aistudio.google.com/apikey | **무료** (rate 제한) |
| Tavily (옵션, Day 5) | https://tavily.com/ | 무료 1000 req/mo |
| Cohere (옵션, Day 8) | https://dashboard.cohere.com/ | 무료 trial |
| RunPod (Day 13) | https://www.runpod.io/ | $5~$10 필요 |

### 3. 프로젝트 클론/이동 + 키 주입 (5분)

```bash
cd /Users/parkjinhui/Desktop/dev/ai-study
cp .env.example .env
# .env 열어서 3개 API 키 채우기 (최소 OpenAI/Anthropic/Google)
$EDITOR .env
```

### 4. Python 의존성 설치 (5분)

```bash
# 루트 Makefile 사용
make setup

# 또는 수동
cd shared
uv sync
```

### 5. 연결 점검 (5분)

```bash
make verify
```

3사 API가 모두 200 응답 + 샘플 출력이 보이면 OK. 실패하면:
- 401 → 키 오타/없음. `.env` 다시 확인
- 403 → 크레딧 없음. 충전
- 네트워크 → VPN/프록시 점검

### 6. Docker 인프라 미리 기동 테스트 (10분)

```bash
make qdrant-up
# → http://localhost:6333/dashboard 접속 확인
curl http://localhost:6333/collections   # {"result":{"collections":[]},...}
make qdrant-down   # 다음 필요 시 다시 켤 것
```

Langfuse는 Day 12 때 처음 기동 (디스크/RAM 꽤 씀).

### 7. IDE / 에디터

- 추천: VS Code 또는 Cursor
- 필수 확장: Python, Jupyter, Ruff
- `.vscode/settings.json` 은 필요 시 별도 작성

### 8. GitHub 포트폴리오 레포 (5분)

```bash
# GitHub에서 빈 레포 생성: llm-bootcamp-portfolio
# 지금은 remote만 메모, 본격 push는 Day 14
```

### 9. Claude Desktop (Day 11 MCP용)

- https://claude.ai/download
- 지금은 설치만. 설정은 Day 11에.

### 10. Ollama (Day 13용 — 지금 안 해도 됨)

```bash
brew install --cask ollama
# 또는 https://ollama.com/download
```

---

## 완료 기준

```bash
make status
```

출력에 다음이 모두 있어야 함:
- ✔ `.env` OK
- Docker가 정상 응답 (`docker ps` 에러 없음)
- `python3 --version` ≥ 3.11
- `uv --version` 출력됨

## 자주 막히는 것
- **Docker가 안 뜸**: Docker Desktop 실행 중인지 확인. 설치만 하고 앱 안 켠 경우 많음.
- **Python 3.11 미만**: `brew install python@3.12` 후 path 설정.
- **uv sync 실패**: `cd shared`에서 돌렸는지 확인. 루트에서 돌리면 pyproject.toml 없음.
- **API 키 쓰는데 403**: 첫 $5 충전이 반영되기까지 몇 분 걸릴 수 있음.

## 예상 소요
- 최소: 1시간
- 현실: 1.5~2시간 (API 가입/결제 + Docker Desktop 첫 설치 포함)

여기 다 했으면 `curriculum/00-roadmap.md` 보고 Day 1로.
