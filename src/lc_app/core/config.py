from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    env: Literal["dev", "prod", "test"] = "dev"
    log_level: Literal["debug", "info", "warning", "error"] = "info"
    service_name: str = "lc_app"
    request_timeout_s: float = 30.0
    enable_tracing: bool = False

    llm_provider: Literal["fake", "openai", "anthropic", "ollama"] = "fake"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    ollama_base_url: str | None = None

    rag_top_k: int = 4
    vector_store_path: Path = Path(".cache/vector_store")
    sample_docs_path: Path = Path("data/sample_docs")


class ReadyCheck(BaseModel):
    status: Literal["ok", "degraded"]
    vector_store: Literal["ready", "missing"]


class ErrorResponse(BaseModel):
    message: str = Field(..., description="Human-readable error message")
    request_id: str
