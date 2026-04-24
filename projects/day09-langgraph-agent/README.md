# Day 10 — LangGraph State Machine Agent

커리큘럼: `curriculum/week2-day10-agents-langgraph.md`

## 체크리스트
- [ ] HF Agents Course unit 0-2 완주
- [ ] `state.py` — TypedDict State (messages, plan, retrieved_docs, tool_results, draft, critique, final)
- [ ] `nodes/` — planner, retriever(RAG 재사용), tool_caller, reflector, finalizer
- [ ] `graph.py` — StateGraph + conditional edges
- [ ] Checkpointing (SqliteSaver)
- [ ] Reflection 루프 (최대 2회)
- [ ] 무한루프 방어 (max_iterations)
- [ ] 테스트: 단순 / RAG 필요 / 최신 정보 / 복합 쿼리 각각

## Stretch
- Streaming으로 노드 진행 표시
- Pydantic AI로 동일 기능 구현 후 코드 라인 비교
