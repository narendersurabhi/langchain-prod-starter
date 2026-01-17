from pathlib import Path

from lc_app.llms.fake import DeterministicEmbeddings
from lc_app.rag.ingest import ensure_vector_store
from lc_app.rag.store import VectorStoreManager


def test_ingest_creates_store(tmp_path: Path):
    sample_docs = tmp_path / "sample_docs"
    sample_docs.mkdir()
    (sample_docs / "doc.md").write_text("Policy says hybrid work is allowed.")

    store_path = tmp_path / "vector_store"
    manager = VectorStoreManager(store_path, DeterministicEmbeddings())
    ensure_vector_store(manager, sample_docs)

    assert manager.is_ready()
    store = manager.load()
    assert store is not None
