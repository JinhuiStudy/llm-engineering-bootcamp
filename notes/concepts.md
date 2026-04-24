# 개념 정리 노트

학습 중 직접 깨달은 것 / 헷갈렸던 것 / 모델 별 차이를 **본인 언어로** 정리한다.
초기에는 비어있음 — 매일 1-3개 채워나가기. 14일 끝에 40-60개 목표.

## 🔖 작성 규칙

1. **본인 언어**로 쓴다 — 문서 복붙 금지 (복붙하면 안 남음)
2. **1줄 요약** 먼저 — 이게 안 되면 아직 이해 안 된 것
3. **언제 쓰는가 / 언제 안 쓰는가** 둘 다
4. **자주 하는 실수** — 본인이 실제 한 실수 우선
5. **실제 코드 or 링크** — 이론만 적지 말고 본인 코드 경로
6. 길면 분할 — 각 개념 50줄 이하

## 📝 포맷 템플릿

```markdown
## <개념 이름>
- **한 줄 요약**:
- **언제 쓰는가**:
- **언제 안 쓰는가**:
- **자주 하는 실수**:
- **코드 / 링크**:
- **본인 실측**: (선택) 수치 기반 관찰
```

---

# 📚 샘플 엔트리 (학습하면서 본인 것으로 교체/추가)

## Structured Output
- **한 줄 요약**: JSON Schema를 LLM에 주입해 출력 구조를 100% 보장하는 것 (strict=true 때).
- **언제 쓰는가**: 파싱 실패가 치명적일 때 — DB 저장, 후속 tool 호출, API 응답
- **언제 안 쓰는가**: 자유 형식 에세이/요약 — 오히려 제약
- **자주 하는 실수**: `required` 빠짐 / enum 없이 자유 string / `additionalProperties` 빠뜨려 OpenAI strict 거부
- **코드**: `projects/day03-structured-extractor/schemas/resume.py`
- **본인 실측**: strict=true는 첫 호출에 schema compile로 +200ms 있지만 후속 호출엔 영향 없음. 성공률 99%+ (field-level)

## Chunk overlap
- **한 줄 요약**: chunk 간 겹침. overlap=0이면 경계에 걸친 답을 놓침, 너무 크면 중복/비용 증가
- **언제 쓰는가**: ingest 파이프라인 튜닝 표준 — 항상 10-20%
- **언제 안 쓰는가**: 문서가 완전히 독립 단락일 때 (FAQ 등)
- **자주 하는 실수**: 문장 중간 잘림 → RecursiveCharacterTextSplitter의 separators 튜닝 누락
- **본인 실측** (Day 6): overlap 0 vs 50 vs 200 → recall@5 0.62 / 0.71 / 0.73. 50에서 이득 급증, 200은 marginal

## Cosine vs Dot product
- **한 줄 요약**: L2-normalized 벡터에서는 수학적으로 동일. 정규화 안 된 벡터에서만 차이
- **언제 쓰는가**: OpenAI embedding은 이미 정규화됨 → 뭐 써도 OK. 속도는 dot이 약간 빠름
- **자주 하는 실수**: 비정규화 벡터에 dot 써서 "길이가 긴 애 우선" 편향
- **코드**: Qdrant `distance=Distance.COSINE` 기본

## HyDE (Hypothetical Document Embeddings)
- **한 줄 요약**: 가상의 답변을 LLM으로 먼저 생성해서 그걸로 검색. 쿼리 어휘와 문서 어휘 불일치 보정
- **언제 쓰는가**: 자연어 질문 vs 전문 용어 문서 (e.g. "이 약 먹으면 돼?" ↔ "acetaminophen contraindication")
- **언제 안 쓰는가**: factual numeric question — 가상 답변이 틀린 숫자 생성하면 오답 방향 유도
- **자주 하는 실수**: 모든 쿼리에 HyDE → latency 2배, 품질 변동
- **본인 실측** (Day 8): 용어 mismatch 쿼리 10건 중 7건 개선, factual 10건 중 3건 악화

## RRF (Reciprocal Rank Fusion)
- **한 줄 요약**: 여러 retrieval 결과의 rank 기반 병합. `score(d) = Σ 1/(k+rank)`, k=60 표준
- **언제 쓰는가**: Hybrid search (dense + sparse), Multi-query 병합
- **자주 하는 실수**: score scale 다른 리스트를 그냥 합산 — RRF는 rank만 씀
- **코드**: `projects/day07-advanced-rag/retrievers/hybrid.py`

## Prompt Caching (Anthropic)
- **한 줄 요약**: `cache_control: {"type":"ephemeral"}`로 prefix 5m/1h 캐시. 읽기 -90%, 쓰기 +25%
- **언제 쓰는가**: 긴 system prompt / RAG context prefix / long document Q&A
- **자주 하는 실수**:
  - prefix가 1024 토큰 미만 → 적용 안 됨 (아무 반응 없음)
  - cache_control 위치 잘못 — 캐시할 덩어리 **끝**에 마커
- **본인 실측** (Day 12): 5000 토큰 system에 적용 시 호출 2부터 cache_read_input_tokens=5000, 비용 85% 절감

## ReAct vs Plan-and-Execute
- **한 줄 요약**: ReAct는 매 턴 Thought→Action→Obs, PE는 전체 계획 먼저 → 실행
- **언제 쓰는가**:
  - ReAct: 작고 빠른 의사결정, tool 적음 (3-5개)
  - PE: 복잡한 multi-step, 중간 실패 시 replan
- **자주 하는 실수**: ReAct로 복잡한 태스크 → thought 길어져 토큰 폭발

## MCP vs Function Calling
- **한 줄 요약**: function calling은 **provider 내부 규약**, MCP는 **클라-서버 표준 프로토콜** (JSON-RPC)
- **언제 쓰는가**:
  - function calling: 단일 앱에서 내 tool만 쓸 때
  - MCP: Claude Desktop/Cursor 등 여러 호스트에 재사용, 또는 타사에 tool 노출
- **자주 하는 실수**: 둘을 같은 개념으로 혼동
- **코드**: `projects/day10-mcp-server/server.py`

## GGUF 양자화 레벨
- **한 줄 요약**: Q_{bits}_{K|_0}_{S|M|L} — Q4_K_M은 4-bit, K-quants, medium 손실
- **언제 쓰는가**:
  - Q4_K_M: 대부분 sweet spot (메모리 1/4, 품질 95%)
  - Q5_K_M: 품질 우선 (5-bit, 1/3.2)
  - Q8_0: fp16 근접 (1/2, 거의 손실 없음)
- **자주 하는 실수**: Q2/Q3는 일반 챗에 품질 무너짐
- **코드**: `projects/day12-local-llm/quantization/`

## TTFT vs tok/s
- **한 줄 요약**: TTFT = 첫 토큰까지 지연, tok/s = decoding 처리율
- **언제 쓰는가**:
  - 짧은 답변 UX: TTFT가 결정적
  - 긴 답변 UX: tok/s가 결정적
- **자주 하는 실수**: TTFT만 보고 선택 → 긴 답변에서 슬로우
- **본인 실측** (Day 12): Haiku TTFT 1.1s / 82 tok/s, 4o-mini TTFT 0.9s / 90 tok/s

---

# 🎯 Day별 최소 1개 권장

- Day 1: Token, Context window, Temperature 중 1개
- Day 2: Streaming SSE, stop_reason 차이
- Day 3: 본인이 고른 최고 prompt 패턴 + 이유
- Day 4: strict mode의 제약 1가지 본인 경험
- Day 5: tool_choice 3모드 사용 상황
- Day 6: 본인 데이터에서 이긴 임베딩 모델
- Day 7: RAG 7단계 중 가장 품질 좌우한 단계
- Day 8: 가장 효과 큰 고급 기법 1개 + 수치
- Day 9: Ragas 메트릭 중 본인에게 가장 유용한 것
- Day 10: Agent vs Workflow 기준
- Day 11: MCP 4 primitive 중 가장 강력했던 것
- Day 12: Prompt caching 비용 절감 실측
- Day 13: API vs Self-host 본인 기준선
- Day 14: 최종 아키텍처의 가장 까다로운 결정

14일 × 평균 3개 = **40-50개** 목표. `INDEX.md`에서 `cheatsheets/`로 연결되는 기준이 됨.
