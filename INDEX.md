# 🎯 AI Study Bootcamp — 마스터 INDEX (v3 ULTRA)

2주 ULTRA 하드코어 LLM 엔지니어링 부트캠프.
**하루 12-14시간 × 14일 = ~170시간**. 논문 25편 + Fine-tune + Deploy + Vision + Voice + Multi-agent 전부 내포.

## 🏁 처음 들어온 경우 이 순서로

1. **이 파일 (INDEX.md)** — 구조 파악
2. [`README.md`](README.md) — 디렉토리 구조
3. [`setup/0-prerequisites.md`](setup/0-prerequisites.md) — Day 0 준비 (1-2시간)
4. [`setup/3-accounts-checklist.md`](setup/3-accounts-checklist.md) — 계정/결제 체크
5. `./setup/1-install.sh` 실행 → `make verify`
6. [`curriculum/00-roadmap.md`](curriculum/00-roadmap.md) — 14일 전체 로드맵
7. [`curriculum/week1-day01-llm-basics.md`](curriculum/week1-day01-llm-basics.md) — Day 1 출발

## 🗂 주요 디렉토리 링크

- **[`curriculum/`](curriculum/)** — 일자별 공부 플랜 (14개)
- **[`resources/links-classified.md`](resources/links-classified.md)** — 모든 자료 분류 + 요약 (단일 진실 소스)
- **[`projects/`](projects/)** — 일자별 실습 스켈레톤 (13개) + 최종 포트폴리오
- **[`shared/`](shared/)** — 공통 Python 패키지 (`ai_study.*`)
- **[`infra/`](infra/)** — Qdrant + Langfuse Docker Compose
- **[`notes/`](notes/)** — 개인 노트 (keywords, concepts, daily-log)
- **[`cheatsheets/`](cheatsheets/)** — 빠른 참조 (prompt, RAG, eval, API 비교)

## 📅 14일 일람

| Day | 주제 | 커리큘럼 | 실습 |
|---|---|---|---|
| 0 | 준비 | [`setup/0-prerequisites.md`](setup/0-prerequisites.md) | — |
| 1 | LLM 기초 | [week1-day01](curriculum/week1-day01-llm-basics.md) | [day01-chatbot-cli](projects/day01-chatbot-cli) |
| 2 | 3대 Provider API | [week1-day02](curriculum/week1-day02-api-providers.md) | [day01-chatbot-cli](projects/day01-chatbot-cli) |
| 3 | Prompt Engineering | [week1-day03](curriculum/week1-day03-prompt-engineering.md) | [day02-prompt-lab](projects/day02-prompt-lab) |
| 4 | Structured Output | [week1-day04](curriculum/week1-day04-structured-output.md) | [day03-structured-extractor](projects/day03-structured-extractor) |
| 5 | Function / Tool Use | [week1-day05](curriculum/week1-day05-function-calling.md) | [day04-tool-agent](projects/day04-tool-agent) |
| 6 | Embedding + Vector DB | [week1-day06](curriculum/week1-day06-embedding-vectordb.md) | [day05-embedding-search](projects/day05-embedding-search) |
| 7 | 기본 RAG | [week1-day07](curriculum/week1-day07-basic-rag.md) | [day06-basic-rag](projects/day06-basic-rag) |
| 8 | 고급 RAG | [week2-day08](curriculum/week2-day08-advanced-rag.md) | [day07-advanced-rag](projects/day07-advanced-rag) |
| 9 | Eval | [week2-day09](curriculum/week2-day09-eval.md) | [day08-rag-eval](projects/day08-rag-eval) |
| 10 | Agents + LangGraph | [week2-day10](curriculum/week2-day10-agents-langgraph.md) | [day09-langgraph-agent](projects/day09-langgraph-agent) |
| 11 | MCP | [week2-day11](curriculum/week2-day11-mcp.md) | [day10-mcp-server](projects/day10-mcp-server) |
| 12 | Observability + Prod | [week2-day12](curriculum/week2-day12-observability.md) | [day11-observability](projects/day11-observability) |
| 13 | Local LLM + RunPod | [week2-day13](curriculum/week2-day13-local-llm-runpod.md) | [day12-local-llm](projects/day12-local-llm) |
| 14 | 포트폴리오 | [week2-day14](curriculum/week2-day14-final-portfolio.md) | [final-portfolio](projects/final-portfolio) |
| +∞ | 확장 | [extras](curriculum/extras.md) | — |

## 🧭 자주 보는 문서

| 필요할 때 | 파일 |
|---|---|
| 프롬프트 패턴 비교 | [`cheatsheets/prompt-patterns.md`](cheatsheets/prompt-patterns.md) |
| RAG 설계/개선 | [`cheatsheets/rag-patterns.md`](cheatsheets/rag-patterns.md) |
| Eval 점수 해석 | [`cheatsheets/eval-metrics.md`](cheatsheets/eval-metrics.md) |
| 3사 API 문법 | [`cheatsheets/api-compare.md`](cheatsheets/api-compare.md) |
| **Agent 패턴** | [`cheatsheets/agent-patterns.md`](cheatsheets/agent-patterns.md) (신규 v2) |
| **Production 패턴** | [`cheatsheets/production-patterns.md`](cheatsheets/production-patterns.md) (신규 v2) |
| **MCP 서버** | [`cheatsheets/mcp-cheatsheet.md`](cheatsheets/mcp-cheatsheet.md) (신규 v2) |
| 용어 모름 | [`notes/keywords.md`](notes/keywords.md) |
| 일일 로그 | [`notes/daily-log.md`](notes/daily-log.md) |
| 시간 블록 계획 | [`curriculum/schedule.md`](curriculum/schedule.md) |
| 자가진단 | [`curriculum/self-check.md`](curriculum/self-check.md) |
| 뒤처졌을 때 | [`curriculum/recovery-playbook.md`](curriculum/recovery-playbook.md) |
| **Troubleshooting / FAQ** | [`curriculum/troubleshooting.md`](curriculum/troubleshooting.md) (신규 v2) |
| **Day 0 프리컬** | [`curriculum/day00-prep.md`](curriculum/day00-prep.md) (신규 v2) |
| **⭐ Pre-Digested 문서** | [`resources/pre-digested.md`](resources/pre-digested.md) (신규 v3.1 — 공식 문서 직접 fetch해서 뽑은 복붙 코드 + 2026 최신) |
| 큰 결정 기록 | [`notes/decisions.md`](notes/decisions.md) |

## 🔧 자주 쓰는 명령

```bash
make help              # 전체 커맨드
make setup             # 최초 1회
make verify            # API 연결 점검
make qdrant-up         # Day 6+
make langfuse-up       # Day 12+
make infra-up          # 둘 다
make status            # 현재 상태 요약
```

## 🎯 최종 산출물

**Devlog RAG Copilot** — Day 14까지 나올 것:
- 공개 GitHub 레포 1개
- Multi-provider RAG + LangGraph Agent + MCP server + Langfuse 관측 + Ragas eval 통과
- README에 아키텍처 다이어그램 + 데모 gif + 평가 점수

## 📌 마인드셋

1. **공식 문서 우선.** 블로그 구글링은 2순위.
2. **튜토리얼은 한 번만.** 두 번째는 반드시 변형.
3. **숫자로 말한다.** Eval 없는 개선은 미신.
4. **실패를 로그한다.** 안 된 이유, 뭘 바꿨더니 됐는지 매일 기록.
5. **완벽 대신 완료.** 내 코드가 완벽하지 않아도 14일 안에 돌아가는 게 먼저.

## 🔥 v3.1 Pre-Digested 추가 (최신)

- **NEW: [`resources/pre-digested.md`](resources/pre-digested.md)** — 14 Day의 공식 문서를 **직접 WebFetch**로 열어 소화한 문서:
  - 2026-04 도메인 이전 (Anthropic → platform.claude.com, Cookbook → developers.openai.com, LangGraph → docs.langchain.com)
  - **Claude 4.7/4.6/4.5 모델명 확정** + 새 tool types (web_search_20260209 등)
  - **Gemini 3-flash-preview** 등장 (2.5 업그레이드)
  - **복붙 가능 코드**: Qdrant quickstart / LangGraph StateGraph / Langfuse @observe / Anthropic Prompt Caching 완전판 (cache_control syntax + 4096 토큰 최소값 per model) / Contextual Retrieval 공식 numbers + prompt template / OpenAI Structured Output parse / Modal FastAPI / Unsloth LoRA pattern
  - **논문 25편 배치** + Claude 요약 프롬프트 템플릿
- Day 0 프리컬에서 바로 이 문서로 안내

## 🚀 v3 ULTRA 업그레이드 요약

- **하루 10h → 12-14h**, 총 170h / 14일. 모든 extras 주제를 2주 안에 통합
- **새 주제 7영역 추가**:
  - Day 3: **OWASP LLM Top 10 + Llama Prompt-Guard 2**
  - Day 7: **Vision / Multi-modal RAG** (표/차트/스캔 PDF)
  - Day 9: **Multi-agent 3 프레임 비교** (LangGraph Supervisor / CrewAI / Swarm)
  - Day 10: **Voice input** (Whisper + Realtime API)
  - Day 11: **Batch API + Guardrails 3겹** (Prompt-Guard/NeMo/LlamaFirewall)
  - Day 12: **Deployment** (Modal/Fly.io/Docker/K8s basics)
  - Day 13: **Fine-tuning 전일** (LoRA/QLoRA/DPO with Unsloth on RunPod GPU)
  - Day 14: **Advanced Topics Rapid Fire** (MoE / Speculative / FlashAttention / Distillation / 분산 훈련 / Long-context) + 5편 논문
- **논문 25편** Figure 수준 배치 (Day 1-14)
- **self-check.md 3단**: 기본 / 심화 / v3 ULTRA
- **schedule.md 12-14h 블록** + Day 13/14 극한 모드
- 최종 산출물: "**Devlog RAG Copilot ULTRA**" — Vision + Voice + Multi-agent + Fine-tuned + Guardrails + Deployed (Modal public URL)

## 🔥 v2 업그레이드 (이전 단계)

- **14 Day 커리큘럼 전면 재작성** — 난이도 ★ 1-2개씩 상향, 각 자료에 "한 줄 요약" 컬럼, 수치 기준 표, 실전 함정 7-10개, Stretch 과제 확장
- **3개 치트시트 신규**: agent-patterns / production-patterns / mcp-cheatsheet
- **self-check.md 심화 질문 추가**
- 2026-04 기준 최신 모델/기법 반영
