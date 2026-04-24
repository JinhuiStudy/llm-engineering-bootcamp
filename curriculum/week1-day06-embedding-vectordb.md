# Day 6 — Embedding + Vector DB (하드코어)

> **난이도**: ★★★ (원래 ★★에서 상향)
> **총량**: 읽기 3.5h + 실습 5.5h + 정리 1h = 10h.
> **이정표**: "embedding이 의미를 벡터 공간에 매핑" → "Qdrant CRUD + HNSW 파라미터 튠 + quantization 트레이드오프 체감 + 한국어 임베딩 모델 선정"까지.

## 🎯 오늘 끝나면

1. Embedding 공간에서 "의미 가까움 = 벡터 가까움" 직관 → 실측
2. **Cosine / Dot product / L2**의 사용 기준 설명 (정규화된 embedding + cosine = 표준)
3. Qdrant로 collection CRUD + filter + HNSW 파라미터(`m`, `ef_construct`, `ef_search`) 손으로 튜닝
4. **Chunk size / overlap의 영향을 수치로**: top-k 정확도 vs chunk size 곡선
5. **한국어 vs 영어 multilingual 임베딩 성능 차이** 실측 (한국어 문서에는 OpenAI text-embedding-3보다 multilingual-e5-large가 강할 수 있음)
6. **Quantization** 3단계(float32 / scalar int8 / binary) 저장공간·검색속도·recall 트레이드오프 체감

## 📚 자료

### 🔥 필수

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 45m | [OpenAI — Embeddings guide](https://platform.openai.com/docs/guides/embeddings) | `text-embedding-3-small/large`. `dimensions` 파라미터로 차원 줄이기(Matryoshka) 가능. 1536 → 256으로 줄여도 큰 손해 없음. 비용 1M 토큰당 ~$0.02 (small). |
| 30m | [Gemini — Embeddings](https://ai.google.dev/gemini-api/docs/embeddings) | `gemini-embedding-001` 또는 `text-embedding-004`. `task_type` 파라미터(RETRIEVAL_QUERY, RETRIEVAL_DOCUMENT, SEMANTIC_SIMILARITY) 중요 — 같은 텍스트도 쿼리/문서에 다른 벡터. |
| 30m | [Voyage AI docs](https://docs.voyageai.com/) | Anthropic 공식 권장 임베딩. `voyage-3-large`가 MTEB 상위. Claude 앱에 잘 맞음. |
| 45m | [Sentence-Transformers (SBERT) intro](https://www.sbert.net/) | 로컬 임베딩 라이브러리. `all-MiniLM-L6-v2` (빠름/384d), `all-mpnet-base-v2` (품질/768d), `BAAI/bge-large-en-v1.5`, `intfloat/multilingual-e5-large` (한국어) 등. |
| 1h | [Qdrant Quickstart](https://qdrant.tech/documentation/quickstart/) | Python client, collection 생성, upsert, search. distance metric 선택. |
| 30m | [Qdrant — HNSW indexing](https://qdrant.tech/documentation/concepts/indexing/) | HNSW 파라미터 `m`(연결도), `ef_construct`(build시 탐색), `ef`(search시 탐색). Recall/latency 튜닝 원리. |
| 30m | [Qdrant — Quantization](https://qdrant.tech/documentation/guides/quantization/) | Scalar(int8, 4배 절감) / Product Quantization(16배+) / Binary(32배) — recall 손실과 트레이드. 100k+ vectors부터 의미 있음. |
| 30m | [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) | 임베딩 모델 벤치마크. **Task 필터링**(Retrieval / Classification / STS)이 필수. 한국어 필터도 있음. |

### ⭐ 강력 권장

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 30m | [Qdrant — Vector search as a service tutorial](https://qdrant.tech/documentation/tutorials/) | RAG tutorial, filter, hybrid 진행용 링크 모음. |
| 30m | [Matryoshka Representation Learning (Kusupati 2022)](https://arxiv.org/abs/2205.13147) | "1 임베딩에 여러 차원 동시 포함" — 앞 256차원만 써도 유효. `text-embedding-3`이 이걸 채택한 배경. |
| 20m | [Pinecone Learn — What is a vector database](https://www.pinecone.io/learn/vector-database/) | 개념 다이어그램. |
| 20m | [Qdrant blog — Storage optimization](https://qdrant.tech/articles/memory-consumption/) | on-disk vs in-memory, 언제 어떻게 고르는지. |

### 🎓 선택

- [FAISS tutorial](https://github.com/facebookresearch/faiss/wiki/Getting-started) — 라이브러리 수준 대안.
- [pgvector docs](https://github.com/pgvector/pgvector) — Postgres 쓰고 있으면 선택지.
- [LanceDB](https://lancedb.github.io/lancedb/) — embedded serverless.

## 🔬 실습 (5.5h)

### 프로젝트: Semantic Search + 모델 대결

위치: `projects/day05-embedding-search/`

```
day05-embedding-search/
├── docker-compose.yml        # Qdrant (infra/qdrant/ 재사용 가능)
├── ingest.py                 # 문서 → chunk → embed → upsert
├── search.py                 # 쿼리 → embed → search + 결과 포맷
├── compare_models.py         # 3사 API + 2개 로컬 모델 = 5개 embedding 대결
├── tuning/
│   ├── chunk_grid.py         # chunk size × overlap × strategy 그리드
│   ├── hnsw_tuning.py        # m × ef_construct × ef 변경하며 recall/latency
│   └── quantization.py       # float32 vs int8 vs binary 비교
├── data/
│   ├── ko/                   # 한국어 기술 블로그/문서 30개
│   └── en/                   # 영어 문서 30개
├── eval/
│   ├── queries.json          # 60개 쿼리 + expected relevant doc ids
│   └── run.py                # recall@k, MRR, nDCG 계산
└── README.md
```

### 🔥 필수 기능

1. **Qdrant 로컬** — `docker-compose up -d`. Dashboard (`http://localhost:6333/dashboard`) 접속
2. **5개 임베딩 모델 대결**:
   - OpenAI `text-embedding-3-small` (1536d, 다국어 중간)
   - OpenAI `text-embedding-3-large` with `dimensions=1024` (Matryoshka)
   - Voyage `voyage-3-large` or `voyage-3-lite`
   - 로컬 `intfloat/multilingual-e5-large` (1024d, **한국어 강함**)
   - 로컬 `BAAI/bge-m3` (1024d, dense+sparse 둘 다 출력)
3. **Chunking 전략 3종 비교**:
   - Fixed token (e.g. 500)
   - Recursive character (LangChain `RecursiveCharacterTextSplitter`)
   - Semantic (SBERT의 문장 단위 → 클러스터)
4. **Overlap 0 / 50 / 200** 3단계
5. **Eval 파이프라인** — 60개 쿼리 × {chunk × overlap × model} 매트릭스 → recall@5, MRR, nDCG@10 계산
6. **Filter metadata** — 문서 언어/카테고리/날짜로 필터링
7. **HNSW 튜닝** — `m=16, ef_construct=100, ef=64` 기본에서 조정 → recall vs search latency 곡선 그리기
8. **Quantization 실험** — same index에서 scalar int8 적용 후 recall 변동 측정

### 💎 실전 팁

- **E5 계열은 prefix 필수**: 쿼리에 `"query: "`, 문서에 `"passage: "` — 이거 안 붙이면 성능 20% 떨어짐.
- **BGE-M3는 dense + sparse + colbert 3가지** 출력. Day 8 hybrid에서 재등장.
- **OpenAI embedding은 L2-normalize 되어서 반환** → cosine = dot product.
- **한국어 조사 처리**: 일부 모델은 "파이썬이", "파이썬을"을 다르게 인식. 전처리 불필요한 게 보통.
- **Matryoshka 차원 자르기**: `text-embedding-3-large`는 `dimensions=512`로 잘라도 품질 97% 유지. 저장 3배 절감.

### 🔥 Stretch

- 🧪 **Semantic chunking** — [LangChain SemanticChunker](https://python.langchain.com/docs/how_to/semantic-chunker/) 로 문장 간 임베딩 유사도 급변 지점을 chunk 경계로.
- 🧪 **Hypothetical Question 증강** — 각 chunk에 대해 LLM이 "이 chunk가 답하는 질문 3개"를 생성 → 질문도 임베딩해서 인덱스에 추가 → query-question 매칭으로 검색 품질 ↑
- 🧪 **Parent-Child 구조** — chunk 100토큰으로 저장하되 parent는 500토큰 원문 — retrieval은 작게, LLM에게는 크게.
- 🧪 **Distance metric 비교** — 동일 벡터에 대해 Cosine / Dot / Euclidean 돌려서 top-k 순서 차이 관찰 (L2-normalized면 동등).
- 🧪 **On-disk mode** — 1M+ 벡터 실험해보고 싶으면 `on_disk=True`로 메모리 절감 실증.

## ⚖️ 수치 기준 (넘겨야 할 선)

| 메트릭 | 나쁨 | 보통 | 좋음 |
|---|---|---|---|
| Recall@5 (한국어) | <0.5 | 0.6-0.7 | >0.8 |
| 1 query 검색 latency (10k docs) | >200ms | 50-200ms | <50ms |
| Ingest 처리율 | <50 chunks/s | 50-200 | >200 |
| Quantization recall 손실 | >10% | 3-10% | <3% |

## ✅ 체크리스트

- [ ] Qdrant Dashboard에서 collection 상태 눈으로 확인
- [ ] 5개 모델 × chunk 설정 grid 결과 표 (`results/matrix.md`)
- [ ] 한국어에서 `multilingual-e5-large` 가 OpenAI embedding보다 나은 쿼리 3개 이상 찾음
- [ ] 영어에서 OpenAI가 로컬보다 나은 쿼리 3개 이상 찾음
- [ ] HNSW `ef=16` vs `ef=256` 동일 쿼리 결과 차이 수치화
- [ ] Scalar quantization 적용 후 recall 손실 측정
- [ ] Filter (language="ko", category="backend") 쿼리 동작
- [ ] BM25 baseline(`rank_bm25`) 대비 embedding 강점/약점 쿼리 각 3개

## 🧨 자주 틀리는 개념

1. **"임베딩 모델 아무거나 바꿔도 됨"** — 바꾸면 **전체 인덱스 재생성** 필수. 차원/분포 다름. 프로덕션에서 embedding 모델 교체는 migration event.
2. **"Cosine이 항상 Dot product보다 낫다"** — 정규화만 되어 있으면 동등. 비정규화 벡터에 dot 쓰면 "길이가 긴 애 우선" 편향.
3. **"Chunk 크게 하면 맥락 많아서 좋다"** — 검색 정확도는 떨어짐. 500 토큰 근방이 sweet spot. 큰 맥락이 필요하면 parent-child 구조로.
4. **"L2 distance = Euclidean"** — 맞는데, cosine과 정규화된 벡터에서는 단조관계(monotonic). 순서는 같음.
5. **"MTEB 1등 모델이 내 태스크에 최고"** — MTEB는 평균. **한국어 + 도메인(예: 의료)**로 필터링해야 의미 있음.
6. **"Quantization 쓰면 무조건 빨라짐"** — 메모리 절감 + 캐시 유리는 맞지만, small index(<10k)에선 오히려 오버헤드. 100k+에서 의미.
7. **"HNSW는 튜닝 안 해도 됨"** — `ef`를 너무 낮추면 recall 급락, 높이면 latency 급등. 데이터 사이즈 따라 다름.

## 🧪 산출물

- `projects/day05-embedding-search/` — 전체
- `results/matrix.md` — 모델 × chunk × overlap × 메트릭 표
- `notes/concepts.md` — "내 데이터에 고른 임베딩 모델 + 이유 3줄"
- `cheatsheets/rag-patterns.md` — chunk 섹션에 본인 수치 반영

## 📌 핵심 키워드

- Dense vector / Sparse vector
- Cosine similarity / Dot product / L2 distance / Manhattan
- Embedding dimension (384 / 768 / 1024 / 1536 / 3072)
- Matryoshka Representation Learning (MRL)
- Task-specific embeddings (retrieval_query vs retrieval_document vs STS)
- Tokenizer 차이가 embedding에 주는 영향
- Qdrant: collection, point, payload, filter, distance
- HNSW: m (edge count), ef_construct, ef (search width), layer hierarchy
- IVF, PQ (Product Quantization), ScaNN (개념만)
- Scalar/Binary/Product quantization, recall-latency trade
- MTEB, task filter, language filter
- Chunking strategies: fixed / recursive / semantic / parent-child
- Overlap, stride
- BM25, TF-IDF (sparse baseline)
- Hybrid (Day 8)

## 🎁 내일(Day 7) 미리보기
오늘 semantic search에 LLM generation을 붙이면 RAG. LangChain RAG From Scratch Part 1-4 + 실제 PDF Q&A 봇.
