# LLM Engineering Bootcamp — 2주 하드코어

8년차 소프트웨어 개발자가 LLM 앱 개발자로 전환하기 위한 **14일 속성 커리큘럼**.
하루 10시간+ 기준 총 ~140시간.

> 목표: Prompt → Structured Output → Function Calling → Embedding → RAG → Eval → Agent → MCP → Observability → Production 까지 실무 수준으로 타파.

## 👉 바로 시작

```bash
# 1. 사전 준비 가이드
cat setup/0-prerequisites.md

# 2. 설치
./setup/1-install.sh           # 또는: make setup

# 3. API 키 3개 채우기
$EDITOR .env

# 4. 점검
make verify

# 5. 로드맵 읽기
cat curriculum/00-roadmap.md

# 6. Day 1 출발
cat curriculum/week1-day01-llm-basics.md
```

**전체 네비게이션**은 [`INDEX.md`](INDEX.md).

## 디렉토리 구조

```
ai-study/
├── INDEX.md                       ← 마스터 TOC (먼저 여기로)
├── README.md                      ← 이 파일
├── .env.example                   ← 환경변수 템플릿
├── .gitignore
├── Makefile                       ← make help
│
├── setup/                         ← Day 0 준비
│   ├── 0-prerequisites.md
│   ├── 1-install.sh               ← one-shot installer
│   ├── 2-verify.py                ← API 연결 점검 (make verify)
│   └── 3-accounts-checklist.md
│
├── shared/                        ← 공통 Python 패키지 (ai_study.*)
│   ├── pyproject.toml             ← 모든 dep (openai/anthropic/qdrant/langfuse/…)
│   └── ai_study/
│       ├── config.py              ← .env 로딩 + settings
│       ├── llm.py                 ← provider-agnostic chat/stream
│       ├── embeddings.py          ← 3사 + 로컬 통합
│       ├── vectors.py             ← Qdrant helper
│       ├── tokens.py              ← 토큰/비용 계산
│       ├── logging.py
│       └── retry.py
│
├── infra/                         ← Docker compose
│   ├── qdrant/docker-compose.yml
│   └── langfuse/docker-compose.yml
│
├── curriculum/                    ← 일자별 플랜
│   ├── 00-roadmap.md              ← 14일 전체
│   ├── schedule.md                ← 하루 시간 블록
│   ├── self-check.md              ← Day별 자가진단
│   ├── recovery-playbook.md       ← 뒤처졌을 때
│   ├── extras.md                  ← 14일 이후 트랙
│   └── week{1,2}-day{01..14}-*.md
│
├── resources/                     ← 링크 분류 + 요약
│   ├── 00-top20-priority.md
│   ├── links-classified.md        ← 단일 진실 소스 (모든 URL + WebFetch 요약)
│   ├── must-read.md  / optional.md / later.md / skip.md
│
├── projects/                      ← 실습 + 스타터 코드
│   ├── day01-chatbot-cli/         (chat.py, tokens.py, temperature_demo.py)
│   ├── day02-prompt-lab/          (runner.py, prompts/01,03,05)
│   ├── day03-structured-extractor/(schemas.py, extract.py)
│   ├── day04-tool-agent/          (agent.py, tools/{weather,calc,search,fileio})
│   ├── day05-embedding-search/    (ingest.py, search.py, compare.py)
│   ├── day06-basic-rag/           (ingest.py, rag.py, prompts/)
│   ├── day07-advanced-rag/        (retrievers/hybrid, rerank; query_transform/hyde, multi_query)
│   ├── day08-rag-eval/            (run_ragas.py, golden_example.json)
│   ├── day09-langgraph-agent/     (state.py, graph.py)
│   ├── day10-mcp-server/          (server.py FastMCP)
│   ├── day11-observability/       (instrument_example, rate_limit, prompt_cache)
│   ├── day12-local-llm/           (ollama_chat, ollama_rag, runpod/vllm_client, benchmark)
│   └── final-portfolio/           (ARCHITECTURE.md, app/main.py)
│
├── notes/                         ← 개인 노트
│   ├── keywords.md                ← Tier S/A/B/C 핵심 용어
│   ├── concepts.md                ← 개념 정리 템플릿
│   ├── daily-log.md               ← Day별 회고
│   └── decisions.md               ← ADR 간소판
│
├── cheatsheets/                   ← 빠른 참조
│   ├── prompt-patterns.md
│   ├── rag-patterns.md
│   ├── eval-metrics.md
│   └── api-compare.md             ← OpenAI / Anthropic / Gemini
│
└── data/                          ← 공용 데이터 (gitignore)
    ├── pdfs/    golden/    samples/
```

## 📏 규모 요약

- 📄 **116 files / 36 dirs**
- 📚 14개 일자별 커리큘럼 문서
- 🔗 `links-classified.md`: 사용자 제공 ~150개 링크 전부 분류 + WebFetch 요약
- 💻 13개 프로젝트 스타터 코드
- 🧰 공통 Python 패키지 (`ai_study.*`)
- 🐳 Docker compose (Qdrant + Langfuse self-host)
- 🛠 one-shot installer + verify

## 핵심 명령

```bash
make help              # 전체
make setup             # 최초 1회
make verify            # API 점검
make qdrant-up         # Day 6+
make langfuse-up       # Day 12+
make infra-up          # 둘 다
make status            # 현재 상태
```

## 규칙

- 모르는 개념 → `notes/keywords.md` 즉시 추가
- 튜토리얼은 한 번만. 두 번째부터는 변형.
- API 키는 `.env`. 코드 하드코딩 금지.
- 매일 마지막 30분: 회고 + commit.
- 뒤처지면 `curriculum/recovery-playbook.md`로.
