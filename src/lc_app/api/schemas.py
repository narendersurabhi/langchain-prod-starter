from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    request_id: str
    model: str
    latency_ms: float


class RagRequest(BaseModel):
    question: str
    top_k: int = 4


class Citation(BaseModel):
    source: str
    snippet: str


class RagResponse(BaseModel):
    answer: str
    citations: list[Citation]
    request_id: str
    latency_ms: float


class AgentRequest(BaseModel):
    task: str


class AgentResponse(BaseModel):
    result: str
    tool_calls: list[dict[str, Any]]
    request_id: str
    latency_ms: float


class HealthResponse(BaseModel):
    status: str


class ReadyResponse(BaseModel):
    status: str
    vector_store: str
