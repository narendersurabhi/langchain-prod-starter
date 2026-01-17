from __future__ import annotations

from typing import Any

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough
from langchain_core.vectorstores import VectorStoreRetriever


def _format_context(docs: list[Any]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def _build_citations(docs: list[Any]) -> list[dict[str, str]]:
    citations: list[dict[str, str]] = []
    for doc in docs:
        snippet = doc.page_content[:160].replace("\n", " ")
        citations.append({"source": doc.metadata.get("source", "unknown"), "snippet": snippet})
    return citations


def build_rag_chain(llm, retriever: VectorStoreRetriever) -> Runnable:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Answer using the provided context. Cite sources."),
            ("human", "Question: {question}\n\nContext: {context}"),
        ]
    )

    retrieval = retriever | RunnableLambda(_format_context)
    chain = (
        {
            "question": RunnablePassthrough(),
            "context": retrieval,
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    def with_citations(inputs: dict[str, Any]) -> dict[str, Any]:
        docs = retriever.get_relevant_documents(inputs["question"])
        return {
            "answer": chain.invoke(inputs["question"]),
            "citations": _build_citations(docs),
        }

    return RunnableLambda(with_citations)
