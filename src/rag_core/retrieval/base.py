from abc import ABC, abstractmethod

from langchain_core.documents import Document


class BaseRetriever(ABC):
    """検索方式の共通インターフェース"""

    @abstractmethod
    def retrieve(
        self,
        question: str,
        k: int = 3,
    ) -> list[Document]:
        """質問に関連する文書を取得する。"""
        pass