from pathlib import Path

import pytest

from lc_app.api.main import create_app


@pytest.fixture()
def app(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    sample_docs = tmp_path / "sample_docs"
    sample_docs.mkdir()
    (sample_docs / "doc.md").write_text("Health coverage starts on day one.")
    monkeypatch.setenv("ENV", "test")
    monkeypatch.setenv("LLM_PROVIDER", "fake")
    monkeypatch.setenv("VECTOR_STORE_PATH", str(tmp_path / "vector_store"))
    monkeypatch.setenv("SAMPLE_DOCS_PATH", str(sample_docs))
    return create_app()
