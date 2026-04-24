# Day 6 — Embedding + Vector DB

## 목표
- Embedding이 "의미를 벡터 공간에 매핑"한다는 감각 확보
- Cosine similarity / dot product / L2 차이 이해
- Qdrant로 collection 만들고 CRUD + 검색 가능
- chunk size, overlap이 retrieval 품질에 미치는 영향 체감

## 자료

| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [OpenAI Embeddings guide](https://platform.openai.com/docs/guides/embeddings) | 1h |
| 필수 | [Gemini embeddings docs](https://ai.google.dev/gemini-api/docs/embeddings) | 0.5h |
| 필수 | [Sentence-Transformers (SBERT)](https://www.sbert.net/) — 로컬 embedding | 1h |
| 필수 | [Qdrant Quickstart](https://qdrant.tech/documentation/quickstart/) | 1h |
| 필수 | [Qdrant RAG tutorial](https://qdrant.tech/documentation/tutorials-build-essentials/rag-deepseek/) | 1h |
| 선택 | [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) — 모델 고를 때 참고 | 0.5h |
| 선택 | [Pinecone Learn — 개념 글 2-3개](https://www.pinecone.io/learn/) | 1h |

## 실습 (4h)

### 프로젝트: 의미 기반 검색 엔진
위치: `projects/day05-embedding-search/`

```
day05-embedding-search/
├── docker-compose.yml   # Qdrant 로컬
├── ingest.py            # 문서 → chunk → embed → Qdrant upsert
├── search.py            # 쿼리 → embed → similarity search
├── compare.py           # BM25 (keyword) vs embedding search 결과 비교
├── data/                # 실험용 문서 (자기 블로그 글/기술 문서 10-20개)
└── README.md
```

### 요구사항
1. Qdrant 로컬 실행 (`docker run -p 6333:6333 qdrant/qdrant`)
2. OpenAI `text-embedding-3-small`과 로컬 `sentence-transformers/all-MiniLM-L6-v2` 둘 다 해보기
3. Chunk size 200 / 500 / 1000 tokens로 각각 ingest → 검색 품질 비교
4. Overlap 0 / 50 / 200 tokens 비교
5. `search.py`에서 top-k=5, score threshold 실험
6. BM25 baseline (`rank_bm25` 패키지) 대비 embedding 검색의 강점/약점 기록

### Stretch
- Metadata filtering (카테고리별 필터)
- 한국어 문서에 multilingual embedding 적용 (`intfloat/multilingual-e5-large`)

## 체크리스트

- [ ] Qdrant 로컬 실행 + dashboard (localhost:6333/dashboard) 접속 확인
- [ ] Chunk size 변화가 retrieval에 미치는 영향 관찰
- [ ] 유사 문서 top-1이 "맞긴 한데 미묘하게 틀린" 케이스 찾아서 기록
- [ ] Embedding 차원 (OpenAI 1536 vs MiniLM 384) 인지
- [ ] 로컬 vs API embedding 품질/비용/속도 표로 정리

## 핵심 키워드
- dense vector, sparse vector, hybrid, cosine similarity, dot product, L2 distance
- chunk, overlap, chunking strategy (fixed / recursive / semantic)
- MTEB, dimension, quantization (scalar / binary — 나중에)
- HNSW, IVF (Qdrant 내부 인덱스 — 이름만)
- Qdrant: collection, point, payload, filter
- BM25, TF-IDF (전통 sparse 기법 — RAG hybrid에서 다시 나옴)
