from __future__ import annotations

from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from lc_app.llms.fake import DeterministicEmbeddings


class VectorStoreManager:
    def __init__(self, store_path: Path, embeddings: DeterministicEmbeddings) -> None:
        self.store_path = store_path
        self.embeddings = embeddings

    def save(self, documents: list[Document]) -> FAISS:
        store = FAISS.from_documents(documents, self.embeddings)
        self.store_path.mkdir(parents=True, exist_ok=True)
        store.save_local(str(self.store_path))
        return store

    def load(self) -> FAISS | None:
        if not self.is_ready():
            return None
        return FAISS.load_local(
            str(self.store_path),
            self.embeddings,
            allow_dangerous_deserialization=True,
        )

    def is_ready(self) -> bool:
        return self.store_path.exists() and any(self.store_path.iterdir())
