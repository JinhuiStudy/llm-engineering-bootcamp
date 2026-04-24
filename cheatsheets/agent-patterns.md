# Agent Patterns 치트시트

## 큰 그림 — Agent vs Workflow (Anthropic 구분)

- **Workflow**: LLM 호출이 **사전에 정해진 경로**를 따름 (prompt chain, routing, parallelization). 예측 가능성 ↑.
- **Agent**: LLM이 **자기 실행 경로를 동적으로 결정** (tool loop + state). 유연성 ↑, 비용/지연/비결정성 ↑.

> 🟢 기본 선택: Workflow. Agent는 작업이 진짜로 동적일 때만.

## 6대 Workflow 패턴

### 1. Prompt Chaining
```
Input → LLM1 → Gate(should continue?) → LLM2 → Output
```
명확한 순차 태스크. Gate는 `if` 또는 LLM-based guard.

### 2. Routing
```
Input → Classifier LLM → (route_a | route_b | route_c)
```
"어떤 sub-pipeline으로 보낼지" 결정. 무거운 모델 아끼기에 유리.

### 3. Parallelization
- **Sectioning**: 입력을 독립 조각으로 쪼개 N 모델 병렬 → 합치기
- **Voting**: 같은 입력을 N번 돌려 다수결 (Self-Consistency)

### 4. Orchestrator-Workers
중앙 LLM이 sub-task를 동적으로 정의 → worker LLM들이 실행 → 중앙이 통합. Plan-and-Execute 원형.

### 5. Evaluator-Optimizer (Reflection)
```
LLM → draft → Evaluator LLM → ok? → output | feedback → LLM → ...
```
품질 낮은 분야에 효과적. 비용 2-3배.

### 6. Agent (진짜 agent)
Tool loop + state + 자율 plan. 경계 불명확, 환경 자체가 변하는 태스크.

## Agent 구현 패턴

### ReAct
```
Observation → Thought → Action (tool) → Observation → ...
```
- 원조 agent 패턴. ([Yao 2022](https://arxiv.org/abs/2210.03629))
- Thought가 모델 head에 노출됨 → 디버깅 쉬움, but 비용 ↑

### Plan-and-Execute
```
Planner LLM → step 1, 2, 3 → Executor LLM (step 1) → ... → Final
```
- 계획 먼저. 중간에 계획 수정 가능 (replan)
- 복잡한 multi-step에 강함

### Reflection / Reflexion
```
Generate → Critique → Revise → (repeat up to N)
```
- Reflexion은 실행 실패 시 memory에 저장해 다음 에피소드에 활용
- N=2가 sweet. N≥3 diminishing + 퇴보 가능

### Supervisor (multi-agent)
```
Supervisor → (Research agent | Write agent | Critic agent)
           → 결과 통합 or 재배정
```
- 진짜 orthogonal한 subtasks에만 유리
- 토큰 통신 비용 주의

### Swarm / Handoff
Agent들이 직접 서로 넘김. OpenAI Swarm (experimental), LangGraph `Command(goto=...)`

## LangGraph 핵심 API

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

# 1. State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    plan: list[str] | None
    ...

# 2. Nodes (함수)
def classifier(state): return {"category": "rag"}
def retriever(state): return {"retrieved": [...]}
def drafter(state): return {"draft": "..."}

# 3. Graph
g = StateGraph(AgentState)
g.add_node("classifier", classifier)
g.add_node("retriever", retriever)
g.add_node("drafter", drafter)

g.add_edge(START, "classifier")
g.add_conditional_edges("classifier",
    lambda s: s["category"],
    {"rag": "retriever", "direct": "drafter"})
g.add_edge("retriever", "drafter")
g.add_edge("drafter", END)

# 4. Compile + checkpoint + HITL
app = g.compile(
    checkpointer=SqliteSaver.from_conn_string("./agent.db"),
    interrupt_before=["tool_caller"],  # HITL
)

# 5. Run
for event in app.stream(
    {"messages": [{"role":"user","content":"..."}]},
    config={"configurable": {"thread_id": "user-123"}}
):
    print(event)
```

## Framework 선택 결정표

| 상황 | 추천 |
|---|---|
| 큰 state machine, checkpointing 필요 | **LangGraph** |
| 타입 안전성 중시, Pydantic 스택 | **Pydantic AI** |
| 최소 코드 + smolagents 기본 | **smolagents** (HF) |
| 이미 LlamaIndex RAG 써봄 | **LlamaIndex Agents** |
| 역할 기반 multi-agent 실험 | **CrewAI** |
| 노코드 프로토타입 | Dify / Langflow |
| 다 커스텀 | 직접 loop (Day 5 패턴) |

## Safety rails (반드시 4개 다)

1. **Recursion limit** — LangGraph `recursion_limit=25`
2. **Token budget** — state에 total_tokens 누적, threshold 넘으면 early exit
3. **Wall-clock timeout** — `asyncio.timeout(60)`
4. **Same-call-repeat detector** — 최근 3 tool call이 동일이면 abort

## HITL (Human-in-the-loop)

```python
g.compile(interrupt_before=["tool_caller"])
# 또는
g.compile(interrupt_after=["plan"])
```
- 사용자 승인 대기 → `app.update_state(config, ...)` 로 재개
- State 수정도 가능 (plan edit)

## Checkpointing

| Store | 용도 |
|---|---|
| `MemorySaver` | 테스트만 |
| `SqliteSaver` | 단일 노드, 개발 |
| `PostgresSaver` | 프로덕션 |
| Redis/Custom | 수평 확장 |

- `thread_id`로 세션 분리 (user_id + conversation_id 조합)
- State 크면 I/O 비용 ↑, `add_messages` reducer로 append-only 유지

## Streaming

```python
for event in app.stream(input, config, stream_mode="values"):
    # values: 전체 state 스냅샷
    # updates: 노드별 업데이트
    # messages: LLM 토큰 레벨
    # debug: 모두
    ...
```

## 안티패턴

- ❌ Agent를 기본 선택. workflow로 해결 가능한 걸 agent로 → 비용/버그 폭발
- ❌ Reflection을 모든 답변에 강제 → 토큰 3배
- ❌ Multi-agent를 선행 검증 없이 → 토큰 5-10배, 일관성 ↓
- ❌ Tool 실행 결과를 그대로 state에 축적 → state 폭증
- ❌ Checkpoint 없는 agent를 production에 → 중단 시 복구 불가
- ❌ Token budget 없는 loop → 비용 통제 불능

## 수치 기준

| 메트릭 | 권장 |
|---|---|
| Reflection iteration | ≤ 2 |
| Total recursion | ≤ 25 |
| Wall-clock timeout | 60s (길면 streaming) |
| Tool call per conversation | ≤ 20 |
| State size (checkpoint) | < 100KB / turn |

## References
- [Anthropic — Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) — 6 workflow + agent 구분 원문
- [LangGraph docs](https://langchain-ai.github.io/langgraph/)
- [HF Agents Course](https://huggingface.co/learn/agents-course)
- [Pydantic AI](https://ai.pydantic.dev/)
- [ReAct paper](https://arxiv.org/abs/2210.03629) / [Reflexion paper](https://arxiv.org/abs/2303.11366)
