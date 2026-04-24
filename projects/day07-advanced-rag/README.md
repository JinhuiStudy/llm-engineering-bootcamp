# Day 8 — 고급 RAG v2 (6 Pipeline 모듈화 + 정답셋 30+)

> **연결**: [`curriculum/week2-day08-advanced-rag.md`](../../curriculum/week2-day08-advanced-rag.md)
> **의존성**: Day 7 v1 (복사해서 시작), Day 6 Qdrant
> **다음**: Day 9 Ragas가 6 pipeline의 winner 결정

## 🎯 이 프로젝트로

1. **6개 pipeline 모듈화** — baseline / +rewrite / +hybrid / +rerank / +contextual / full
2. Query transform 3대장 (rewrite / HyDE / multi-query) 장단 실측
3. **Hybrid (dense + BM25 + RRF k=60)** 단일 dense 대비 승리 조건
4. Cross-encoder rerank 전후 top-1 정확도 (보통 +10-25%)
5. **Anthropic Contextual Retrieval** 재현 — 49% 개선?
6. 내일 Ragas 입력: 30+ 정답셋 × 6 pipeline × 4 metrics 벤치마크 JSON

## 📁 디렉토리

```
day07-advanced-rag/
├── pyproject.toml
├── config.py                       # Config dataclass: pipeline / embedder / reranker / k / etc.
├── pipelines/
│   ├── base.py                     # Pipeline ABC: query → Answer
│   ├── baseline.py                 # = Day 7 dense only
│   ├── v2_query_transform.py       # + rewrite + multi-query + HyDE (토글)
│   ├── v2_hybrid.py                # dense + BM25 + RRF
│   ├── v2_rerank.py                # + cross-encoder rerank
│   ├── v2_contextual.py            # Anthropic contextual (ingest 단계에서 chunk prepend)
│   └── v2_full.py                  # 모든 기법 조합
├── retrievers/
│   ├── dense.py
│   ├── sparse_bm25.py              # rank_bm25 or Qdrant sparse (SPLADE)
│   ├── hybrid.py                   # RRF fusion
│   └── reranker.py                 # cross-encoder/ms-marco-MiniLM-L-6-v2 or Cohere
├── query_transform/
│   ├── rewrite.py                  # 구어체 → 검색용
│   ├── hyde.py                     # 가상 답변 → 임베딩
│   ├── multi_query.py              # N=3 변형
│   ├── decompose.py                # 복합 → sub-question
│   └── step_back.py                # 구체 → 일반
├── indexing/
│   ├── contextual_chunks.py        # 각 chunk에 "이 chunk가 전체 문서의 어디" 한 줄 prepend
│   └── raptor_tree.py              # Stretch
├── routing/
│   └── router.py                   # logical/semantic routing (LLM 분류로 collection 선택)
├── benchmark.py                    # 모든 pipeline × queries × metrics (내일 Day 9 입력)
├── eval/
│   └── qa_pairs.json               # Day 7 20 + 10 추가 = 30+
└── README.md
```

## 🚀 시작

```bash
cp -r ../day06-basic-rag/* ./  # 복사로 시작
cd projects/day07-advanced-rag
uv sync
uv add sentence-transformers rank_bm25 cohere FlagEmbedding
```

## ✅ 필수 기능

### Pipeline 구조
- [ ] `pipelines/base.py`:
  ```python
  @dataclass
  class PipelineResult:
      answer: Answer
      retrieved: list[Chunk]
      metadata: dict  # tokens, latency, cost, steps
  
  class Pipeline(ABC):
      @abstractmethod
      async def run(self, question: str) -> PipelineResult: ...
  ```
- [ ] 모든 pipeline은 이 ABC 구현 → benchmark가 동일 인터페이스로 호출

### Query Transform
- [ ] `rewrite.py` — Haiku/flash로 구어체 → 검색 쿼리. "qdrant 점 추가 그거 뭐더라" → "Qdrant upsert points API method"
- [ ] `hyde.py` — 가상 답변 1개 생성 → 그걸로 임베딩 → search
- [ ] `multi_query.py` — 3개 변형 → 각각 search → RRF merge
- [ ] `step_back.py` — "구체적 질문의 상위 개념이 뭔가" → 상위 검색 후 구체 맥락 얹기

### Hybrid
- [ ] `sparse_bm25.py` — `rank_bm25.BM25Okapi` 로컬 or Qdrant sparse vector
- [ ] `hybrid.py`:
  ```python
  def rrf_fusion(results: list[list[Chunk]], k=60):
      scores = defaultdict(float)
      for result in results:
          for rank, chunk in enumerate(result):
              scores[chunk.id] += 1 / (k + rank)
      return sorted(scores, key=scores.get, reverse=True)
  ```
- [ ] dense top-50 + BM25 top-50 → RRF → top-10 → rerank

### Reranker
- [ ] Local `cross-encoder/ms-marco-MiniLM-L-6-v2` (CPU 충분) — 빠른 버전
- [ ] Cohere Rerank `rerank-multilingual-v3.0` (한국어 품질 우수)
- [ ] 토글: `config.reranker = "local" | "cohere" | None`

### Contextual Retrieval (Anthropic 2024-09)
- [ ] `indexing/contextual_chunks.py`:
  ```python
  # 각 chunk마다 prompt:
  # <document>{FULL_DOC}</document>
  # <chunk>{THIS_CHUNK}</chunk>
  # Explain in 1 sentence what this chunk is about within the document.
  context_sentence = haiku_call(...)
  indexed_text = context_sentence + "\n\n" + chunk.text
  embed(indexed_text)
  ```
- [ ] Anthropic cache_control로 `<document>` 프리픽스 캐시 → 비용 90% 절감
- [ ] baseline vs contextual 동일 쿼리 recall 비교

### Benchmark
- [ ] `benchmark.py`:
  - 모든 pipeline × 30 query
  - 각 (pipeline, query) → `PipelineResult` JSON 저장
  - `results/benchmark_YYYYMMDD.jsonl` — Day 9 Ragas 입력
  - latency / cost / tokens 메타 포함

## 📊 수치 기준 (Day 7 v1 대비)

| 메트릭 | v1 (Day 7) | v2 목표 (오늘) |
|---|---|---|
| recall@5 | ~0.6 | ≥ 0.75 |
| top-1에 근거 chunk 포함 | ~0.5 | ≥ 0.75 |
| Unanswerable 거절률 | ~0.6 | ≥ 0.80 |
| p50 latency | ~3s | ≤ 4s |
| $/query | ~$0.002 | ≤ $0.01 |

## 🧨 실전 함정

1. **HyDE가 factual 수치 질문에 독** — 가상 답변이 틀린 숫자 유도 → 잘못된 방향으로 검색
2. **Multi-query N=10** — redundant + 비용 5-10배. N=3 sweet
3. **Hybrid의 RRF k=60** 표준. k 작으면 top 우위, 크면 평평. 상황별
4. **Cross-encoder rerank가 안 먹힐 때** — 한국어에 영어 전용 MiniLM 쓰면. `bongsoo/kpf-cross-encoder-v1` 또는 Cohere multilingual
5. **Contextual Retrieval 비용** — document당 chunk 수만큼 haiku 호출. 대량이면 batch API or cache
6. **RAPTOR는 클러스터링 학습 시간** — 10k+ chunks에서 의미 있음. 작은 데이터에선 overhead
7. **Query rewriting이 원쿼리보다 안 좋을 때** — 짧고 명확한 쿼리는 그대로가 나음. 판별 Haiku 추가

## 🎁 Stretch

- 🧪 **RAPTOR** — chunks → GMM cluster → summarize → 상위 노드 → 재귀
- 🧪 **ColBERT via BGE-M3** — late interaction으로 fine-grained matching
- 🧪 **CRAG (Corrective RAG)** — chunk relevance LLM 판정 → low면 Tavily로 web fallback
- 🧪 **Self-RAG** — `<needs_retrieval>` 토큰 판정으로 adaptive retrieval
- 🧪 **Metadata filter 자동 추출** — 질문에서 "2024년 이후" → date_filter 자동 생성

## 🔗 다음에 쓰이는 곳

- Day 9: `benchmark.py` 결과 → Ragas evaluate → leaderboard
- Day 10: 최고 pipeline을 LangGraph `retriever` 노드로
- Day 14: `app/rag/pipelines/`
