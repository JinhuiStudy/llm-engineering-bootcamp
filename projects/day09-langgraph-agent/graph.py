"""Day 10: LangGraph state machine skeleton.

실제 로직은 커리큘럼 진행하며 채울 것. 이 파일은 "어떤 노드/엣지가 있어야 하는가"의 스캐폴드.
"""

from __future__ import annotations

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from state import AgentState

MAX_ITERATIONS = 3


# ── Nodes ──
def planner(state: AgentState) -> dict:
    # TODO: LLM으로 질문 → sub-task list
    return {"plan": ["step1", "step2"]}


def retriever(state: AgentState) -> dict:
    # TODO: Day 8 RAG 호출
    return {"retrieved": []}


def tool_caller(state: AgentState) -> dict:
    # TODO: Day 5 tools 호출
    return {"tool_results": []}


def drafter(state: AgentState) -> dict:
    # TODO: plan + retrieved + tools → draft
    return {"draft": "TODO"}


def reflector(state: AgentState) -> dict:
    # TODO: draft를 self-critique
    return {"critique": "looks ok", "iterations": state.get("iterations", 0) + 1}


def finalizer(state: AgentState) -> dict:
    return {"messages": [{"role": "assistant", "content": state["draft"]}]}


# ── Conditionals ──
def needs_rag(state: AgentState) -> str:
    # 간단 heuristic: plan에 "search" 들어가면 RAG
    return "retriever" if any("search" in s for s in state.get("plan", [])) else "tool_caller"


def should_reflect_again(state: AgentState) -> str:
    if state.get("iterations", 0) >= MAX_ITERATIONS:
        return "finalizer"
    if "ok" in state.get("critique", "").lower():
        return "finalizer"
    return "retriever"


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("planner", planner)
    g.add_node("retriever", retriever)
    g.add_node("tool_caller", tool_caller)
    g.add_node("drafter", drafter)
    g.add_node("reflector", reflector)
    g.add_node("finalizer", finalizer)

    g.add_edge(START, "planner")
    g.add_conditional_edges("planner", needs_rag, {"retriever": "retriever", "tool_caller": "tool_caller"})
    g.add_edge("retriever", "drafter")
    g.add_edge("tool_caller", "drafter")
    g.add_edge("drafter", "reflector")
    g.add_conditional_edges(
        "reflector",
        should_reflect_again,
        {"finalizer": "finalizer", "retriever": "retriever"},
    )
    g.add_edge("finalizer", END)

    memory = SqliteSaver.from_conn_string(":memory:")
    return g.compile(checkpointer=memory)


if __name__ == "__main__":
    app = build_graph()
    # 최소 smoke test
    result = app.invoke(
        {"messages": [{"role": "user", "content": "hello"}], "plan": [], "retrieved": [],
         "tool_results": [], "draft": "", "critique": "", "iterations": 0},
        config={"configurable": {"thread_id": "test"}},
    )
    print(result)
