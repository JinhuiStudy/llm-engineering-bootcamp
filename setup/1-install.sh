#!/usr/bin/env bash
# AI Study Bootcamp — one-shot installer
# 최초 1회만 실행. 이미 깔린 건 skip.

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info()  { echo -e "${GREEN}✔${NC} $1"; }
warn()  { echo -e "${YELLOW}⚠${NC} $1"; }
fail()  { echo -e "${RED}✗${NC} $1"; exit 1; }

echo "── 1. Python 3.11+ 확인"
if ! command -v python3 &>/dev/null; then
    fail "python3 없음. brew install python@3.12"
fi
PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ "$(printf '%s\n' "3.11" "$PYVER" | sort -V | head -n1)" != "3.11" ]]; then
    fail "Python 3.11+ 필요. 현재: $PYVER"
fi
info "Python $PYVER"

echo "── 2. uv"
if ! command -v uv &>/dev/null; then
    warn "uv 설치 중..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi
info "uv $(uv --version)"

echo "── 3. Docker"
if ! command -v docker &>/dev/null; then
    fail "Docker Desktop 필요: https://www.docker.com/products/docker-desktop/"
fi
if ! docker ps &>/dev/null; then
    fail "Docker daemon 미실행. Docker Desktop 앱 켜기."
fi
info "Docker OK"

echo "── 4. git"
command -v git &>/dev/null || fail "git 없음"
info "git $(git --version | awk '{print $3}')"

echo "── 5. .env"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"
if [ ! -f .env ]; then
    cp .env.example .env
    warn ".env 생성됨. 이제 편집 필요: $ROOT_DIR/.env"
else
    info ".env 이미 존재"
fi

echo "── 6. shared deps"
cd "$ROOT_DIR/shared"
uv sync
info "shared/ sync 완료"

echo ""
echo "${GREEN}── 설치 끝 ──${NC}"
echo "다음: "
echo "  1) .env 편집 (API 키 3개 이상)"
echo "  2) make verify"
echo "  3) make qdrant-up  (Day 6부터 필요)"
