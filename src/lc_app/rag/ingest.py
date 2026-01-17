from __future__ import annotations

from pathlib import Path

from langchain_core.documents import Document

from lc_app.rag.store import VectorStoreManager


def load_documents(sample_docs_path: Path) -> list[Document]:
    documents: list[Document] = []
    for file_path in sample_docs_path.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")
        documents.append(Document(page_content=content, metadata={"source": file_path.name}))
    return documents


def chunk_documents(documents: list[Document], chunk_size: int = 500) -> list[Document]:
    chunks: list[Document] = []
    for doc in documents:
        text = doc.page_content
        for idx in range(0, len(text), chunk_size):
            chunk_text = text[idx : idx + chunk_size]
            chunks.append(
                Document(
                    page_content=chunk_text,
                    metadata={"source": doc.metadata.get("source", "unknown")},
                )
            )
    return chunks


def ensure_vector_store(store_manager: VectorStoreManager, sample_docs_path: Path) -> None:
    if store_manager.is_ready():
        return
    documents = load_documents(sample_docs_path)
    chunks = chunk_documents(documents)
    store_manager.save(chunks)
