from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from lc_app.api.schemas import (
    AgentRequest,
    AgentResponse,
    ChatRequest,
    ChatResponse,
    HealthResponse,
    RagRequest,
    RagResponse,
    ReadyResponse,
)
from lc_app.core.errors import ProviderNotConfiguredError, VectorStoreNotReadyError
from lc_app.core.utils import timer
from lc_app.chains.rag import build_rag_chain
from lc_app.observability.tracing import get_tracer
from lc_app.rag.retriever import get_retriever
from lc_app.rag.store import VectorStoreManager

router = APIRouter()


@router.get("/healthz", response_model=HealthResponse)
async def healthz() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/readyz", response_model=ReadyResponse)
async def readyz(request: Request) -> ReadyResponse:
    store_manager: VectorStoreManager = request.app.state.vector_store
    vector_status = "ready" if store_manager.is_ready() else "missing"
    status = "ok" if vector_status == "ready" else "degraded"
    return ReadyResponse(status=status, vector_store=vector_status)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: Request, payload: ChatRequest) -> ChatResponse:
    chain = request.app.state.chat_chain
    request_id = request.state.request_id
    if request.app.state.llm_error:
        raise HTTPException(status_code=400, detail=request.app.state.llm_error)
    with timer() as elapsed_ms:
        try:
            tracer = get_tracer("chat")
            with tracer.start_as_current_span("chat_chain") as span:
                span.set_attribute("request_id", request_id)
                response = chain.invoke({"message": payload.message})
        except ProviderNotConfiguredError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ChatResponse(
        response=response,
        request_id=request_id,
        model=request.app.state.settings.llm_provider,
        latency_ms=elapsed_ms(),
    )


@router.post("/rag", response_model=RagResponse)
async def rag(request: Request, payload: RagRequest) -> RagResponse:
    request_id = request.state.request_id
    store_manager: VectorStoreManager = request.app.state.vector_store
    llm = request.app.state.llm
    if request.app.state.llm_error:
        raise HTTPException(status_code=400, detail=request.app.state.llm_error)
    with timer() as elapsed_ms:
        try:
            retriever = get_retriever(store_manager, payload.top_k)
            chain = build_rag_chain(llm, retriever)
            tracer = get_tracer("rag")
            with tracer.start_as_current_span("rag_chain") as span:
                span.set_attribute("request_id", request_id)
                result = chain.invoke({"question": payload.question})
        except VectorStoreNotReadyError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
    return RagResponse(
        answer=result["answer"],
        citations=result["citations"],
        request_id=request_id,
        latency_ms=elapsed_ms(),
    )


@router.post("/agent", response_model=AgentResponse)
async def agent(request: Request, payload: AgentRequest) -> AgentResponse:
    request_id = request.state.request_id
    chain = request.app.state.agent_chain
    with timer() as elapsed_ms:
        tracer = get_tracer("agent")
        with tracer.start_as_current_span("agent_chain") as span:
            span.set_attribute("request_id", request_id)
            result = chain.invoke(payload.task)
    return AgentResponse(
        result=result["result"],
        tool_calls=result["tool_calls"],
        request_id=request_id,
        latency_ms=elapsed_ms(),
    )


@router.get("/metrics")
async def metrics() -> PlainTextResponse:
    data = generate_latest()
    return PlainTextResponse(data.decode("utf-8"), media_type=CONTENT_TYPE_LATEST)
