"""Day 14: FastAPI entrypoint 스켈레톤.

실제 구현은 Day 14에 하되, 뼈대만 먼저.

실행:
    uv run uvicorn app.main:app --reload
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ai_study.logging import logger

app = FastAPI(title="Devlog RAG Copilot")


class ChatRequest(BaseModel):
    question: str
    profile: str = "dev"


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest) -> StreamingResponse:
    logger.info(f"chat: {req.question!r} profile={req.profile}")

    def stream():
        # TODO: 실제 LangGraph agent 연결
        for chunk in ["안녕", ". ", "RAG ", "답변 ", "스텁입니다."]:
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.post("/ingest")
def ingest() -> dict:
    # TODO: 폴더/URL → Qdrant
    return {"status": "todo"}
