# AI Study Bootcamp — Makefile
# `make help` 로 전체 명령 보기

.PHONY: help setup verify qdrant-up qdrant-down langfuse-up langfuse-down \
        infra-up infra-down clean-data status day1 day2 portfolio

help: ## 이 도움말
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── 초기 세팅 ──
setup: ## 최초 1회: uv sync + .env 복사
	@if [ ! -f .env ]; then cp .env.example .env && echo "✔ .env 생성됨. API 키 채워넣기"; fi
	cd shared && uv sync
	@echo "✔ setup 완료. 다음: make verify"

verify: ## API 키/모델 연결 점검
	cd shared && uv run python ../setup/2-verify.py

# ── 로컬 인프라 ──
qdrant-up: ## Qdrant 로컬 실행 (Day 6+)
	docker compose -f infra/qdrant/docker-compose.yml up -d
	@echo "→ http://localhost:6333/dashboard"

qdrant-down: ## Qdrant 중지
	docker compose -f infra/qdrant/docker-compose.yml down

langfuse-up: ## Langfuse self-host (Day 12+)
	docker compose -f infra/langfuse/docker-compose.yml up -d
	@echo "→ http://localhost:3000  (초기 가입 후 프로젝트 만들기)"

langfuse-down: ## Langfuse 중지
	docker compose -f infra/langfuse/docker-compose.yml down

ollama-pull: ## Day 13: 로컬 모델 받기
	ollama pull qwen2.5:7b

infra-up: qdrant-up langfuse-up ## 전체 로컬 인프라 기동

infra-down: qdrant-down langfuse-down ## 전체 중지

# ── 유지보수 ──
clean-data: ## 프로젝트별 outputs/, results/ 정리 (주의)
	find projects -type d -name outputs -exec rm -rf {} + || true
	find projects -type d -name results -exec rm -rf {} + || true

status: ## 현재 상태 요약
	@echo "── Docker ──" ; docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -E 'qdrant|langfuse|postgres|clickhouse' || echo "(no infra running)"
	@echo "" ; echo "── .env 존재 여부 ──" ; [ -f .env ] && echo "✔ .env OK" || echo "✗ .env 없음 (make setup)"
	@echo "" ; echo "── Ollama ──" ; ollama list 2>/dev/null || echo "(ollama 미설치 or 미실행)"

# ── Day별 바로가기 ──
day1: ## Day 1 체크리스트 출력
	@cat curriculum/week1-day01-llm-basics.md | head -60

day2: ## Day 2 체크리스트
	@cat curriculum/week1-day02-api-providers.md | head -60

portfolio: ## 최종 포트폴리오 체크리스트
	@cat projects/final-portfolio/README.md
