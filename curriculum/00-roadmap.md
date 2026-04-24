# 14일 하드코어 LLM 엔지니어링 로드맵

하루 10시간+ 기준. 총 ~140시간.

## 전체 로드맵 (한눈에)

| Day | 주제 | 핵심 산출물 | 난이도 |
|---|---|---|---|
| 1 | LLM 기초 + 토크나이저 + Transformer 감각 | Google ML Crash Course LLM 완독 + 용어 정리 | ★ |
| 2 | 3대 Provider API 실전 (OpenAI/Anthropic/Gemini) | CLI 챗봇 3-provider 스위처 | ★★ |
| 3 | Prompt Engineering (Anthropic Interactive Tutorial 9챕터) | Prompt lab (패턴 10개 비교) | ★★ |
| 4 | Structured Output + Pydantic + JSON Schema | 이력서/PDF 정보 추출기 | ★★ |
| 5 | Function Calling / Tool Use (Anthropic tool_use 6강) | 멀티툴 에이전트 (weather+calc+web) | ★★★ |
| 6 | Embedding + Vector DB (Qdrant) | 의미 기반 검색 엔진 | ★★ |
| 7 | 기본 RAG (LangChain RAG From Scratch part 1-4) | PDF Q&A 봇 v1 | ★★★ |
| 8 | 고급 RAG (Query translation / Routing / Rerank / Hybrid) | PDF Q&A 봇 v2 (개선판) | ★★★★ |
| 9 | Eval (Ragas + OpenAI Evals) | RAG eval 파이프라인 | ★★★ |
| 10 | Agents (HF Agents Course unit 0-2) + LangGraph | State machine 에이전트 | ★★★★ |
| 11 | MCP (Model Context Protocol) | 자체 MCP 서버 + Claude Desktop 연결 | ★★★ |
| 12 | Observability (Langfuse + Phoenix) + Production (rate limit, streaming, caching) | 기존 프로젝트에 tracing/cost 측정 추가 | ★★★ |
| 13 | Local LLM (Ollama + vLLM OpenAI-compat) | Ollama + Qwen/Llama RAG | ★★ |
| 14 | 최종 포트폴리오 프로젝트 완성 + 회고 | production-grade RAG+Agent 앱 | ★★★★★ |

## 주차별 학습 목표

### Week 1 (Day 1–7): Foundation + Retrieval 기반
**목표**: LLM API를 자유자재로 다루고 기본 RAG을 혼자 만들 수 있다.

- [ ] Transformer / Attention / Token / Context window 감각 장착
- [ ] OpenAI / Anthropic / Gemini 3사 API 실전 (동일 작업을 3개로 구현 가능)
- [ ] Prompt 패턴 10가지 숙지 (zero/few-shot, CoT, role, structured, XML, prefill 등)
- [ ] Pydantic으로 strict JSON 스키마 검증
- [ ] Tool use로 외부 함수 호출 구현
- [ ] Embedding 기반 semantic search 구현
- [ ] Qdrant로 기본 RAG 파이프라인 완성

### Week 2 (Day 8–14): 고급 / Production / Portfolio
**목표**: 실무 수준의 RAG + Agent 앱을 관측 가능한 형태로 배포할 수 있다.

- [ ] Query translation, HyDE, RAG-Fusion, reranking, hybrid search
- [ ] RAG 품질을 Ragas 등으로 객관적으로 측정
- [ ] LangGraph로 상태머신 에이전트 구축
- [ ] MCP 서버 작성 및 Claude Desktop 연동
- [ ] Langfuse로 trace/cost/latency 관측
- [ ] Ollama로 로컬 LLM 돌리고 OpenAI 클라이언트 재활용
- [ ] 최종 포트폴리오: RAG + Agent + MCP + Langfuse 통합

## 날짜별 공부 시간 배분 (하루 10시간 기준)

| 블록 | 시간 | 용도 |
|---|---|---|
| Morning | 3h | 공식문서/튜토리얼 읽기 (read-only) |
| Mid-morning | 2h | 예제 코드 따라치기 |
| Lunch | 1h | 휴식 |
| Afternoon | 3h | 본인 변형 과제 (그날의 프로젝트 디렉토리에 코드 작성) |
| Evening | 1.5h | 디버깅 + `notes/keywords.md` 업데이트 |
| Wrap | 0.5h | `notes/daily-log.md` 한 줄 회고 + git commit |

## 핵심 원칙

1. **공식 문서 우선** — 한국어 블로그 구글링 금지. 막힐 때만 보조.
2. **이론은 지연 로딩** — 논문은 2주차 이후. 지금은 Claude한테 요약 시키고 그림만.
3. **튜토리얼은 딱 1번** — 두 번째부터는 반드시 변형.
4. **실패를 로깅** — 안 된 이유, 뭘 바꿨더니 됐는지 `daily-log.md`에 쓴다.
5. **중복 자료는 스킵** — `resources/skip.md` 참고.
6. **모델 선택 기본값**:
   - 빠른 실험: `claude-haiku-4-5` 또는 `gpt-4o-mini` / `gemini-flash`
   - 품질 필요: `claude-sonnet-4-6` / `gpt-4o` / `gemini-pro`
   - Local: `qwen2.5:7b` 또는 `llama3.1:8b` (Ollama)

## 중단 시 복구 방법

- 어디까지 했는지 `notes/daily-log.md` 마지막 줄 확인
- 그날 프로젝트 디렉토리 `README.md`의 체크리스트 이어서
- 막힌 링크는 `resources/links-classified.md` 에서 대체 자료 찾기
