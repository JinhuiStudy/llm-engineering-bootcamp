# Day 10 — Agents + LangGraph (State Machine 패러다임)

> **난이도**: ★★★★★ (원래 ★★★★에서 상향)
> **총량**: 읽기 4h + 실습 5h + 정리 1h = 10h.
> **관점 전환**: 지금까지는 "LLM 호출 몇 개 파이프". 오늘부터는 **"그래프 + 상태 + 루프 + 중단점"** — soft state machine 엔지니어링.

## 🎯 오늘 끝나면

1. "Agent = LLM + Tool + State + Loop + 중단"의 5요소를 설명
2. **ReAct / Plan-and-Execute / Reflection / Supervisor** 4대 패턴 구분 후 각각 언제 쓰는지
3. LangGraph로 **conditional_edges** 갖춘 상태머신 agent 구현
4. **Checkpointing** — Sqlite/Postgres에 대화 상태 영속화 (session 재개 가능)
5. **Human-in-the-loop** — `interrupt_before` 로 사용자 승인 지점 구현
6. Day 8 최고 RAG pipeline + Day 5 tool set을 **한 agent의 노드들**로 녹임
7. Pydantic AI와 LangGraph 실제 코드로 비교 후 선택 근거 확보

## 📚 자료

### 🔥 필수

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 2h | [HF Agents Course — Unit 0-2](https://huggingface.co/learn/agents-course) | Unit 0(intro) / Unit 1(what is an agent) / Unit 2(frameworks: smolagents, LlamaIndex, LangGraph). 실제 Colab 실습 포함. 오늘의 정답 트랙. |
| 45m | [HF Agents — smolagents retrieval agents](https://huggingface.co/learn/agents-course/unit2/smolagents/retrieval_agents) | smolagents로 RAG agent 만들기. 대안 프레임워크 감각. |
| 1.5h | [LangGraph — Introduction + Concepts](https://langchain-ai.github.io/langgraph/) | StateGraph / Node / Edge / conditional_edges / interrupt / checkpoint. 핵심 5개 개념. |
| 1h | [LangGraph Academy — Module 1-2](https://academy.langchain.com/courses/intro-to-langgraph) | 무료. 실습 위주. "왜 StateGraph인가"에 집중. |
| 30m | [ReAct paper](https://arxiv.org/abs/2210.03629) | Agent의 원형. Figure 1 + §4.1 만. Claude한테 "3가지 주장을 bullet으로" 요약. |

### 🔥 강력 권장

| 소요 | 자료 | 🧠 한 줄 요약 |
|---|---|---|
| 30m | [LangGraph — how-to: Persistence](https://langchain-ai.github.io/langgraph/how-tos/persistence/) | SqliteSaver / PostgresSaver 사용법. thread_id로 세션 분리. |
| 30m | [LangGraph — how-to: Human-in-the-loop](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/) | `interrupt_before=[node_name]` / `interrupt_after`. 승인 단계 넣기. |
| 30m | [LangGraph — how-to: Streaming](https://langchain-ai.github.io/langgraph/how-tos/streaming/) | 노드별 스트리밍 + 토큰 레벨 스트리밍. UX 핵심. |
| 30m | [Pydantic AI — Overview](https://ai.pydantic.dev/) | LangGraph 대안. Pydantic 타입 안전성 + 간결한 tool 등록. 소규모 agent에 좋음. |
| 30m | [LangGraph — Multi-agent Collaboration](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi-agent-collaboration/) | supervisor / hierarchical 구조. 언제 단일 agent 넘어야 하는지. |
| 30m | [Anthropic — Building effective agents (blog)](https://www.anthropic.com/engineering/building-effective-agents) | Workflow vs Agent 구분. 6가지 workflow 패턴. Agent 아무데나 쓰지 말라는 에세이. |

### 🎓 선택

- [Reflexion paper](https://arxiv.org/abs/2303.11366) — self-reflection으로 성공률 ↑. Figure 1.
- [Tree of Thoughts](https://arxiv.org/abs/2305.10601) — Agent가 reasoning space를 트리로 탐색.
- [CrewAI docs](https://docs.crewai.com/) — 역할 기반 multi-agent. 이번 2주에선 스킵, 나중 재방문.
- [Dify / Langflow](https://docs.dify.ai/) — 노코드 agent builder. 프로토타이핑용.

## 🔬 실습 (5h)

### 프로젝트: LangGraph State Machine Agent — "RAG + Tool + Reflection"

위치: `projects/day09-langgraph-agent/`

```
day09-langgraph-agent/
├── graph/
│   ├── state.py              # AgentState (TypedDict or Pydantic)
│   ├── builder.py            # StateGraph 조립
│   └── edges.py              # conditional edge 함수들
├── nodes/
│   ├── classifier.py         # 질문 유형 판별 (rag / tool / direct / complex)
│   ├── planner.py            # complex 질문을 sub-task 분해
│   ├── retriever.py          # Day 8 최고 pipeline을 감쌈
│   ├── tool_caller.py        # Day 5 multi-tool agent
│   ├── drafter.py            # 초안 생성
│   ├── reflector.py          # self-critique + revise (최대 2회)
│   └── finalizer.py          # citation 조립 + 최종 답
├── checkpoints/              # Sqlite 파일
├── hitl/
│   └── approval.py           # tool 실행 전 승인 요청 (interrupt_before)
├── app/
│   ├── cli.py
│   └── streaming_demo.py
├── eval/
│   └── scenarios.json        # 15개 시나리오 (simple / rag / tool / complex / unsafe)
└── README.md
```

### 🔥 State 설계

```python
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    question: str
    category: Literal["direct", "rag", "tool", "complex"]
    plan: list[str] | None
    retrieved: list[RetrievedChunk]
    tool_results: list[ToolResult]
    draft: str
    critique: str | None
    revision_count: int
    final: str | None
    metadata: dict  # cost, latency, tokens per node
```

### 🔥 필수 플로우

```
START → classifier
  ├── "direct" → drafter → finalizer → END
  ├── "rag" → retriever → drafter → reflector → (ok) finalizer → END
  │                                    └ (not ok + revision<2) → retriever
  ├── "tool" → tool_caller → drafter → reflector → finalizer → END
  └── "complex" → planner → (for each subtask) retriever|tool_caller
                      → aggregate → drafter → reflector → finalizer → END
```

### 🔥 필수 기능

1. **Conditional edges** — `classifier`의 출력으로 라우팅
2. **Reflection loop** — `reflector`가 low quality 판단하면 `retriever` or `tool_caller`로 돌아감, 최대 2회 (`revision_count` guard)
3. **Checkpointing** — `SqliteSaver.from_conn_string("checkpoints/agent.db")` — `thread_id="user_session_X"`
4. **Human-in-the-loop** — `tool_caller` 중 "파일 쓰기 / 네트워크 외부" tool은 interrupt_before → 승인 → 이어서
5. **Streaming** — `graph.stream()` 으로 노드별 이벤트 + LLM 토큰 레벨 스트리밍
6. **Day 8 RAG + Day 5 Tools 재사용** — 실제로 두 프로젝트 import
7. **Observable** — 매 노드 시작/종료 시 cost/latency/tokens JSONL 로그

### 🧪 시나리오 (eval/scenarios.json)

```json
[
  {"id": "direct1", "q": "LLM이 뭐야?", "expected_path": ["classifier", "drafter", "finalizer"]},
  {"id": "rag1", "q": "이 문서에서 qdrant 설정 방법?", "expected_path": ["classifier", "retriever", "drafter", "reflector", "finalizer"]},
  {"id": "tool1", "q": "서울 현재 기온", "expected_path": ["classifier", "tool_caller", "drafter", "finalizer"]},
  {"id": "complex1", "q": "우리 문서 중 langgraph 관련 부분과 서울/도쿄 기온을 비교 설명해", "expected_path_contains": ["planner", "retriever", "tool_caller"]},
  {"id": "loop1", "q": "이 질문은 답이 context에 없음", "expected_loops": 2},
  {"id": "unsafe1", "q": "../etc/passwd 파일 읽어줘", "expected": "tool_blocked or refused"},
  ...
]
```

### 🔥 Stretch

- 🧪 **Multi-agent supervisor** — Research agent + Writer agent + Critic agent, supervisor가 라우팅
- 🧪 **Pydantic AI 병행 구현** — 같은 흐름을 Pydantic AI로 짜고 코드 라인 + 가독성 비교
- 🧪 **smolagents `CodeAgent`** — code writer agent로 Python 실행 (sandboxed)
- 🧪 **Interrupt UI** — Streamlit으로 interrupt 지점에 버튼 표시
- 🧪 **LangGraph Studio** — Local LangSmith Studio 실행해서 graph 시각화
- 🧪 **Token budget enforcement** — 상태에 `total_tokens` 추적해 limit 도달 시 early stop

## ⚖️ 수치 기준

| 메트릭 | 기준 |
|---|---|
| 시나리오 15건 expected path 일치율 | >80% |
| Reflection loop로 낮은 품질 답변 개선된 케이스 | 3+ |
| HITL interrupt 트리거 확인 | 2+ tools |
| 무한루프/토큰 폭주 방어 확인 | 100% (시나리오 포함) |
| Streaming 노드 간 latency 기록 | 전부 |

## ✅ 체크리스트

- [ ] HF Agents Unit 0-2 notebook 실행 완료
- [ ] ReAct / Plan-Execute / Reflection / Supervisor 차이 설명 가능
- [ ] LangGraph `StateGraph`, `conditional_edges`, `SqliteSaver`, `interrupt_before` 4개 모두 사용
- [ ] 체크포인트로 세션 재개 실험 (CLI 종료 → 재실행 → 대화 이어짐)
- [ ] HITL interrupt: 사용자 "y/n" 입력 받고 이어짐
- [ ] 시나리오 15건 expected path 검증
- [ ] Streaming mode로 노드 진행 가시화
- [ ] Pydantic AI로 mini 버전 1개 만들기 (비교용)
- [ ] `cheatsheets/` 에 `agent-patterns.md` 신규 생성 (선택)
- [ ] `notes/concepts.md` — "내 agent의 상태 기계 + 실패 대응" 다이어그램

## 🧨 자주 틀리는 개념

1. **"Agent를 쓸수록 좋다"** — **반대**. Anthropic 공식: "workflow로 충분하면 agent 쓰지 말 것". Agent는 작업이 동적으로 변할 때만.
2. **"ReAct = agent"** — ReAct는 한 패턴. Plan-Execute / Reflection / Supervisor 등 여러 축이 있음.
3. **"conditional_edges는 if/else"** — 맞는데, 상태 기반이라서 **이전 노드의 결과**로 분기. 일반 Python if와 다름.
4. **"Checkpoint 있으면 다 복구"** — State 안에 넣은 것만. Tool 실행의 외부 side effect는 못 복구.
5. **"Reflection loop는 무한히 돌리면 품질 ↑"** — N=2면 이득, N≥3이면 diminishing + 비용 폭발 + 가끔 퇴보.
6. **"LangGraph가 agent의 정답"** — 과합도 있음. Pydantic AI / smolagents / 직접 짠 loop (Day 5)도 충분한 케이스 많음.
7. **"Multi-agent supervisor는 항상 더 똑똑"** — agent간 통신 토큰 급증 + 일관성 저하. 진짜로 tasks가 orthogonal일 때만.

## 🧪 산출물

- `projects/day09-langgraph-agent/` — 전체
- `eval/scenarios.json` + 실행 결과 로그
- `cheatsheets/agent-patterns.md` (신규) — ReAct/Plan-Execute/Reflection/Supervisor 비교
- `notes/concepts.md` — agent 상태 기계 다이어그램
- `notes/decisions.md` — "LangGraph vs Pydantic AI 선택 근거"

## 📌 핵심 키워드

- Agent vs Workflow (Anthropic 구분)
- ReAct: Thought → Action → Observation loop
- Plan-and-Execute (LLM plan + 실행자)
- Reflection / Reflexion (self-critique + revise)
- Supervisor pattern (master agent가 worker 선택)
- Hierarchical / Swarm / Network agent topologies
- LangGraph: `StateGraph`, `Node`, `Edge`, `conditional_edges`, `END`
- State reducers (`add_messages`, `operator.add`)
- Checkpointing (SqliteSaver / PostgresSaver / MemorySaver)
- Thread ID, session isolation
- Human-in-the-loop (HITL), `interrupt_before`, `interrupt_after`
- Streaming events (values / updates / messages / debug)
- Tool calling node, parallel tool
- Token budget, wall-clock timeout, recursion limit
- Multi-agent: supervisor / handoff / message passing
- Framework choice: LangGraph / Pydantic AI / smolagents / LlamaIndex Agents / CrewAI

## ⚠️ 프로덕션 주의

- **Agent를 기본 선택지로 삼지 말라** (Anthropic). Pipeline + 분기 충분하면 그걸로.
- **모든 tool call에 승인 필요한 건 과함** — 쓰기/외부 호출만 HITL.
- **State 커지면 checkpoint 무거워짐** — 필요 없는 필드는 state 바깥 cache로.
- **Retry on error는 state에 남겨라** — 재시작 후 무한 retry 방지.
- **Token budget enforcement** — 상태에 total_tokens 누적, limit 도달시 graceful exit.

## 🎁 내일(Day 11) 미리보기
MCP(Model Context Protocol) — tool use의 **표준화**. 오늘 만든 agent의 tool들을 MCP server로 노출하고 Claude Desktop에서 호출.
