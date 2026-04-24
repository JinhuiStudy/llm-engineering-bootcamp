# Day 8 — 고급 RAG (v2)

커리큘럼: `curriculum/week2-day08-advanced-rag.md`

Day 6의 v1을 복사해서 시작. 기능을 하나씩 추가하며 비교.

## 체크리스트
- [ ] RAG From Scratch Part 5-14 노트북 완주
- [ ] `retrievers/dense.py` / `bm25.py` / `hybrid.py` / `reranker.py`
- [ ] `query_transform/rewrite.py` / `hyde.py` / `multi_query.py` / `decompose.py`
- [ ] Reranker: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- [ ] Hybrid: RRF로 dense+BM25 결합
- [ ] `eval/qa_pairs.json` — 정답셋 20개 수기 (내일 Ragas에서 사용)
- [ ] 각 기법 on/off로 동일 쿼리 결과 비교 기록
- [ ] HyDE의 함정 케이스 기록 (가설이 틀렸을 때)

## 비교표 양식
| config | Q1 | Q2 | ... | 관찰 |
|---|---|---|---|---|
| baseline | ... |
| +rewrite | ... |
| +hyde | ... |
| +rerank | ... |
| +hybrid | ... |
| all | ... |
