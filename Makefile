# AI Study Bootcamp — Makefile (v2)
# `make help` 로 전체 명령 보기

.PHONY: help setup verify status clean-data \
        qdrant-up qdrant-down langfuse-up langfuse-down phoenix-up \
        infra-up infra-down \
        ollama-pull mcp-inspector \
        fmt lint typecheck test \
        smoke-llm smoke-embed smoke-qdrant pricing \
        eval-mini eval-full \
        day0 day1 day2 day3 day4 day5 day6 day7 \
        day8 day9 day10 day11 day12 day13 day14 \
        portfolio open-docs

# ── 기본 ──
help: ## 이 도움말
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'

# ── 초기 세팅 ──
setup: ## 최초 1회: uv sync + .env 복사
	@if [ ! -f .env ]; then cp .env.example .env && echo "✔ .env 생성됨. API 키 채워넣기"; fi
	cd shared && uv sync
	@echo "✔ setup 완료. 다음: make verify"

verify: ## 3사 API 연결 점검 (make setup 후)
	cd shared && uv run python ../setup/2-verify.py

status: ## 현재 상태 요약
	@echo "── .env ──" ; [ -f .env ] && echo "✔ .env OK" || echo "✗ .env 없음"
	@echo "\n── Python ──" ; python3 --version
	@echo "\n── uv ──" ; uv --version 2>/dev/null || echo "✗ uv 없음"
	@echo "\n── Docker ──" ; docker ps --format 'table {{.Names}}\t{{.Status}}' 2>/dev/null | grep -E 'qdrant|langfuse|postgres|clickhouse' || echo "(no infra running)"
	@echo "\n── Ollama ──" ; ollama list 2>/dev/null || echo "(ollama 미설치)"
	@echo "\n── Claude Desktop MCP (macOS) ──" ; [ -f "$$HOME/Library/Application Support/Claude/claude_desktop_config.json" ] && echo "✔ config 존재" || echo "(config 없음)"

# ── 로컬 인프라 ──
qdrant-up: ## Qdrant 로컬 실행 (Day 6+)
	docker compose -f infra/qdrant/docker-compose.yml up -d
	@sleep 2
	@echo "→ http://localhost:6333/dashboard"
	@curl -s http://localhost:6333/collections | head -c 200 || true

qdrant-down: ## Qdrant 중지
	docker compose -f infra/qdrant/docker-compose.yml down

langfuse-up: ## Langfuse self-host (Day 12+, 무거움 — postgres+clickhouse+web)
	docker compose -f infra/langfuse/docker-compose.yml up -d
	@echo "→ http://localhost:3000  (초기 가입 후 프로젝트/키 만들기)"

langfuse-down: ## Langfuse 중지
	docker compose -f infra/langfuse/docker-compose.yml down

phoenix-up: ## Arize Phoenix 로컬 (Day 12 선택)
	docker run -d -p 6006:6006 -p 4317:4317 --name phoenix arizephoenix/phoenix:latest || true
	@echo "→ http://localhost:6006"

infra-up: qdrant-up langfuse-up ## 전체 로컬 인프라 기동
infra-down: qdrant-down langfuse-down ## 전체 중지

# ── Local LLM ──
ollama-pull: ## Day 13: 한국어 강한 Qwen3 + llama3.3 + gpt-oss pull
	ollama pull qwen3:8b
	ollama pull llama3.3:8b-instruct-q4_K_M
	@echo "선택: ollama pull gpt-oss:20b (큰 모델)"

# ── MCP ──
mcp-inspector: ## Day 11: Inspector로 자체 서버 테스트
	npx -y @modelcontextprotocol/inspector uv run python projects/day10-mcp-server/server.py

# ── 품질 (shared) ──
fmt: ## ruff format
	cd shared && uv run ruff format .

lint: ## ruff check
	cd shared && uv run ruff check .

typecheck: ## mypy
	cd shared && uv run mypy ai_study || true

test: ## pytest
	cd shared && uv run pytest -q || true

# ── Smoke tests (Day 1-2 안전망) ──
smoke-llm: ## 3사 chat 1회씩 — 키 유효성 검증
	cd shared && uv run python -m ai_study.llm openai "In one sentence, hello."
	cd shared && uv run python -m ai_study.llm anthropic "In one sentence, hello."
	cd shared && uv run python -m ai_study.llm gemini "In one sentence, hello."

smoke-embed: ## OpenAI 임베딩 smoke
	cd shared && uv run python -c "from ai_study.embeddings import embed; v=embed(['hello']); print(len(v[0]))"

smoke-qdrant: ## Qdrant 연결 smoke
	cd shared && uv run python -c "from ai_study.vectors import client; print(client().get_collections())"

pricing: ## 2026-04 모델별 가격표
	cd shared && uv run python -m ai_study.tokens

# ── Eval (Day 9+) ──
eval-mini: ## Day 9 RAG mini eval (20 샘플)
	cd projects/day08-rag-eval && uv run python run_ragas.py --sample 20 --pipeline full_stack || echo "(Day 9 프로젝트 완성 후 실행)"

eval-full: ## Day 9 RAG 전체 eval
	cd projects/day08-rag-eval && uv run python run_ragas.py --sample all

# ── Day 바로가기 (커리큘럼 열기) ──
day0: ## Day 0 프리컬
	@cat curriculum/day00-prep.md | head -80

day1: ## Day 1 LLM 기초
	@cat curriculum/week1-day01-llm-basics.md | head -80

day2: ## Day 2 3사 API
	@cat curriculum/week1-day02-api-providers.md | head -80

day3: ## Day 3 Prompt
	@cat curriculum/week1-day03-prompt-engineering.md | head -80

day4: ## Day 4 Structured Output
	@cat curriculum/week1-day04-structured-output.md | head -80

day5: ## Day 5 Tool Use
	@cat curriculum/week1-day05-function-calling.md | head -80

day6: ## Day 6 Embedding
	@cat curriculum/week1-day06-embedding-vectordb.md | head -80

day7: ## Day 7 기본 RAG
	@cat curriculum/week1-day07-basic-rag.md | head -80

day8: ## Day 8 고급 RAG
	@cat curriculum/week2-day08-advanced-rag.md | head -80

day9: ## Day 9 Eval
	@cat curriculum/week2-day09-eval.md | head -80

day10: ## Day 10 LangGraph
	@cat curriculum/week2-day10-agents-langgraph.md | head -80

day11: ## Day 11 MCP
	@cat curriculum/week2-day11-mcp.md | head -80

day12: ## Day 12 Observability
	@cat curriculum/week2-day12-observability.md | head -80

day13: ## Day 13 Local LLM
	@cat curriculum/week2-day13-local-llm-runpod.md | head -80

day14: ## Day 14 Portfolio
	@cat curriculum/week2-day14-final-portfolio.md | head -80

portfolio: ## 최종 포트폴리오 체크리스트
	@cat projects/final-portfolio/README.md

open-docs: ## VSCode로 핵심 문서 열기
	@code INDEX.md curriculum/00-roadmap.md curriculum/day00-prep.md curriculum/self-check.md notes/daily-log.md 2>/dev/null || open INDEX.md

# ── 유지보수 ──
clean-data: ## 프로젝트별 outputs/, results/, checkpoints/ 정리 (주의: 결과 삭제)
	find projects -type d \( -name outputs -o -name results -o -name checkpoints -o -name logs \) -exec rm -rf {} + 2>/dev/null || true
	@echo "✔ cleaned"

clean-docker: ## docker volumes 정리 (주의: Qdrant/Langfuse 데이터 삭제)
	@echo "⚠️  Qdrant / Langfuse volumes 삭제. 진행? (5초 대기)"
	@sleep 5
	docker compose -f infra/qdrant/docker-compose.yml down -v
	docker compose -f infra/langfuse/docker-compose.yml down -v
