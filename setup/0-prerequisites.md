# 사전 준비 — Day 1 시작 전 0~2시간

> **Day 0 플랜은 [`curriculum/day00-prep.md`](../curriculum/day00-prep.md) 참조**. 이 문서는 **설치/검증 액션만** 요약.

## 🎯 완료 기준 1줄

```bash
make verify  # 3사 API 모두 200 + make qdrant-up OK + python3 ≥ 3.11
```

## 체크리스트 (순서대로)

### 1. 시스템 도구 (15분)

```bash
# macOS
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 3.11+
python3 --version  # 3.11 이상 / 미만이면 brew install python@3.12

# uv (표준)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Docker Desktop (수동)
# https://www.docker.com/products/docker-desktop/
docker --version
docker compose version

# git
git --version
```

### 2. API 계정 + 키 (20-30분)

상세 → [`setup/3-accounts-checklist.md`](3-accounts-checklist.md)

**필수 3사**:
- OpenAI: https://platform.openai.com/api-keys  (카드 + $5 충전)
- Anthropic: https://console.anthropic.com/settings/keys (카드 + $5 충전)
- Google AI Studio: https://aistudio.google.com/apikey (무료)

**옵션**: Tavily (Day 5 web search) / Cohere (Day 8 rerank) / RunPod (Day 13 GPU)

### 3. 프로젝트 준비 (5분)

```bash
cd /Users/parkjinhui/Desktop/dev/ai-study
cp .env.example .env
$EDITOR .env   # 최소 OPENAI_API_KEY / ANTHROPIC_API_KEY / GOOGLE_API_KEY
```

### 4. Python 의존성 (5분)

```bash
make setup
# 또는: cd shared && uv sync
```

### 5. 연결 점검 (5분)

```bash
make verify
```

- 200 모두 → OK
- 401 → 키 오타. `.env` 재확인
- 403 → 크레딧 미반영. 10분 대기 후 재시도
- 네트워크/타임아웃 → VPN/프록시 점검

### 6. Docker 인프라 미리 pull (10분, 백그라운드)

```bash
make qdrant-up
open http://localhost:6333/dashboard
curl http://localhost:6333/collections
make qdrant-down

# Langfuse는 Day 12에. 이미지만 pull:
docker pull langfuse/langfuse:latest
docker pull clickhouse/clickhouse-server:24.3  # infra/langfuse/docker-compose.yml과 일치
docker pull postgres:16-alpine
```

### 7. IDE (5분)

- **VS Code** 또는 **Cursor** 권장
- 필수 extension: Python, Jupyter, Ruff
- 테마는 어두운 색 권장 (눈 피로)

### 8. GitHub 포트폴리오 레포 (5분)

1. github.com 새 빈 repo 생성 (이름: `devlog-rag-copilot` 등)
2. README/gitignore/license 선택 안 함 (Day 14에 push할 때 충돌 방지)
3. 원격 URL 메모만 — push는 Day 14

### 9. Claude Desktop / Claude Code (Day 11용)

- https://claude.ai/download
- Claude Code: `npm install -g @anthropic-ai/claude-code` 또는 https://claude.ai/code
- 설치만, 설정은 Day 11에

### 10. Ollama (Day 13용)

```bash
brew install --cask ollama
# 또는 https://ollama.com/download
# 실행 및 모델 pull은 Day 13
```

---

## 🔍 완료 검증

```bash
make status
```

출력에 모두 ✔:
- `.env` 3개 키
- Python ≥ 3.11
- `uv --version`
- Docker daemon 정상

## 🚫 자주 막히는 것

### Docker 관련
- **`Cannot connect to the Docker daemon`** → Docker Desktop 실행 안 됨. 앱 실행 후 재시도
- **포트 충돌** — `lsof -i :6333` / `lsof -i :3000` — 다른 프로세스 kill or 포트 변경
- **Apple Silicon 경고** — `platform: linux/amd64` 추가 또는 최신 이미지 사용

### Python
- **Python 3.11 못 찾음** — `brew install python@3.12 && echo 'export PATH="/opt/homebrew/opt/python@3.12/libexec/bin:$PATH"' >> ~/.zshrc`
- **`uv sync` 실패 (pyproject.toml not found)** — `cd shared` 먼저
- **SSL cert error** — `/Applications/Python\ 3.12/Install\ Certificates.command` 실행 (Python.org 설치본)

### API
- **`Incorrect API key provided: sk-...`** → `.env` 줄 끝 공백/따옴표 제거
- **`Insufficient quota`** → Billing 탭에서 결제 상태 재확인
- **429 즉시 발생** → tier 1은 RPM 낮음. 다른 호출 멈추고 10s 대기

### 네트워크
- **회사 VPN/프록시** — `export HTTPS_PROXY=http://proxy.internal:8080` (쉘 env 설정)
- **`requests.exceptions.SSLError`** — corporate cert bundle: `REQUESTS_CA_BUNDLE=/path/to/cert.pem`

## 예상 소요

- 최소: 1시간 (이미 Python/Docker 있음)
- 현실: 2-4시간 (첫 API 가입 + Docker Desktop + 결제 반영 대기 포함)

## 다음

완료 → [`curriculum/day00-prep.md`](../curriculum/day00-prep.md)로 멘탈 세팅 + 캘린더 차단 → `curriculum/week1-day01-llm-basics.md`로 Day 1 출발.
