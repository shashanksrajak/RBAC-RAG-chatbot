from typing import List
from typing_extensions import Annotated, TypedDict, List
from langchain_core.documents import Document

# Desired schema for response


class AnswerWithSources(TypedDict):
    """An answer to the question, with sources."""

    answer: str
    sources: Annotated[
        List[str],
        ...,
        "List of sources (source_file) used to answer the question",
    ]


class State(TypedDict):
    question: str
    access_level: str
    context: List[Document]
    answer: AnswerWithSources
