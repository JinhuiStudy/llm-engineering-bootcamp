# 14일 하드코어 LLM 엔지니어링 로드맵 (v2 — 상향 조정)

> **8년차 소프트웨어 엔지니어 기준. 하루 10h+ × 14일 = ~140h.**
> **v1(초기) 대비 난이도 ★ 1-2개씩 상향**. 각 Day의 링크 자료에는 **한 줄 요약** 포함. "읽기만" 아니고 **측정 + 실전 함정 + 수치 기준**까지.

## 전체 로드맵 (한눈에)

| Day | 주제 | 핵심 산출물 | 난이도 |
|---|---|---|---|
| 1 | LLM 기초 + Tokenizer + Transformer 감각 + logprob | `tokens.py` 3사 토크나이저 비교 + `temperature_demo.py` sampling 그리드 + logprob 엔트로피 | ★★ |
| 2 | 3대 Provider API (OpenAI Responses/Chat, Anthropic, Gemini) + 재시도 + prompt caching 예고 | `ai_study.llm` Provider 추상화 + `--compare` 병렬 호출 | ★★★ |
| 3 | Prompt Engineering (9챕터) + Prompt Injection 방어 lab | 10+ 패턴 × 3 태스크 × 형식·비용 매트릭스 + injection 공격/방어 | ★★★★ |
| 4 | Structured Output (strict / Pydantic v2 / self-heal) | 3도메인 추출기 + strict vs non-strict 성공률 + field-level F1 | ★★★ |
| 5 | Function/Tool Use + 방어적 agent loop + parallel | 3사 tool adapter + safety rail + 10 시나리오 eval | ★★★★ |
| 6 | Embedding + Qdrant + Chunk/Quantization/HNSW 튜닝 | 5 임베딩 모델 × chunk 그리드, HNSW `ef` sweep, int8 양자화 | ★★★ |
| 7 | 기본 RAG + 프레임워크 3종 비교 | `from_scratch` + LangChain LCEL + LlamaIndex 3벌 구현, 정답셋 20+ | ★★★★ |
| 8 | 고급 RAG (Query Transform / Hybrid+RRF / Rerank / Contextual Retrieval / RAPTOR) | 6 pipeline 모듈화, 정답셋 30+ | ★★★★★ |
| 9 | Eval (Ragas 4대 + LLM-judge 편향 + CI gate + Cost vs Quality Pareto) | 6 pipeline leaderboard + CI threshold + failure pattern | ★★★★ |
| 10 | Agents + LangGraph (StateGraph / HITL / Checkpoint / Reflection) | classifier→planner→retriever→tool→reflector→finalizer agent | ★★★★★ |
| 11 | MCP Server (Tools/Resources/Prompts/Sampling) + 3 호스트 연동 | FastMCP 서버 + Claude Desktop/Code/Cursor 전체 등록 | ★★★★ |
| 12 | Observability (Langfuse self-host) + Production (retry/breaker/caching/streaming) | 전 노드 trace + Ragas score attach + 3사 cache 실측 | ★★★★ |
| 13 | Local LLM (Ollama + vLLM) + RunPod Serverless | 4 backend × 20 쿼리 벤치 + 양자화 비교 + decision matrix | ★★★ |
| 14 | Portfolio — Devlog RAG Copilot (GitHub 공개) | FastAPI+LangGraph+MCP+Langfuse+Ragas CI, docker-compose, MIT | ★★★★★ |

### 주차별 목표

#### Week 1 (Day 1–7): Foundation + Retrieval

- [ ] Transformer / Attention / KV cache / TTFT의 멘탈 모델
- [ ] 3사 API 실전 + Provider 추상화 모듈 1개 (`ai_study.llm`)
- [ ] Prompt 패턴 10+ 체화 + Injection 방어 실측
- [ ] Pydantic v2 strict JSON schema 3사 강제
- [ ] Tool use 방어적 agent loop (sandbox + safety rail)
- [ ] Embedding + Qdrant + HNSW/quantization 기본 튜닝 손맛
- [ ] 정답셋 20+ 건 수기 + 3 프레임워크로 RAG v1

#### Week 2 (Day 8–14): Advanced + Production + Portfolio

- [ ] Query Transform / Hybrid / Rerank / Contextual Retrieval 체계화 + Ragas로 **수치 기반 선정**
- [ ] LangGraph state machine (checkpoint + HITL + reflection loop)
- [ ] MCP 서버 4 primitives + 3 호스트 연동
- [ ] Langfuse trace + prompt versioning + score attach + 3사 prompt caching
- [ ] Self-host (Ollama / vLLM / RunPod) + 의사결정 기준
- [ ] 최종 **Devlog RAG Copilot** GitHub 공개 (CI + demo + eval threshold 통과)

## 날짜별 공부 시간 배분 (하루 10시간 기준, 재확인)

| 블록 | 시간 | 용도 |
|---|---|---|
| Morning read-only | 3h | 공식문서/튜토리얼 (키보드 손 놓기) |
| Tutorial 따라치기 | 2h | notebook 실행만, 변형 X |
| Lunch | 1h | 화면 밖 |
| Afternoon 본실습 | 3h | 프로젝트 디렉토리 변형 과제 |
| Evening debug + 키워드 | 1.5h | 막힌 거 + `notes/keywords.md` |
| Wrap | 0.5h | `daily-log.md` + commit |

> 수요일/목요일은 `schedule.md`의 호흡 고르기 모드로.

## 핵심 원칙 (v2 강화)

1. **공식 문서 우선** — 한국어 블로그 금지 기본, 막힐 때만 보조
2. **이론은 지연 로딩** — 논문은 **Figure + Abstract + Conclusion만**. 본문은 필요할 때
3. **튜토리얼은 딱 1번** — 두 번째는 변형. 같은 코드를 두 번 치는 건 시간 낭비
4. **실패 로깅** — 안 된 이유 + 뭘 바꿨더니 됐는지 `daily-log.md`에
5. **중복 자료 스킵** — `resources/skip.md` 참고
6. **Eval 없는 개선은 미신** — Day 9 이후 모든 "RAG 개선"은 수치로 증명
7. **비용 가드레일** — Day 12 caching + 모델 선택 규칙, 실수로 $수백 나갈 수 있음
8. **모델 선택 기본값** (2026-04 기준):
   - 빠른 실험: `claude-haiku-4-5` / `gpt-4o-mini` / `gemini-2.5-flash`
   - 품질 필요: `claude-sonnet-4-6` / `gpt-4o` / `gemini-2.5-pro`
   - Local dev: `qwen3:8b` (한국어) / `llama3.3:8b` / `gpt-oss:20b` (Ollama)
   - Self-host prod: `Qwen/Qwen3-8B-Instruct` AWQ on RunPod L4

## 중단 시 복구

- `notes/daily-log.md` 마지막 줄 확인 → 이어서
- 그날 프로젝트 `README.md` 체크리스트 이어가기
- 막힌 링크는 `resources/links-classified.md` 에 대체 자료
- 3일 이상 뒤처짐 → [`recovery-playbook.md`](recovery-playbook.md) C/D 모드

## 새롭게 추가된 내용 (v1 → v2 변화점)

- **각 Day 자료 표에 한 줄 요약 컬럼** — 링크만 있던 걸 요약까지
- **수치 기준** — Day별 "넘어야 할 선" 표 (faithfulness/TTFT/recall 등)
- **자주 틀리는 개념** 섹션 — 실전 함정 7-10개씩
- **Stretch 과제** 명시적 확장 — 하드 모드
- **프로덕션 주의** — 실무 직결 경고
- **2026년 4월 최신 모델/도구**: Claude Opus 4.7 / Sonnet 4.6 / Haiku 4.5, GPT-4o/Responses API, Gemini 2.5, Qwen3, RunPod Serverless vLLM, FastMCP, Contextual Retrieval, RAPTOR
