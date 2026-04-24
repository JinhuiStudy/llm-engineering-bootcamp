# Day 14 — Final Portfolio: Devlog RAG Copilot

커리큘럼: `curriculum/week2-day14-final-portfolio.md`

14일 부트캠프의 최종 산출물. GitHub 공개 품질.

## 통합 체크리스트
- [ ] Ingest 파이프라인 (폴더/URL → Qdrant)
- [ ] Hybrid retrieval (dense + BM25 + RRF)
- [ ] Cross-encoder reranker
- [ ] Query rewriting + multi-query
- [ ] LangGraph agent (planner → retriever/tools → reflector → finalizer)
- [ ] Structured output (Pydantic: answer + citations + confidence)
- [ ] Tool use 3개 이상 (web_search, calculator, today's date)
- [ ] MCP server로 핵심 기능 노출
- [ ] Langfuse tracing + cost + prompt versioning
- [ ] Ragas eval + CI gate (정답셋 30+)
- [ ] Multi-provider 지원 (OpenAI/Anthropic/Ollama/RunPod env 스위치)
- [ ] FastAPI + SSE streaming
- [ ] Anthropic prompt caching
- [ ] tenacity rate limit 대응
- [ ] Docker Compose 원클릭 실행

## README 체크리스트 (공개용)
- [ ] 한 줄 소개
- [ ] 동기 (Why)
- [ ] 아키텍처 다이어그램 (이미지)
- [ ] 기술 스택 배지
- [ ] 실행법 (docker-compose up)
- [ ] 스크린샷/gif 3장+
- [ ] Eval 결과 (Ragas 점수 표)
- [ ] 한계 + 개선점 (정직하게)
- [ ] 라이선스 (MIT)

## 14일차 시간 배분 (10h)
| 시간 | 작업 |
|---|---|
| 1h | Day 1-13 코드 재활용 선별 |
| 3h | app 스켈레톤 + LangGraph 조립 |
| 2h | RAG 포팅 + Langfuse 연결 |
| 1h | MCP 붙이기 |
| 1h | Eval 30개 + Ragas 통과 |
| 1h | README + 스크린샷 |
| 1h | git push + 회고 |
