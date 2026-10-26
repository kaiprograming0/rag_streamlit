"""チャット履歴リポジトリの抽象インターフェース。"""

from abc import ABC, abstractmethod


class ChatHistoryRepository(ABC):
    """チャット履歴の操作に必要なインターフェース。"""

    @abstractmethod
    def create_session(
        self,
        user_id: str,
        title: str = "新しいチャット",
    ) -> int:
        """チャットセッションを作成する。"""
        raise NotImplementedError

    @abstractmethod
    def add_message(
        self,
        session_id: int,
        role: str,
        content: str,
    ) -> int:
        """メッセージを保存する。"""
        raise NotImplementedError

    @abstractmethod
    def get_messages(self, session_id: int) -> list[dict]:
        """メッセージ一覧を取得する。"""
        raise NotImplementedError

    @abstractmethod
    def get_sessions(self, user_id: str) -> list[dict]:
        """ユーザーのチャット一覧を取得する。"""
        raise NotImplementedError

    @abstractmethod
    def delete_session(
        self,
        session_id: int,
        user_id: str,
    ) -> bool:
        """指定ユーザーのチャットを削除する。"""
        raise NotImplementedError