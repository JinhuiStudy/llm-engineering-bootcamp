# 일자별 자가진단 (Self-Check)

각 Day 끝에 이 질문들에 **남의 설명 없이** 답할 수 있어야 한다.
답 안 나오면 그 개념은 다음 날 재학습.

## Day 1 — LLM 기초
- [ ] "LLM은 다음 토큰 확률을 예측한다"를 한 문장으로 엔지니어 동료에게 설명
- [ ] Token과 단어의 차이를 한국어/영어 예시로 설명
- [ ] Context window가 부족하면 어떤 증상이 나타나나?
- [ ] Temperature 0.0과 1.2의 행동 차이를 설명
- [ ] Self-attention이 왜 RNN을 대체했나 (1문장)
- [ ] 3사 기본 모델(4o-mini / Haiku / Flash)의 포지션 차이?

## Day 2 — API
- [ ] Anthropic의 `system`이 어디 붙고 OpenAI와 어떻게 다른가
- [ ] 3사 streaming 객체 구조 차이를 한 가지씩
- [ ] 401/403/429 각각 무엇이고 대응 방식은?
- [ ] `max_tokens` 너무 작으면? 너무 크면?
- [ ] 본인 CLI 챗봇에 `--provider openai` / `anthropic` / `gemini` 가 동일 결과를 내는가?

## Day 3 — Prompt Engineering
- [ ] Zero-shot / Few-shot / CoT 중 언제 뭘 쓰는지
- [ ] Prefill이 왜 Anthropic에서만 되는지
- [ ] XML 태그가 프롬프트 정확도에 어떻게 영향
- [ ] Self-critique를 production에 무조건 쓰면 안 되는 이유
- [ ] "Don't include markdown"과 "Output plain text only"의 차이

## Day 4 — Structured Output
- [ ] `response_format={"type":"json_schema", "strict": true}` 가 약속하는 것
- [ ] Pydantic v2의 `model_validate` vs `model_validate_json`
- [ ] Claude에서 structured output을 tool_use 트릭으로 하는 이유와 한계
- [ ] `Optional[X]` 필드가 LLM에 없으면 기본값 어떻게 주나
- [ ] Schema validation 실패 시 어떤 재시도 전략을 썼나 (본인 코드 기준)

## Day 5 — Function / Tool Use
- [ ] 3사 tool 정의 포맷 차이 3가지
- [ ] Parallel tool calling이 발생하는 조건
- [ ] `tool_choice: any` vs `tool_choice: {"type": "tool", "name": "x"}` 차이
- [ ] Tool이 에러를 내면 agent가 어떻게 회복해야 하나
- [ ] 무한 루프 방어 방법 3가지

## Day 6 — Embedding / Vector DB
- [ ] Embedding 차원 (1536 vs 384)이 실무에 주는 영향
- [ ] Cosine vs Dot product 언제 뭘 쓰나
- [ ] Chunk 200 / 500 / 1000 의 실측 차이 (본인 관찰 기반)
- [ ] Qdrant collection의 `distance` 설정을 바꿨을 때 기존 데이터는?
- [ ] BM25가 embedding보다 나은 전형적 케이스 1개

## Day 7 — RAG 기본
- [ ] RAG 7단계 flow를 종이에 그려라
- [ ] "근거 없으면 모른다고 답해라" 프롬프트의 효과
- [ ] 출처 인용 (citation) 동작 원리
- [ ] LangChain Document vs LlamaIndex Node 차이
- [ ] Hallucination이 여전히 일어나는 케이스 2개와 이유

## Day 8 — 고급 RAG
- [ ] HyDE가 언제 역효과인가
- [ ] Reranker 넣기 전/후 top-1 정확도 변화 (본인 숫자)
- [ ] RRF의 공식 `1/(k+rank)` 의 의미
- [ ] Multi-query로 top-k를 늘리는 것과 단일 query k=20의 차이
- [ ] Parent document retriever가 chunk size 딜레마를 어떻게 푸는가

## Day 9 — Eval
- [ ] Faithfulness와 Answer Relevancy 차이
- [ ] Context Precision과 Recall이 트레이드오프인가?
- [ ] LLM-as-a-judge의 positional bias 어떻게 완화
- [ ] 정답셋이 20 → 200으로 늘 때 기대되는 분산 변화
- [ ] A/B 비교에서 통계적으로 의미 있으려면 몇 개 필요?

## Day 10 — Agents / LangGraph
- [ ] ReAct의 "thought → action → observation" 순환의 각 단계 역할
- [ ] LangGraph `conditional_edges`가 if/else와 다른 점
- [ ] Checkpointing이 왜 production agent에 필수
- [ ] Reflection 루프의 비용/효용 트레이드오프
- [ ] Multi-agent (supervisor)가 single-agent보다 나은 케이스

## Day 11 — MCP
- [ ] MCP와 OpenAI function calling 차이 (힌트: 표준 vs 호출 규약)
- [ ] Tools / Resources / Prompts 세 primitives 각각 언제?
- [ ] stdio vs SSE transport 각각의 사용 상황
- [ ] Sampling (서버가 호스트 LLM 역호출) 위험성
- [ ] 본인 MCP 서버를 Claude Desktop에 연결했을 때 로그 어디에 찍히나

## Day 12 — Observability / Production
- [ ] Trace / Span / Observation 용어 구분
- [ ] TTFT와 완료 시간의 체감 차이
- [ ] Anthropic prompt caching에서 `cache_creation_input_tokens` vs `cache_read_input_tokens`
- [ ] Exponential backoff + jitter에서 jitter가 왜 필요
- [ ] Circuit breaker를 언제 열고 언제 닫아야?

## Day 13 — Local LLM / RunPod
- [ ] Ollama `base_url`을 OpenAI SDK에 주입하는 방법
- [ ] PagedAttention의 "페이지"가 뜻하는 것
- [ ] GGUF Q4_K_M의 "Q4", "K", "M" 각각 의미
- [ ] Serverless GPU의 cold start가 체감에 어떻게 영향
- [ ] 월 $X 이상일 때 API → self-host 전환을 본인 기준으로

## Day 14 — 포트폴리오
- [ ] 본인 아키텍처를 30초에 설명
- [ ] 가장 큰 한계와 그 이유
- [ ] Eval 점수 근거
- [ ] 같은 프로젝트를 다시 한다면 1순위로 바꿀 것
- [ ] 실무에 바로 적용할 3가지

---

## 재학습 규칙

- 3개 이상 답 못하면 → 다음 날 오전 읽기 블록에 그 Day 자료 재방문
- 모든 Day에 답 가능 = 14일 부트캠프 성공
