from langchain_core.documents import Document

from src.rag_core.generation.generator import generate_answer
from src.rag_core.retrieval.base import BaseRetriever
from src.rag_core.retrieval.vector_retriever import VectorRetriever


class RAGPipeline:
    """文書検索から回答生成までを統括する。"""

    def __init__(
        self,
        retriever: BaseRetriever | None = None,
    ) -> None:
        self.retriever = (
            retriever
            if retriever is not None
            else VectorRetriever()
        )

    def run(
        self,
        question: str,
        k: int = 3,
        chat_history: list[dict[str, str]] | None = None,
    ) -> dict[str, str | list[Document]]:
        """質問の受付から文書検索、回答生成までを実行する。"""

        if not isinstance(question, str) or not question.strip():
            raise ValueError("質問を入力してください。")

        documents = self.retriever.retrieve(
            question=question,
            k=k,
        )

        answer = generate_answer(
            question=question.strip(),
            documents=documents,
            chat_history=chat_history,
        )

        return {
            "question": question.strip(),
            "answer": answer,
            "source_documents": documents,
        }


def run_rag(
    question: str,
    k: int = 3,
    chat_history: list[dict[str, str]] | None = None,
) -> dict[str, str | list[Document]]:
    """既存の呼び出し方を維持するための関数。"""

    pipeline = RAGPipeline()
    return pipeline.run(question=question, k=k, chat_history=chat_history)
