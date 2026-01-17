from __future__ import annotations

from langchain_core.vectorstores import VectorStoreRetriever

from lc_app.core.errors import VectorStoreNotReadyError
from lc_app.rag.store import VectorStoreManager


def get_retriever(store_manager: VectorStoreManager, top_k: int) -> VectorStoreRetriever:
    store = store_manager.load()
    if store is None:
        raise VectorStoreNotReadyError("Vector store is not ready.")
    return store.as_retriever(search_kwargs={"k": top_k})
