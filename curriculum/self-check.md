# 일자별 자가진단 (Self-Check v2)

> 각 Day 끝에 이 질문들에 **남의 설명 없이** 답할 수 있어야 한다. 답 안 나오면 그 개념은 다음 날 오전 읽기 블록에 재학습.
> v2에서 난이도 ↑ — 각 Day에 "심화 질문" 2-3개 추가.

## Day 1 — LLM 기초

**기본**
- [ ] "LLM은 다음 토큰 **확률 분포**를 예측한다"를 한 문장으로
- [ ] Token과 단어/글자의 차이를 한국어/영어 예시로
- [ ] Context window가 부족하면 나타나는 증상 3가지
- [ ] Temperature 0 / 1 / 2 각각의 분포 변화 (logit을 T로 나누는 의미)
- [ ] Self-attention이 RNN을 대체한 수치 근거 3가지 (병렬화 / long-range / gradient)

**심화 ⬆**
- [ ] 같은 한국어 문장의 cl100k vs o200k 토큰 수 차이 (본인 실측)
- [ ] Temperature 0인데도 출력이 미세히 다를 수 있는 이유
- [ ] KV cache가 context 길어짐에 따라 메모리를 어떻게 쓰는지 (prefill vs decode 단계)
- [ ] Lost in the Middle 현상을 경험했나? (Day 7 이후에도 체크)

## Day 2 — API

**기본**
- [ ] Anthropic `system` 위치 vs OpenAI / Gemini
- [ ] 3사 streaming 이벤트 구조 차이 (chunk / event 구분 / generator)
- [ ] 401 / 403 / 429 / 529 대응 방식
- [ ] `max_tokens` 너무 작 / 너무 큼 문제
- [ ] 3사 Usage 객체 필드명

**심화 ⬆**
- [ ] OpenAI `Chat Completions` vs `Responses API` 차이 3가지 + 언제 뭘 쓰나
- [ ] Anthropic `stop_reason` 각 값이 의미하는 것
- [ ] Gemini `SAFETY` finish 재현 조건 + 완화
- [ ] Streaming에서 usage 받으려면? (3사 각자)
- [ ] Tenacity `wait_random_exponential`가 `wait_exponential`보다 나은 이유 (jitter)

## Day 3 — Prompt Engineering

**기본**
- [ ] Zero-shot / Few-shot / CoT 언제 뭐 쓰나
- [ ] Prefill이 Anthropic 전용인 이유
- [ ] XML tag가 Claude에서 특히 강한 이유
- [ ] Self-critique를 모든 호출에 넣으면 안 되는 이유
- [ ] "Don't include markdown" vs "Output plain text only"

**심화 ⬆**
- [ ] Prompt injection 4유형 + 각각의 방어
- [ ] Sandwich defense의 구체 구조
- [ ] CoT가 오히려 정확도 떨어뜨리는 태스크 예시
- [ ] Self-Consistency (N=5)와 단일 CoT의 비용/정확도 트레이드

## Day 4 — Structured Output

**기본**
- [ ] `strict: true`가 보장하는 것 + 제약 3가지
- [ ] Pydantic `model_validate` vs `model_validate_json`
- [ ] Anthropic tool_use 트릭으로 structured output 하는 이유
- [ ] `Optional[X]` strict mode에서 다루는 법
- [ ] Schema validation 실패 시 retry 전략

**심화 ⬆**
- [ ] `$ref` / `$defs`가 strict mode에서 문제되는 이유 + 해결
- [ ] Discriminated union을 3사에 먹이는 법
- [ ] Instructor의 `Partial[T]` 스트리밍이 실제 어떻게 동작
- [ ] Outlines의 grammar-constrained decoding은 API 모델에 왜 못 씀

## Day 5 — Function / Tool Use

**기본**
- [ ] 3사 tool 정의 포맷 차이 (파라미터명, 응답 경로)
- [ ] Parallel tool call 발생 조건 + 강제 불가
- [ ] `tool_choice: auto / any / specific` 차이
- [ ] Tool 에러 복구 패턴 (throw vs `is_error: true`)
- [ ] 무한 루프 방어 3가지

**심화 ⬆**
- [ ] Tool description 길이와 정확도 상관 (실측)
- [ ] Extended thinking + tool use에서 thinking block이 어디 오나
- [ ] OpenAI built-in tools (web_search/file_search/code_interpreter)를 언제 써야 하나
- [ ] Sandbox `..` / symlink 공격 차단 구체 코드

## Day 6 — Embedding / Vector DB

**기본**
- [ ] Embedding 차원 (384 vs 1024 vs 1536)의 실무 영향
- [ ] Cosine vs Dot product (정규화 전제)
- [ ] Chunk 200 / 500 / 1000 실측 차이
- [ ] Qdrant `distance` 바꿨을 때 기존 데이터
- [ ] BM25가 embedding보다 나은 케이스

**심화 ⬆**
- [ ] Matryoshka dimension 자르기 원리 + 한계
- [ ] E5 계열 prefix (`query:` / `passage:`) 필요한 이유
- [ ] HNSW `ef=16` vs `ef=256` recall/latency 트레이드
- [ ] Scalar vs Binary quantization recall 손실 패턴
- [ ] 한국어 쿼리에 OpenAI `text-embedding-3` vs `multilingual-e5-large` 실측 승자

## Day 7 — RAG 기본

**기본**
- [ ] RAG 7단계 flow
- [ ] "근거 없으면 모른다" 프롬프트 효과 (실측 수치)
- [ ] Citation 동작 원리
- [ ] LangChain Document vs LlamaIndex Node 차이
- [ ] Hallucination이 여전히 일어나는 2개 케이스

**심화 ⬆**
- [ ] `from_scratch` vs LangChain LCEL vs LlamaIndex 라인 수 / 가독성 / 유연성 비교
- [ ] Lost in the Middle 대응 context 배치 전략
- [ ] Pydantic Answer schema로 citation 강제했을 때 품질 변화
- [ ] Parent-child chunk 구조의 장단

## Day 8 — 고급 RAG

**기본**
- [ ] HyDE 언제 유용 / 언제 독
- [ ] Reranker 전후 top-1 정확도 (본인 숫자)
- [ ] RRF 공식 `1/(k+rank)` 의미 + `k=60` 관례
- [ ] Multi-query N=3 vs k=20 단일 쿼리
- [ ] Parent document retriever가 chunk size 딜레마 해결하는 방식

**심화 ⬆**
- [ ] Anthropic Contextual Retrieval의 49% 개선 재현도
- [ ] ColBERT late interaction의 장단 (저장 10배 vs 정확도)
- [ ] RAPTOR 트리 레벨별 검색 유용한 질문 유형
- [ ] CRAG(Corrective RAG)와 Self-RAG 차이
- [ ] 본인 pipeline "쓸만한 것 top3 + 버린 것 2" 근거

## Day 9 — Eval

**기본**
- [ ] Faithfulness vs Answer Relevancy 차이
- [ ] Context Precision / Recall 트레이드 실존 여부
- [ ] LLM-as-judge positional bias 완화
- [ ] 정답셋 20 → 200 분산 변화 기대
- [ ] A/B 비교 통계적 significance에 몇 개 필요

**심화 ⬆**
- [ ] Custom faithfulness 구현했을 때 Ragas와 오차
- [ ] Pairwise vs 절대평가 노이즈 차이 (본인 실험)
- [ ] CI threshold `faithfulness ≥ 0.85` 근거 (본인 데이터셋 기준)
- [ ] Cost vs quality Pareto에서 본인이 고른 point + 이유

## Day 10 — Agents / LangGraph

**기본**
- [ ] ReAct의 Thought/Action/Observation 각 단계
- [ ] LangGraph `conditional_edges`의 if/else와 다른 점
- [ ] Checkpointing이 production agent에 필수인 이유
- [ ] Reflection loop 비용/효용
- [ ] Multi-agent supervisor 유리 케이스

**심화 ⬆**
- [ ] Agent vs Workflow Anthropic 기준
- [ ] Interrupt_before로 HITL 구현 시 state 저장 위치
- [ ] Pydantic AI vs LangGraph 본인 선택 + 이유
- [ ] Streaming events 중 values/updates/messages 차이
- [ ] Token budget enforcement를 state에 어떻게 박는가

## Day 11 — MCP

**기본**
- [ ] MCP vs function calling 차이 (표준 vs 호출 규약)
- [ ] Tools / Resources / Prompts 언제 각각?
- [ ] stdio vs Streamable HTTP 사용 상황
- [ ] Sampling 위험성
- [ ] Claude Desktop 로그 위치

**심화 ⬆**
- [ ] JSON-RPC `initialize` handshake에서 오가는 capability
- [ ] MCP Inspector로 실시간 JSON-RPC 메시지 확인 경험
- [ ] Resource URI scheme 설계 원칙 (`notes://`, `db://` 등)
- [ ] MCP OAuth 2.1 flow 개요

## Day 12 — Observability / Production

**기본**
- [ ] Trace / Span / Observation 구분
- [ ] TTFT vs E2E latency 사용자 체감
- [ ] Anthropic `cache_creation_input_tokens` vs `cache_read_input_tokens`
- [ ] Backoff + jitter에서 jitter 필요한 이유
- [ ] Circuit breaker 상태 3개

**심화 ⬆**
- [ ] Prompt caching 3사 각각 적용 조건 (최소 prefix 토큰)
- [ ] Langfuse prompt versioning으로 hot swap 경험
- [ ] OpenTelemetry LLM semantic conventions 5가지 attribute
- [ ] Async batch send(Langfuse)의 app latency 영향
- [ ] 본인 앱 p50/p95/p99 측정값

## Day 13 — Local LLM / RunPod

**기본**
- [ ] Ollama `base_url` + OpenAI SDK 트릭
- [ ] PagedAttention의 "페이지" 의미
- [ ] GGUF Q4_K_M의 Q4 / K / M
- [ ] Serverless cold start 체감
- [ ] "월 $X 이상 self-host" 본인 기준선

**심화 ⬆**
- [ ] AWQ vs GPTQ vs GGUF 차이
- [ ] Continuous batching이 왜 throughput 10배인가
- [ ] Speculative decoding의 draft/target 구조
- [ ] 본인 데이터/쿼리에 `Qwen3-8B` vs `GPT-4o-mini` Ragas 점수 gap

## Day 14 — Portfolio

**기본**
- [ ] 본인 아키텍처 30초 설명
- [ ] 가장 큰 한계 1개
- [ ] Eval 점수 근거 (어떤 pipeline 고른 이유)
- [ ] 같은 프로젝트 다시 하면 1순위 개선점
- [ ] 실무에 바로 적용할 3가지

**심화 ⬆**
- [ ] CI mini-eval threshold가 실제로 PR 차단한 사례 (만들어보기)
- [ ] Multi-provider env switch 실제 한 번 해보기 (ollama ↔ runpod)
- [ ] Prompt caching 실제 비용 감소율 (전/후)
- [ ] 14일 중 과대/과소평가된 자료 1개씩
- [ ] 다음 2주 확장 계획 (extras.md 중 선택 3개)

---

## 재학습 규칙

- **기본 3개 이상 못 답** → 다음 날 오전 읽기 블록에 해당 Day 자료 재방문
- **심화 3개 이상 못 답** → 그 주 주말(토) 오후 2h 복습 블록 삽입
- 모든 Day 기본 + 심화 답 가능 = 14일 부트캠프 **만점 통과**

## 이 문서 자체 사용법

- 매일 밤 21:00 블록에 해당 Day 섹션 5분 안에 전부 체크
- 애매한 것은 바로 `notes/keywords.md` / `concepts.md`에 정리
- 체크 못 한 것은 `daily-log.md`에 "내일 복수"로 표시
