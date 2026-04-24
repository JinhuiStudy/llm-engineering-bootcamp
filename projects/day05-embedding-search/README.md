# Day 6 — Embedding + Vector DB (Qdrant)

커리큘럼: `curriculum/week1-day06-embedding-vectordb.md`

## 체크리스트
- [ ] `docker-compose.yml` — Qdrant 로컬 (port 6333)
- [ ] `ingest.py` — 문서 → chunk → embed → upsert
- [ ] `search.py` — 쿼리 → embed → similarity search
- [ ] `compare.py` — BM25 vs embedding 비교
- [ ] Chunk size 200/500/1000 실험
- [ ] Overlap 0/50/200 실험
- [ ] OpenAI `text-embedding-3-small` + 로컬 `all-MiniLM-L6-v2` 둘 다
- [ ] Qdrant dashboard 접속 확인 (localhost:6333/dashboard)
- [ ] 결과를 notes/concepts.md에 표로
