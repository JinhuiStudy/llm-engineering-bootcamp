# Day 6 — Semantic Search (5 임베딩 모델 × Qdrant 튜닝)

> **연결**: [`curriculum/week1-day06-embedding-vectordb.md`](../../curriculum/week1-day06-embedding-vectordb.md)
> **의존성**: Day 0 설치 완료, `infra/qdrant/docker-compose.yml` (또는 로컬 docker-compose)
> **다음**: Day 7 기본 RAG가 이 collection과 ingest 로직 재사용

## 🎯 이 프로젝트로

1. **5 임베딩 모델** (OpenAI 3-small / OpenAI 3-large@1024 / Voyage-3 / multilingual-e5-large / BGE-M3) 대결
2. **Chunk × overlap × strategy** 그리드 (3×3×3 = 27 조합) 실측
3. **HNSW 파라미터** `m / ef_construct / ef` sweep → recall/latency 곡선
4. **Quantization 3단계** (fp32 / scalar int8 / binary) 저장/속도/정확도
5. 한국어/영어 60 쿼리에 대해 **recall@5 / MRR / nDCG@10** 측정
6. Metadata filter + BM25 baseline과의 강점/약점 기록

## 📁 디렉토리

```
day05-embedding-search/
├── pyproject.toml
├── docker-compose.yml                # 또는 ../../infra/qdrant/docker-compose.yml 심볼릭
├── config.py
├── ingest.py                         # --model X --chunk-size N --overlap N
├── search.py                         # --model X "쿼리"
├── compare_models.py                 # 모든 조합 × 쿼리 벤치
├── embeddings/
│   ├── base.py                       # EmbeddingProvider Protocol
│   ├── openai_small.py
│   ├── openai_large_1024.py          # dimensions=1024 (Matryoshka)
│   ├── voyage.py                     # voyageai
│   ├── e5_multilingual.py            # sentence-transformers
│   └── bge_m3.py                     # FlagEmbedding — dense+sparse+colbert
├── chunking/
│   ├── fixed_token.py
│   ├── recursive_char.py             # LangChain RecursiveCharacterTextSplitter
│   └── semantic.py                   # sentence-level similarity boundaries
├── tuning/
│   ├── chunk_grid.py                 # 3 chunk × 3 overlap × 3 strategy
│   ├── hnsw_sweep.py                 # m × ef_construct × ef
│   └── quantization.py               # fp32 / int8 / binary
├── baselines/
│   └── bm25.py                       # rank_bm25 비교
├── data/
│   ├── ko/                           # 한국어 문서 30개 (자기 블로그/기술문서)
│   └── en/                           # 영어 30개
├── eval/
│   ├── queries.json                  # 60 쿼리 + expected relevant doc ids
│   ├── metrics.py                    # recall@k, MRR, nDCG
│   └── run.py
├── results/
│   └── matrix.md                     # 대결 결과
└── README.md
```

## 🚀 시작

```bash
cd projects/day05-embedding-search
uv sync
uv add qdrant-client openai voyageai sentence-transformers FlagEmbedding rank_bm25

# Qdrant
docker compose up -d
open http://localhost:6333/dashboard
```

## ✅ 필수 기능

### Embedding providers
- [ ] 5개 `EmbeddingProvider` 구현
- [ ] E5 모델 호출 시 **prefix 자동 주입** — 쿼리는 `"query: "`, 문서는 `"passage: "`
- [ ] BGE-M3는 `dense_vecs`, `lexical_weights`(sparse), `colbert_vecs` 셋 다 반환

### Ingest
- [ ] `ingest.py` — 문서 iterator → chunker → embedder → Qdrant upsert (batch 100)
- [ ] Metadata: `source`, `chunk_id`, `page`, `lang`, `chunker`, `embedder`, `chunk_size`, `overlap`
- [ ] Chunking strategy 3종 모두 호출 가능
- [ ] Qdrant collection은 `{model}_{chunk_strategy}_{size}_{overlap}` 이름으로 분리 (실험 격리)

### Search + Filter
- [ ] `search.py` — 쿼리 → 같은 embedder → `client.query_points(limit=top_k, query_filter=...)`
- [ ] Metadata filter (`lang == "ko"`, `chunker == "recursive"`)
- [ ] Score threshold 옵션

### Eval
- [ ] `queries.json` 60개 (30 한국어 + 30 영어). 각 쿼리마다 `relevant_doc_ids: list[str]`
- [ ] `metrics.py`:
  - recall@k (relevant ∩ retrieved / relevant)
  - MRR (첫 relevant의 역순위 평균)
  - nDCG@10
- [ ] `compare_models.py` 실행: 5 model × 27 chunking grid × 60 query

### HNSW sweep
- [ ] `hnsw_sweep.py`:
  - `m ∈ {8, 16, 32}`
  - `ef_construct ∈ {64, 100, 200}`
  - `ef ∈ {16, 64, 256}`
  - 같은 collection 데이터에 대해 쿼리 latency vs recall

### Quantization
- [ ] `quantization.py`:
  - `scalar` int8 (`quantization_config={"scalar": {"type": "int8"}}`)
  - `binary` (대규모에서만 의미)
  - 같은 쿼리에 대해 recall 손실 + latency 개선 측정

## 📊 수치 기준

| 메트릭 | 기준 |
|---|---|
| 한국어 recall@5 | ≥ 0.75 (multilingual-e5) |
| 영어 recall@5 | ≥ 0.80 (OpenAI 3-large) |
| HNSW `ef=64` latency | < 50ms (10k docs) |
| int8 quantization recall 손실 | < 5% |
| BM25 대비 dense 승률 (paraphrase 쿼리) | ≥ 70% |

## 🧨 실전 함정

1. **임베딩 모델 교체 시 같은 collection 재사용 불가** — dimension 다름, 의미 분포 다름. collection 재생성 필수
2. **E5 prefix 누락** — `query:` / `passage:` 안 붙이면 성능 20% 하락
3. **OpenAI `text-embedding-3`는 L2-normalized로 반환** — cosine = dot. 직접 정규화 금지
4. **Qdrant `distance` 선택 후 바꾸면 기존 데이터 무효** — 재생성
5. **Matryoshka `dimensions=256`** 사용 시 품질 97% 유지 실측. 무조건 1536 쓸 필요 없음
6. **한국어 조사 ("파이썬이" vs "파이썬을")** — 대부분 모델이 같은 벡터로 잘 매핑. 전처리 불필요
7. **Scalar quantization은 10k+ 벡터에서만 의미** — 1k에서는 overhead
8. **on-disk 모드** — `on_disk=True` 하면 메모리 절감 but latency ↑. 10M+에서 고려

## 🎁 Stretch

- 🧪 **Semantic chunking** — LangChain `SemanticChunker`로 문장간 유사도 급변 지점 자르기
- 🧪 **Hypothetical Question augmentation** — 각 chunk에 LLM이 "이 chunk가 답하는 질문 3개" 생성 → 같이 인덱싱
- 🧪 **Parent-Child 구조** — chunk 100 토큰 저장 / parent 500 토큰 retrieve 시 확장
- 🧪 **FAISS / LanceDB** 같은 대안으로 동일 데이터 벤치

## 🔗 다음에 쓰이는 곳

- Day 7: `ingest.py` + Qdrant collection 그대로 사용
- Day 8: hybrid retrieval (dense+BM25+RRF)에 dense 부분
- Day 14: `app/rag/ingest.py` 의 베이스
