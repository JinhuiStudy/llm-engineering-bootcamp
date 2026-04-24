# Day 8 — 고급 RAG (Query Translation / Rerank / Hybrid)

## 목표
- 어제 만든 PDF Q&A v1의 품질 문제를 실제로 고치면서 고급 기법 체화
- Query rewriting / HyDE / RAG-Fusion / Multi-query / Reranking / Hybrid search 적용

## 자료

| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [RAG From Scratch — Part 5-14 (Query translation, Routing, RAPTOR, ColBERT)](https://github.com/langchain-ai/rag-from-scratch) | 3h |
| 필수 | [OpenAI Cookbook — Search reranking with cross-encoders](https://github.com/openai/openai-cookbook/blob/main/examples/Search_reranking_with_cross-encoders.ipynb) | 1h |
| 필수 | [SBERT — Cross-Encoders](https://www.sbert.net/examples/cross_encoder/applications/README.html) | 0.5h |
| 필수 | [Qdrant — Hybrid queries](https://qdrant.tech/documentation/concepts/hybrid-queries/) | 1h |
| 선택 | [Weaviate — Hybrid search](https://docs.weaviate.io/weaviate/search/hybrid) | 0.5h |
| 선택 | [LlamaIndex — Qdrant hybrid example](https://docs.llamaindex.ai/en/stable/examples/vector_stores/qdrant_hybrid/) | 0.5h |
| 선택 | [HuggingFace — cross-encoder models](https://huggingface.co/cross-encoder) | — |

## 실습 (5h)

### 프로젝트: PDF Q&A 봇 v2 (개선판)
위치: `projects/day07-advanced-rag/` (Day 7에서 복사해 시작)

```
day07-advanced-rag/
├── retrievers/
│   ├── dense.py              # 기존 embedding search
│   ├── bm25.py               # sparse
│   ├── hybrid.py             # RRF (Reciprocal Rank Fusion)
│   └── reranker.py           # cross-encoder rerank
├── query_transform/
│   ├── rewrite.py            # LLM으로 query 다시 쓰기
│   ├── hyde.py               # Hypothetical Document Embeddings
│   ├── multi_query.py        # 1 query → N query
│   └── decompose.py          # sub-question decomposition
├── rag.py                    # 파이프라인 조립
└── eval/
    └── qa_pairs.json         # 수기 작성 정답셋 20개 (내일 Ragas에서 사용)
```

### 요구사항
1. **Query rewriting**: LLM으로 사용자 질문을 검색용 쿼리로 다듬기
2. **HyDE**: "가상의 답변"을 생성해 그걸로 검색
3. **Multi-query**: 한 질문을 3~5가지 변형으로 확장 후 결과 병합
4. **Reranking**: `cross-encoder/ms-marco-MiniLM-L-6-v2` 또는 Cohere rerank(무료 trial) 로 top-k 재정렬
5. **Hybrid search**: BM25 + dense 결과를 RRF로 결합
6. 각 기법을 켜고 끄며 동일 쿼리에 대해 결과 차이를 로그

### Stretch
- RAG-Fusion (multi-query + RRF)
- Parent Document Retriever (chunk는 작게 retrieve하고 넘길 때는 부모 문서로 확장)

## 체크리스트

- [ ] HyDE가 언제 도움이 되고 언제 독이 되는지 설명 가능
- [ ] Cross-encoder rerank 전후 top-1 정확도 비교
- [ ] Hybrid가 단일 dense보다 나은 케이스와 나쁜 케이스 관찰
- [ ] `cheatsheets/rag-patterns.md` 작성
- [ ] 오늘 쓴 20개 Q&A pair를 `eval/qa_pairs.json`에 저장 (내일 사용)

## 핵심 키워드
- Query rewriting, HyDE (Hypothetical Doc Embeddings), Multi-query, Step-back prompting
- Routing (logical routing, semantic routing)
- Sub-question decomposition
- Reranking (cross-encoder vs bi-encoder)
- Hybrid search, RRF (Reciprocal Rank Fusion)
- RAPTOR, ColBERT (이름/개념만)
- Parent document retriever, Small-to-big retrieval
