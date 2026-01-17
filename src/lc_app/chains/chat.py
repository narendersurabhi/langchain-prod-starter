from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable


def build_chat_chain(llm) -> Runnable:
    prompt = ChatPromptTemplate.from_messages(
        [("system", "You are a helpful assistant."), ("human", "{message}")]
    )
    chain: Runnable = prompt | llm | StrOutputParser()
    return chain
