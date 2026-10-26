
from langchain_core.documents import Document
from pydantic import BaseModel, ConfigDict, Field


from src.rag_core.retrieval.base import BaseRetriever
from src.rag_core.retrieval.vectorstore import load_vectorstore

class RetrievalRequest(BaseModel):
    """文書検索の入力データ"""

    model_config = ConfigDict(strict=True)

    question: str = Field(min_length=1)
    k: int = Field(default=3, ge=1, le=10)


class VectorRetriever(BaseRetriever):
    """FAISSによるベクトル検索"""

    def __init__(self) -> None:
        self.vectorstore = load_vectorstore()

    def retrieve(
        self,
        question: str,
        k: int = 3,
    ) -> list[Document]:
        request = RetrievalRequest(
            question=question,
            k=k,
        )

        return self.vectorstore.similarity_search(
            request.question,
            k=request.k,
        )
