import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

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
