# Day 10 — Agents + LangGraph

## 목표
- Agent가 "LLM + Tool Loop + State"라는 멘탈 모델 확보
- HF Agents Course의 unit 0-2 핵심 내용 소화
- LangGraph로 state machine 기반 agent 직접 구축
- ReAct / Plan-and-Execute / Reflection 패턴 구분

## 자료

| 분류 | 자료 | 소요 |
|---|---|---|
| 필수 | [HF Agents Course — unit 0-2](https://huggingface.co/learn/agents-course) | 3h |
| 필수 | [HF Agents Course — smolagents retrieval agents](https://huggingface.co/learn/agents-course/unit2/smolagents/retrieval_agents) | 1h |
| 필수 | [LangGraph docs — quickstart + concepts](https://langchain-ai.github.io/langgraph/) | 2h |
| 필수 | ReAct 논문 ([arxiv](https://arxiv.org/abs/2210.03629)) — Claude한테 요약 시키고 Figure 1만 | 0.5h |
| 선택 | [Pydantic AI overview](https://pydantic.dev/docs/ai/overview/) | 1h |
| 선택 | [LlamaIndex agents](https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/) | 1h |
| 선택 | [LangChain Academy](https://academy.langchain.com/) | 나중에 |
| 스킵 | CrewAI (이번 2주에서는 우선순위 낮음) | — |

## 실습 (5h)

### 프로젝트: LangGraph State Machine Agent
위치: `projects/day09-langgraph-agent/`

```
day09-langgraph-agent/
├── graph.py             # StateGraph 정의
├── nodes/
│   ├── planner.py       # 질문을 sub-task로 분해
│   ├── retriever.py     # RAG 호출 (Day 8 재사용)
│   ├── tool_caller.py   # 웹 검색/계산기
│   ├── reflector.py     # 답변 self-critique
│   └── finalizer.py     # 최종 답변 조립
├── state.py             # TypedDict / Pydantic State
├── app.py               # CLI
└── README.md
```

### 요구사항
1. State는 `messages`, `plan`, `retrieved_docs`, `tool_results`, `draft`, `critique`, `final` 정도
2. Conditional edge로 "계획이 필요한가" / "RAG 필요한가" / "툴 필요한가" 라우팅
3. Reflection 루프: draft → critique → 부족하면 다시 retriever로 (최대 2회)
4. Checkpointing (SqliteSaver) — 대화 히스토리 영속화
5. Tool은 Day 5의 멀티툴을 그대로 재사용

### 테스트 쿼리
- 단순 질문 (툴 필요 없음) → 바로 finalizer
- 지식 질문 → retriever로 라우팅
- 최신 정보 질문 → web_search 툴
- 복합 질문 → planner → 여러 노드 순회

### Stretch
- Streaming으로 노드 진행 상황 실시간 출력
- Pydantic AI로 동일 기능 구현, 코드 비교

## 체크리스트

- [ ] ReAct vs Plan-and-Execute vs Reflection 차이 설명 가능
- [ ] LangGraph의 conditional edge 동작 이해
- [ ] Checkpointing으로 중간 상태 복구 실험
- [ ] "무한루프 방어"를 어떻게 했는지 기록
- [ ] `cheatsheets/agent-patterns.md` (선택) 작성

## 핵심 키워드
- Agent loop, tool calling, state machine, checkpoint
- ReAct, Plan-and-Execute, Reflection, Reflexion, Tree of Thoughts
- LangGraph: `StateGraph`, `Node`, `Edge`, `conditional_edges`, `END`
- Human-in-the-loop, interruption, approval gating
- Multi-agent (supervisor, hierarchical) — 개념만
- Pydantic AI, smolagents, LlamaIndex Agents, CrewAI — 선택지로서 인지
