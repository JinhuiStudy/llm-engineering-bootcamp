# Day 8 — 고급 RAG (Query Transform / Hybrid / Rerank / RAPTOR 맛보기)

> **난이도**: ★★★★★ (원래 ★★★★에서 상향 — Week 2 진짜 시작)
> **총량**: 읽기 4h + 실습 5.5h + 정리 0.5h = 10h.
> **철학**: 어제 v1은 "그럭저럭 동작". 오늘 v2는 **실측 숫자가 실제로 개선되는가**를 매 기법마다 검증한다. **Eval 없이 추가하는 기법은 미신.**

## 🎯 오늘 끝나면

1. Query transformation 3대장(**Rewrite / HyDE / Multi-query**) 각각의 장단 실험 후 선택
2. **Hybrid search** (BM25 + dense + RRF)를 Qdrant 또는 직접 구현
3. **Cross-encoder reranking** 전후 top-1 정확도 수치화 (보통 +10~25%)
4. **Logical / Semantic routing**으로 "어떤 subsystem으로 보낼지" 결정
5. **RAPTOR / ColBERT / Contextual Retrieval** 3대 신기법의 **개념**은 설명 가능, 한 개는 직접 돌려봄
6. 내일 Ragas eval에 쓸 "v1 / v2 / v2+rerank / v2+hybrid / 풀스택" 5-6개 구성을 동시에 돌릴 수 있는 모듈화된 코드

## 📚 자료

### 🔥 오늘의 메인 (3h)

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 3h | [RAG From Scratch — Part 5-14](https://github.com/langchain-ai/rag-from-scratch) | Part 5(Multi-Query) / 6(RAG-Fusion) / 7(Decomposition) / 8(Step-back) / 9(HyDE) / 10(Logical/Semantic Routing) / 11(Query Structuring) / 12(Multi-representation) / 13(RAPTOR) / 14(ColBERT). 각 notebook 실행 + 본인 프로젝트에 2-3개 이식. |

### 🔥 필수

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 30m | [Anthropic — Contextual Retrieval (blog)](https://www.anthropic.com/news/contextual-retrieval) | **2024년 9월 발표**. Chunk마다 LLM이 "이 chunk가 전체 문서에서 어느 부분인지" 설명 한 줄 추가해 임베딩. 실측 49% retrieval 실패 감소. 현대 RAG 표준. |
| 30m | [OpenAI Cookbook — Search reranking with cross-encoders](https://cookbook.openai.com/examples/search_reranking_with_cross-encoders) | BM25/dense 상위 50 → cross-encoder로 재정렬 → top-5. 코드 그대로 옮겨와도 됨. |
| 30m | [Qdrant — Hybrid queries](https://qdrant.tech/documentation/concepts/hybrid-queries/) | Qdrant에서 dense + sparse vector를 한 collection에 저장하고 `prefetch` + fusion RRF. **2024 버전에서 Qdrant 자체 지원**. |
| 30m | [SBERT — Cross-Encoders](https://www.sbert.net/examples/applications/cross-encoder/README.html) | `cross-encoder/ms-marco-MiniLM-L-6-v2` (22MB, 빠름) 또는 `ms-marco-MiniLM-L-12-v2` (더 정확). 사용법 30줄. |
| 30m | [Cohere Rerank API](https://docs.cohere.com/docs/rerank) | `rerank-english-v3.0` / `rerank-multilingual-v3.0`. 무료 trial 월 1000 queries. 로컬 cross-encoder보다 한국어 품질 좋음. |
| 30m | [RAPTOR paper](https://arxiv.org/abs/2401.18059) | Recursive abstraction tree. 문서를 계층적으로 클러스터링 후 요약 트리 → 검색 시 각 레벨에서 검색. 긴 문서에 강함. |

### ⭐ 강력 권장

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 30m | [ColBERT/ColBERTv2 개요](https://github.com/stanford-futuredata/ColBERT) | Token-level late interaction. 정확도 강력하지만 저장소 10배. BGE-M3의 colbert 벡터로 가볍게 체험 가능. |
| 30m | [LlamaIndex — Qdrant hybrid example](https://docs.llamaindex.ai/en/stable/examples/vector_stores/qdrant_hybrid/) | 실제 코드. BM25 sparse vectors + dense fusion. |
| 20m | [Weaviate — Hybrid search alpha 튜닝](https://weaviate.io/developers/weaviate/search/hybrid) | alpha 파라미터로 dense/sparse 비중 조절 직관. |
| 20m | [HuggingFace — cross-encoder 모델 카드](https://huggingface.co/cross-encoder) | 모델 카탈로그. 한국어 강한 건 `bongsoo/kpf-cross-encoder-v1` 등. |

### 🎓 선택

- [BGE-M3 paper](https://arxiv.org/abs/2402.03216) — dense / sparse / colbert 3 출력 단일 모델. 한국어도 지원. **Day 6에서 다룬 모델**, 오늘 본격 활용.
- [Corrective RAG (CRAG)](https://arxiv.org/abs/2401.15884) — retrieved chunk의 품질을 평가해 low면 web search fallback.
- [Self-RAG](https://arxiv.org/abs/2310.11511) — 모델이 스스로 "retrieve 필요" 판단. Adaptive retrieval.

## 🔬 실습 (5.5h)

### 프로젝트: PDF Q&A v2 (모듈화)

위치: `projects/day07-advanced-rag/` (Day 7에서 복사 후 확장)

```
day07-advanced-rag/
├── config.py                     # 구성 스위치 (Baseline / v2 / v2+rerank / ...)
├── pipelines/
│   ├── base.py                   # Pipeline ABC: query → answer + metadata
│   ├── baseline.py               # = Day 7 (dense only, no transform)
│   ├── v2_query_transform.py     # + rewrite / multi-query / HyDE
│   ├── v2_hybrid.py              # dense + BM25 + RRF
│   ├── v2_rerank.py              # + cross-encoder rerank
│   ├── v2_contextual.py          # Anthropic contextual retrieval
│   └── v2_full.py                # 모든 기법 조합
├── retrievers/
│   ├── dense.py
│   ├── sparse_bm25.py            # rank_bm25 or Qdrant sparse
│   ├── hybrid.py                 # RRF fusion
│   ├── reranker.py               # cross-encoder / Cohere
│   └── router.py                 # logical / semantic routing
├── query_transform/
│   ├── rewrite.py                # 구어체 → 검색용 쿼리
│   ├── hyde.py                   # 가상 답변 생성 → 임베딩
│   ├── multi_query.py            # 1 쿼리 → N 쿼리
│   ├── decompose.py              # 복합 → sub-question
│   └── step_back.py              # 구체 → 일반화
├── indexing/
│   ├── contextual_chunks.py      # Anthropic contextual retrieval 구현
│   └── raptor_tree.py            # (Stretch) RAPTOR 계층 클러스터
├── eval/
│   └── qa_pairs.json             # Day 7 것 그대로 + 30개로 확장
├── benchmark.py                  # 모든 파이프라인 × 정답셋 → 결과
└── README.md
```

### 🔥 필수 기능

1. **Query transform 3종**:
   - `rewrite.py`: LLM(Haiku/flash)로 구어체 → 검색용. "어 그거 뭐더라 Qdrant에서 점 추가할 때 쓰는 거" → "Qdrant collection upsert points API"
   - `hyde.py`: 가상의 답변을 LLM으로 생성 → 그 답변 임베딩으로 검색. 용어 mismatch 상황에 강함.
   - `multi_query.py`: 1 쿼리 → 3-5개 변형 → 각각 retrieval → RRF 병합.
2. **Hybrid search** — Qdrant sparse vector(`fastembed` or `splade`) + dense vector 같은 collection. `prefetch`로 각각 50건 → fusion RRF로 top-10.
3. **Cross-encoder rerank**:
   - `cross-encoder/ms-marco-MiniLM-L-6-v2` 로컬 (CPU도 충분)
   - Cohere Rerank API (한국어면 multilingual 권장)
   - top-50 → rerank → top-5
4. **Routing** — LLM(flash)로 쿼리 분류: "general" / "code" / "api_docs" → 각기 다른 collection으로
5. **Contextual retrieval** — 각 chunk에 대해 LLM으로 "이 chunk가 전체 문서에서 어느 부분인지 한 문장" 생성해 prepend → 임베딩 (Anthropic 방법, 실측 49% 개선)
6. **Benchmark harness** — 모든 pipeline × qa_pairs.json 자동 실행, latency + cost + retrieved chunks 저장 (내일 Ragas 입력)

### 🧠 RRF 공식 복기
`score(d) = Σ 1 / (k + rank_i(d))`. `k=60`이 표준. 서로 다른 랭킹 리스트를 rank 기반으로 병합 — score scale 무관.

### 🔥 Stretch

- 🧪 **RAPTOR 실구현** — 문서 chunks → GMM 클러스터링 → 각 클러스터 요약 → 상위 레벨 chunks → 다시 클러스터링 → 트리. 검색 시 모든 레벨 union.
- 🧪 **ColBERT via BGE-M3** — `bge-m3`의 colbert 벡터로 fine-grained matching. `FlagEmbedding` 패키지.
- 🧪 **Corrective RAG** — 각 retrieved chunk의 relevance를 LLM이 score → threshold 미달이면 Tavily/Brave로 web fallback.
- 🧪 **Self-RAG 맛보기** — 모델이 `<needs_retrieval>` 토큰 생성 시에만 retrieval. 간단한 분류 LLM으로 구현.
- 🧪 **Query-dependent chunk size** — 쿼리 유형(factual vs synthesis)에 따라 chunk 크기 선택.
- 🧪 **Metadata filter 자동 추출** — 사용자 쿼리에서 "2024년 이후" → `date_filter` 생성.

### 📏 수치 기준

Day 7 v1 대비 Day 8 v2가 넘어야 할 선:
| 메트릭 | v1 (어제) | v2 (오늘 목표) |
|---|---|---|
| Retrieve recall@5 | ~0.6 | >0.75 |
| Top-1 정답에 직접 근거 chunk 포함 | ~0.5 | >0.75 |
| Unanswerable 거절률 | ~0.6 | >0.8 |
| latency p50 (end-to-end) | ~3s | <4s (rerank 추가로 약간 ↑ OK) |
| 1 query 비용 | ~$0.002 | <$0.01 (multi-query + rerank 감안) |

**수치 안 오르면 그 기법은 버려라.** 오늘의 진짜 가치는 "뭘 더하느냐"가 아니라 "뭘 안 쓰느냐".

## ✅ 체크리스트

- [ ] RAG From Scratch Part 5-14 전부 실행 (14개 notebook)
- [ ] HyDE가 **도움 되는 케이스**와 **독이 되는 케이스** 각 3개 기록 (예: domain-specific 용어 O, factual numeric 질문 X)
- [ ] Cross-encoder rerank 전후 top-1 정확도 수치
- [ ] Hybrid search (dense+BM25+RRF) 동작 — 단일 dense 대비 쿼리 유형별 승률
- [ ] Multi-query k=3 vs single-query k=15 비교 (토큰 비용 포함)
- [ ] Anthropic Contextual Retrieval 1회 이상 시도 (비쌀 수 있으니 소량)
- [ ] `benchmark.py`로 5+ pipeline × 30+ 쿼리 매트릭스 저장
- [ ] `cheatsheets/rag-patterns.md` 본인 관찰 반영
- [ ] 정답셋 20 → 30+ 확장 (Day 9 eval 준비)

## 🧨 자주 틀리는 개념

1. **"HyDE는 언제나 좋다"** — factual에 약함. "2024년 OpenAI 매출이 얼마?" 같이 정답이 특정 숫자면 HyDE의 가상 답변이 오히려 오답 방향으로 검색 유도.
2. **"Multi-query 많을수록 좋다"** — N=3가 보통 sweet. N=10이면 redundant + 비용 폭발.
3. **"Rerank는 항상 더하면 됨"** — 맞는데, BM25+dense 조합에서만 진짜 큰 이득. Dense only는 이미 의미 정렬 잘 되어 있어 gap 작음.
4. **"Hybrid가 단일 dense보다 항상 낫다"** — 대체로 맞지만, **embedding이 좋고 도메인 vocab가 매치되는 경우** dense only가 더 나을 수도. BM25는 OOV(새 용어)에 강함.
5. **"RRF alpha는 0.5가 기본"** — RRF 자체는 alpha 없음 (`1/(k+rank)` 합). Weaviate의 `hybrid(alpha=0.5)`는 sparse/dense 가중치. 구분.
6. **"Query rewriting은 무조건 품질 ↑"** — LLM 호출 추가 비용 + latency + 가끔 원쿼리보다 안 좋게 바뀜. 짧고 명확한 쿼리는 그대로가 나음.
7. **"Routing은 오버엔지니어링"** — 도메인/collection 2개 이상이면 routing이 오히려 심플함 + 정확도 ↑.

## 🧪 산출물

- `projects/day07-advanced-rag/` — 6개 pipeline 모듈화
- `benchmark.py` 결과물 (CSV/JSONL) — 내일 Ragas 입력
- `eval/qa_pairs.json` — 30+ 건
- `cheatsheets/rag-patterns.md` — 본인 수치 반영
- `notes/concepts.md` — "HyDE 언제 독/약 / Rerank 언제 필수 / Hybrid의 승리조건"

## 📌 핵심 키워드

- Query rewriting, Query translation
- HyDE (Hypothetical Document Embeddings)
- Multi-query, Query expansion
- Sub-question decomposition
- Step-back prompting
- Logical routing, Semantic routing
- Query structuring (metadata filter extraction)
- BM25, TF-IDF, SPLADE (learned sparse)
- Hybrid search, RRF (Reciprocal Rank Fusion), weighted fusion
- Cross-encoder vs Bi-encoder, late interaction
- Reranking, ms-marco checkpoints, Cohere Rerank
- Anthropic Contextual Retrieval (2024)
- RAPTOR (recursive tree), ColBERT (late interaction)
- Parent Document / Small-to-Big
- Corrective RAG (CRAG), Self-RAG (adaptive retrieval)

## 🎁 내일(Day 9) 미리보기
오늘 만든 5-6개 pipeline에 대해 Ragas의 **faithfulness / answer_relevancy / context_precision / context_recall** 수치로 승부. "eval 없는 개선은 미신"을 몸으로 실감하는 날.
