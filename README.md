# LLM Engineering Bootcamp — 2주 ULTRA 하드코어

[![License: MIT](https://img.shields.io/github/license/JinhuiStudy/llm-engineering-bootcamp?color=blue)](LICENSE)
[![Stars](https://img.shields.io/github/stars/JinhuiStudy/llm-engineering-bootcamp?style=social)](https://github.com/JinhuiStudy/llm-engineering-bootcamp/stargazers)
[![Issues](https://img.shields.io/github/issues/JinhuiStudy/llm-engineering-bootcamp)](https://github.com/JinhuiStudy/llm-engineering-bootcamp/issues)
[![Made with Python](https://img.shields.io/badge/Python-3.11%2B-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-managed-261230?logo=python&logoColor=white)](https://docs.astral.sh/uv/)
[![Docker](https://img.shields.io/badge/Docker-Qdrant%20%2B%20Langfuse-2496ed?logo=docker&logoColor=white)](infra/)

8년차 소프트웨어 개발자가 LLM 앱 엔지니어로 전환하는 **14일 ULTRA 속성 커리큘럼** (v3).
하루 **12-14시간** × 14일 = **~170시간**.

> 목표 (v3 ULTRA): Prompt → Structured → Tool → Embedding → RAG → **Vision RAG** → Eval → **Multi-agent** → MCP → **Batch API + Guardrails 3겹** → **Observability + Deployment (Modal)** → Local LLM + **Fine-tuning (LoRA/QLoRA/DPO)** → **Advanced Topics (MoE/FlashAttention/...)** + **Portfolio 공개** — 2주 안에 전부.

## 👉 바로 시작

```bash
# 1. Day 0 프리컬 (2-4h)
cat curriculum/day00-prep.md

# 2. 사전 준비 가이드
cat setup/0-prerequisites.md

# 3. 설치
./setup/1-install.sh           # 또는: make setup

# 4. API 키 채우기
$EDITOR .env

# 5. 점검
make verify

# 6. 2026-04 최신 복붙 코드 한 번에 훑기 (v3.1 신규)
cat resources/pre-digested.md | head -200

# 7. 로드맵 읽기
cat curriculum/00-roadmap.md

# 8. Day 1 출발
cat curriculum/week1-day01-llm-basics.md
```

**전체 네비게이션**은 [`INDEX.md`](INDEX.md).

## 📏 v3 규모 요약

- 📄 **130+ 파일 / 40 dirs**, 10,000+ 줄 문서
- 📚 14개 일자별 커리큘럼 (각각 수치 기준 + 실전 함정 + Stretch)
- ⭐ **[`resources/pre-digested.md`](resources/pre-digested.md)** — 공식 문서 WebFetch로 직접 뽑은 복붙 가능 코드 (1100+ 줄)
- 🔗 `resources/links-classified.md`: 150+ 링크 분류 + 요약
- 💻 13개 프로젝트 스타터 코드 + 각 프로젝트 pyproject.toml
- 🧰 공통 Python 패키지 (`ai_study.*`) — config / llm / embeddings / vectors / tokens / prompts / langfuse_client
- 🐳 Docker compose (Qdrant + Langfuse self-host)
- 🛠 one-shot installer + verify + 15+ Makefile 타겟
- 📜 논문 **25편** Figure 수준 배치
- 🎯 최종: **"Devlog RAG Copilot ULTRA"** (Vision + Voice + Multi-agent + Fine-tuned + Guardrails + Modal public URL)

## 디렉토리 구조

```
ai-study/
├── INDEX.md                       ← 마스터 TOC (먼저 여기로)
├── README.md                      ← 이 파일
├── .env.example                   ← 환경변수 템플릿 (2026-04 기준)
├── .gitignore
├── Makefile                       ← make help / day1..day14 / smoke-* / eval-* / deploy
│
├── setup/                         ← Day 0 준비
│   ├── 0-prerequisites.md
│   ├── 1-install.sh               ← one-shot installer
│   ├── 2-verify.py                ← API 연결 점검 (make verify)
│   └── 3-accounts-checklist.md
│
├── shared/                        ← 공통 Python 패키지 (ai_study.*)
│   ├── pyproject.toml             ← 모든 deps (2026-04 기준)
│   └── ai_study/
│       ├── config.py              ← .env 로딩 + Settings
│       ├── llm.py                 ← 4-provider chat/stream (openai/anthropic/gemini/ollama)
│       ├── embeddings.py          ← 3사 + 로컬 SBERT
│       ├── vectors.py             ← Qdrant helper
│       ├── tokens.py              ← 토큰/비용 (2026-04 PRICING)
│       ├── prompts.py             ← Jinja2 template 렌더
│       ├── langfuse_client.py     ← @observe no-op fallback
│       ├── logging.py
│       └── retry.py
│
├── infra/                         ← Docker compose (Qdrant + Langfuse self-host)
│   ├── qdrant/docker-compose.yml
│   └── langfuse/docker-compose.yml
│
├── curriculum/                    ← 일자별 플랜 (v3 ULTRA)
│   ├── 00-roadmap.md              ← 14일 전체 + 논문 25편 스케줄
│   ├── day00-prep.md              ← Day 0 프리컬 + 멘탈 세팅 (v3.1 신규)
│   ├── schedule.md                ← 12-14h 시간 블록
│   ├── self-check.md              ← Day별 자가진단 (기본/심화/ULTRA 3단)
│   ├── troubleshooting.md         ← 13 카테고리 FAQ (v3 신규)
│   ├── recovery-playbook.md       ← 뒤처졌을 때 A/B/C/D 모드
│   ├── extras.md                  ← 14일 이후 심화 트랙
│   └── week{1,2}-day{01..14}-*.md
│
├── resources/                     ← 링크 분류 + 요약
│   ├── 00-top20-priority.md       ← Top 20 최우선 자료
│   ├── pre-digested.md            ← ⭐ 공식 문서 직접 fetch한 복붙 코드 (v3.1 신규)
│   ├── links-classified.md        ← 모든 URL + WebFetch 요약
│   ├── must-read.md / optional.md / later.md / skip.md
│
├── projects/                      ← 실습 + 스타터 코드 (각자 pyproject.toml)
│   ├── day01-chatbot-cli/         (chat.py, tokens.py, temperature_demo.py)
│   ├── day02-prompt-lab/          (runner.py, prompts/)
│   ├── day03-structured-extractor/(schemas.py, extract.py)
│   ├── day04-tool-agent/          (agent.py, tools/)
│   ├── day05-embedding-search/    (ingest.py, search.py, compare.py)
│   ├── day06-basic-rag/           (ingest.py, rag.py, prompts/)
│   ├── day07-advanced-rag/        (retrievers/, query_transform/)
│   ├── day08-rag-eval/            (run_ragas.py — Ragas v0.2)
│   ├── day09-langgraph-agent/     (state.py, graph.py)
│   ├── day10-mcp-server/          (server.py FastMCP)
│   ├── day11-observability/       (instrument / rate_limit / prompt_cache)
│   ├── day12-local-llm/           (ollama_chat / ollama_rag / runpod/vllm_client / benchmark)
│   └── final-portfolio/           (ARCHITECTURE.md, app/main.py)
│
├── notes/                         ← 개인 노트
│   ├── keywords.md                ← Tier S/A/B/C 핵심 용어
│   ├── concepts.md                ← 개념 정리 (본인 언어)
│   ├── daily-log.md               ← Day별 회고
│   └── decisions.md               ← ADR 간소판
│
├── cheatsheets/                   ← 빠른 참조
│   ├── prompt-patterns.md
│   ├── rag-patterns.md
│   ├── eval-metrics.md
│   ├── api-compare.md             ← OpenAI / Anthropic / Gemini (2026-04 기준)
│   ├── agent-patterns.md          (v2 신규)
│   ├── production-patterns.md     (v2 신규)
│   └── mcp-cheatsheet.md          (v2 신규)
│
└── data/                          ← 공용 데이터 (gitignore)
    ├── pdfs/    golden/    samples/
```

## 핵심 명령

```bash
make help              # 15+ 타겟
make setup             # 최초 1회
make verify            # 3사 API 점검
make smoke-llm         # chat smoke
make pricing           # 2026-04 모델 가격표
make qdrant-up         # Day 6+
make langfuse-up       # Day 12+
make infra-up          # 둘 다
make ollama-pull       # Day 13 모델 pull (qwen3:8b / llama3.3:8b)
make mcp-inspector     # Day 11 MCP 서버 디버깅
make eval-mini         # Day 9 20-sample Ragas
make day1 / day2 / ... / day14   # Day별 커리큘럼 head 열기
make status            # 전체 상태
```

## v3 ULTRA 규칙 (강화)

- **공식 문서 우선** — 한국어 블로그 금지 기본. 막힐 때만 보조
- **튜토리얼 한 번만** — 두 번째는 변형
- **수치로 말한다** — Eval 없는 RAG 개선은 미신 (Ragas faithfulness ≥ 0.85)
- **Prompt caching** 적극 — Anthropic 90% 절감
- **GPU 예산** — RunPod H100 $25 상한 (Day 13)
- **논문 Figure만** — 본문 통독 X, Claude 요약 활용
- **매일 커밋** — 작아도
- **뒤처지면** → [`curriculum/recovery-playbook.md`](curriculum/recovery-playbook.md)
- **막히면** → [`curriculum/troubleshooting.md`](curriculum/troubleshooting.md)

## 💰 예산 (v3 ~$45-90)

OpenAI $15-25 + Anthropic $10-20 + Gemini $0 + RunPod Serverless $5-10 + **RunPod H100 Fine-tuning $15-25** + Modal free tier.

## 📚 참고

- [`INDEX.md`](INDEX.md) — 마스터 TOC
- [`curriculum/00-roadmap.md`](curriculum/00-roadmap.md) — 14일 로드맵
- [`resources/pre-digested.md`](resources/pre-digested.md) — ⭐ 2026-04 복붙 코드
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — PR/Issue 환영
