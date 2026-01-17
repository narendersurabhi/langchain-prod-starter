from __future__ import annotations

from typing import Any, Iterable, List

import numpy as np
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.embeddings import Embeddings


class FakeChatModel(BaseChatModel):
    model_name: str = "fake"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: list[str] | None = None,
        run_manager: Any | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        last_message = next(
            (message for message in reversed(messages) if isinstance(message, HumanMessage)),
            None,
        )
        content = last_message.content if last_message else ""
        response = f"Fake response to: {content}"
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=response))])

    @property
    def _llm_type(self) -> str:
        return "fake-chat"


class DeterministicEmbeddings(Embeddings):
    def __init__(self, size: int = 128) -> None:
        self.size = size

    def _embed(self, text: str) -> list[float]:
        vector = np.zeros(self.size, dtype=np.float32)
        for idx, char in enumerate(text.encode("utf-8")):
            vector[idx % self.size] += float(char)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector /= norm
        return vector.tolist()

    def embed_documents(self, texts: Iterable[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)
