# Day 10 — LangGraph State Machine Agent

> **연결**: [`curriculum/week2-day10-agents-langgraph.md`](../../curriculum/week2-day10-agents-langgraph.md)
> **의존성**: Day 8 winner RAG pipeline, Day 5 tool agent
> **다음**: Day 11 MCP로 노드 기능을 tool로 노출, Day 12 Langfuse trace, Day 14 app/agent

## 🎯 이 프로젝트로

1. `classifier → planner → retriever → tool_caller → reflector → finalizer` **6노드 StateGraph**
2. `conditional_edges`로 "direct / rag / tool / complex" 4가지 라우팅
3. **Reflection loop** — draft → critique → (부족하면) retriever로 되돌아감, 최대 2회
4. **SqliteSaver checkpoint** — 세션 재개 가능 (thread_id)
5. **HITL interrupt_before** — 민감 tool 실행 전 사용자 승인
6. **Streaming** — 노드별 이벤트 + LLM 토큰 레벨
7. Pydantic AI로 병행 mini 버전 → 코드 라인 수 비교

## 📁 디렉토리

```
day09-langgraph-agent/
├── pyproject.toml
├── graph/
│   ├── state.py                   # AgentState TypedDict + add_messages reducer
│   ├── builder.py                 # StateGraph 조립 → compile
│   └── edges.py                   # conditional edge 함수들
├── nodes/
│   ├── classifier.py              # 질문 → "direct" | "rag" | "tool" | "complex"
│   ├── planner.py                 # complex → sub-tasks
│   ├── retriever.py               # Day 8 winner pipeline wrap
│   ├── tool_caller.py             # Day 5 agent loop wrap
│   ├── drafter.py                 # 초안 생성
│   ├── reflector.py               # self-critique + quality score
│   └── finalizer.py               # citation 조립 + 최종 Answer
├── checkpoints/                   # Sqlite — gitignore
├── hitl/
│   └── approval.py                # interrupt_before 처리 헬퍼
├── pydantic_ai_version/           # 비교용 mini 구현
│   └── agent.py
├── app/
│   ├── cli.py
│   └── streaming_demo.py
├── eval/
│   ├── scenarios.json             # 15 시나리오 (expected_path 포함)
│   └── run.py
└── README.md
```

## 🚀 시작

```bash
cd projects/day09-langgraph-agent
uv sync
uv add langgraph langgraph-checkpoint-sqlite pydantic-ai
```

## ✅ 필수 기능

### State 설계
- [ ] `state.py`:
  ```python
  class AgentState(TypedDict):
      messages: Annotated[list[AnyMessage], add_messages]
      question: str
      category: Literal["direct", "rag", "tool", "complex"] | None
      plan: list[str] | None
      retrieved: list[RetrievedChunk]
      tool_results: list[ToolResult]
      draft: str | None
      critique: str | None
      revision_count: int
      final: Answer | None
      cost_usd: float
      tokens_total: int
  ```

### Nodes
- [ ] `classifier.py` — Haiku/flash로 질문 분류. `{"category": "..."}` 반환
- [ ] `planner.py` — complex 질문을 sub-tasks 3-5개로 분해 (Pydantic output)
- [ ] `retriever.py` — Day 8 winner pipeline 호출 → state에 chunks
- [ ] `tool_caller.py` — Day 5 loop 재사용
- [ ] `drafter.py` — context + tool results → Pydantic Answer 초안
- [ ] `reflector.py`:
  - 초안에 대해 "context 충분한가? 질문에 답하는가? citation 일치?"
  - `{quality: 1-5, needs_more_retrieval: bool, feedback: str}`
  - quality < 3 + revision_count < 2 → retriever로 되돌림
- [ ] `finalizer.py` — citation 조립 + 최종 state.final

### Graph
- [ ] `builder.py`:
  ```python
  g = StateGraph(AgentState)
  [g.add_node(name, fn) for name, fn in NODES.items()]
  
  g.add_edge(START, "classifier")
  g.add_conditional_edges("classifier",
      lambda s: s["category"],
      {"direct": "drafter", "rag": "retriever", "tool": "tool_caller", "complex": "planner"})
  g.add_edge("planner", "retriever")
  g.add_edge("retriever", "drafter")
  g.add_edge("tool_caller", "drafter")
  g.add_edge("drafter", "reflector")
  g.add_conditional_edges("reflector",
      lambda s: "retriever" if (s.get("revision_count",0)<2 and s["critique"] == "needs_more") else "finalizer",
      ["retriever", "finalizer"])
  g.add_edge("finalizer", END)
  
  app = g.compile(
      checkpointer=SqliteSaver.from_conn_string("checkpoints/agent.db"),
      interrupt_before=["tool_caller"],  # HITL
  )
  ```

### HITL
- [ ] `approval.py`:
  ```python
  # tool_caller 전에 중단됨
  # state 확인 후 사용자 y/n 입력 → update_state → resume
  state = app.get_state(config)
  print(f"About to call: {state.values['tool_calls']}")
  if input("Approve? (y/n) ") == "y":
      app.invoke(None, config)  # resume
  ```

### Streaming
- [ ] `streaming_demo.py`:
  ```python
  for event in app.stream(input, config, stream_mode="updates"):
      for node, update in event.items():
          print(f"[{node}] {update}")
  ```

### Eval
- [ ] `scenarios.json` 15개 — simple / rag / tool / complex / unanswerable / adversarial
- [ ] `run.py` — expected_path vs actual path, quality metric (Ragas 재호출 OK)

## 📊 수치 기준

| 메트릭 | 기준 |
|---|---|
| 15 시나리오 expected path 일치율 | ≥ 80% |
| Reflection이 품질 개선한 케이스 | ≥ 3 |
| HITL interrupt 트리거 확인 | 1+ tool |
| Checkpoint로 세션 재개 | 100% |
| Streaming 노드 이벤트 수집 | 전부 |
| Token budget exceed abort | 1회 시뮬레이션 |

## 🧨 실전 함정

1. **LangGraph conditional_edges**는 조건 함수 반환값 → edge 이름 매핑. 반환값에 오타 잦음
2. **`add_messages` reducer** 없으면 messages가 덮어쓰기 되어 히스토리 사라짐
3. **SqliteSaver thread_id 안 주면** — 모든 세션이 섞임
4. **`interrupt_before` 후 `invoke(None, config)`로 재개** — None이 중요 (새 입력 아니라 resume)
5. **Reflection loop revision_count guard 빠지면 무한루프**
6. **노드 함수에서 state 반환 시 partial OK** — dict 전체 리턴 안 해도 됨
7. **Streaming `stream_mode`** 4종: values (전체 state) / updates (노드별) / messages (토큰) / debug. 목적별 선택
8. **tool_caller 안에서 추가 LLM 호출도 trace에 잡히게** — Day 12 `@observe` 전파 필요

## 🎁 Stretch

- 🧪 **Pydantic AI 병행** — `pydantic_ai_version/agent.py`로 같은 흐름 구현 → 코드 라인 비교
- 🧪 **Multi-agent supervisor** — Researcher + Writer + Critic + Supervisor
- 🧪 **LangGraph Studio** — 로컬 UI로 graph 시각화
- 🧪 **Token budget enforcement** — state.tokens_total 추적, limit 시 graceful exit
- 🧪 **smolagents CodeAgent 한 버전** — code execution agent 구현

## 🔗 다음에 쓰이는 곳

- Day 11: graph nodes를 MCP tool로 wrap 가능
- Day 12: 모든 노드에 `@observe` trace
- Day 14: `app/agent/graph.py` 의 기반
