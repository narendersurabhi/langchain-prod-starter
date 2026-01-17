from __future__ import annotations

from lc_app.core.config import AppSettings
from lc_app.core.errors import ProviderNotConfiguredError
from langchain_core.language_models.chat_models import BaseChatModel

from lc_app.llms.fake import FakeChatModel


def get_chat_model(settings: AppSettings) -> BaseChatModel:
    if settings.llm_provider == "fake":
        return FakeChatModel()

    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise ProviderNotConfiguredError("OPENAI_API_KEY is not set.")
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(api_key=settings.openai_api_key, model="gpt-4o-mini")

    if settings.llm_provider == "anthropic":
        if not settings.anthropic_api_key:
            raise ProviderNotConfiguredError("ANTHROPIC_API_KEY is not set.")
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(api_key=settings.anthropic_api_key, model="claude-3-haiku-20240307")

    if settings.llm_provider == "ollama":
        if not settings.ollama_base_url:
            raise ProviderNotConfiguredError("OLLAMA_BASE_URL is not set.")
        from langchain_ollama import ChatOllama

        return ChatOllama(base_url=settings.ollama_base_url, model="llama3")

    raise ProviderNotConfiguredError("Unknown provider configuration.")
