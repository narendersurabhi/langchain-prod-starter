from __future__ import annotations

from fastapi import FastAPI

from lc_app.api.middleware import RequestContextMiddleware
from lc_app.api.routes import router
from lc_app.chains.agent import build_agent
from lc_app.chains.chat import build_chat_chain
from lc_app.core.config import AppSettings
from lc_app.llms.factory import get_chat_model
from lc_app.llms.fake import DeterministicEmbeddings, FakeChatModel
from lc_app.observability.logging import setup_logging
from lc_app.observability.tracing import instrument_app, setup_tracing
from lc_app.rag.ingest import ensure_vector_store
from lc_app.rag.retriever import get_retriever
from lc_app.rag.store import VectorStoreManager


def create_app() -> FastAPI:
    settings = AppSettings()
    setup_logging(settings.log_level)

    app = FastAPI(title="LangChain Prod Starter", version="0.1.0")
    app.add_middleware(RequestContextMiddleware)

    if settings.enable_tracing:
        setup_tracing(settings.service_name)
        instrument_app(app)

    embeddings = DeterministicEmbeddings()
    vector_store = VectorStoreManager(settings.vector_store_path, embeddings)
    llm_error: str | None = None
    try:
        llm = get_chat_model(settings)
    except Exception as exc:  # noqa: BLE001 - capture provider errors for graceful startup
        llm_error = str(exc)
        llm = FakeChatModel()
    chat_chain = build_chat_chain(llm)
    agent_chain = build_agent()

    app.state.settings = settings
    app.state.vector_store = vector_store
    app.state.llm_error = llm_error
    app.state.llm = llm
    app.state.chat_chain = chat_chain
    app.state.agent_chain = agent_chain

    @app.on_event("startup")
    async def _startup() -> None:
        ensure_vector_store(vector_store, settings.sample_docs_path)
        get_retriever(vector_store, settings.rag_top_k)

    app.include_router(router)
    return app


app = create_app()
