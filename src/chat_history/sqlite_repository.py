"""SQLiteを使用したチャット履歴リポジトリ。"""

from datetime import datetime

from src.chat_history.base import ChatHistoryRepository
from src.chat_history.connection import get_connection


def now_iso() -> str:
    """現在日時をISO 8601形式で取得する。"""
    return datetime.now().astimezone().isoformat(timespec="seconds")


class SQLiteChatHistoryRepository(ChatHistoryRepository):
    """SQLiteによるチャット履歴のCRUD操作を担当する。"""

    def create_user(self, user_id: str) -> None:
        """ユーザーを登録する。既存ユーザーは変更しない。"""
        if not user_id.strip():
            raise ValueError("user_idは空にできません。")

        with get_connection() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO users (user_id, created_at)
                VALUES (?, ?)
                """,
                (user_id, now_iso()),
            )

    def create_session(
        self,
        user_id: str,
        title: str = "新しいチャット",
    ) -> int:
        """チャットを作成し、session_idを返す。"""
        if not user_id.strip():
            raise ValueError("user_idは空にできません。")

        timestamp = now_iso()

        with get_connection() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO users (user_id, created_at)
                VALUES (?, ?)
                """,
                (user_id, timestamp),
            )

            cursor = conn.execute(
                """
                INSERT INTO chat_sessions
                    (user_id, title, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, title, timestamp, timestamp),
            )

            return int(cursor.lastrowid)

    def get_sessions(self, user_id: str) -> list[dict]:
        """ユーザーのチャット一覧を取得する。"""
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT session_id, user_id, title, created_at, updated_at
                FROM chat_sessions
                WHERE user_id = ?
                ORDER BY updated_at DESC, session_id DESC
                """,
                (user_id,),
            ).fetchall()

            return [dict(row) for row in rows]

    def update_session_title(
        self,
        session_id: int,
        user_id: str,
        title: str,
    ) -> bool:
        """指定ユーザーのチャットタイトルを変更する。"""
        if not title.strip():
            raise ValueError("titleは空にできません。")

        with get_connection() as conn:
            cursor = conn.execute(
                """
                UPDATE chat_sessions
                SET title = ?, updated_at = ?
                WHERE session_id = ? AND user_id = ?
                """,
                (title, now_iso(), session_id, user_id),
            )

            return cursor.rowcount > 0

    def delete_session(self, session_id: int, user_id: str) -> bool:
        """指定ユーザーのチャットを削除する。"""
        with get_connection() as conn:
            cursor = conn.execute(
                """
                DELETE FROM chat_sessions
                WHERE session_id = ? AND user_id = ?
                """,
                (session_id, user_id),
            )

            return cursor.rowcount > 0

    def add_message(
        self,
        session_id: int,
        role: str,
        content: str,
    ) -> int:
        """質問または回答を保存し、message_idを返す。"""
        if role not in ("user", "assistant"):
            raise ValueError(
                "roleは'user'または'assistant'を指定してください。"
            )

        if not content.strip():
            raise ValueError("contentは空にできません。")

        timestamp = now_iso()

        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO chat_messages
                    (session_id, role, content, created_at)
                SELECT session_id, ?, ?, ?
                FROM chat_sessions
                WHERE session_id = ?
                """,
                (role, content, timestamp, session_id),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    f"チャットが存在しません: session_id={session_id}"
                )

            conn.execute(
                """
                UPDATE chat_sessions
                SET updated_at = ?
                WHERE session_id = ?
                """,
                (timestamp, session_id),
            )

            return int(cursor.lastrowid)

    def get_messages(self, session_id: int) -> list[dict]:
        """指定チャットのメッセージを古い順に取得する。"""
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT message_id, session_id, role, content, created_at
                FROM chat_messages
                WHERE session_id = ?
                ORDER BY message_id ASC
                """,
                (session_id,),
            ).fetchall()

            return [dict(row) for row in rows]

    def get_session_messages(
        self,
        session_id: int,
        user_id: str,
    ) -> list[dict] | None:
        """所有者を確認してからメッセージを取得する。"""
        with get_connection() as conn:
            session = conn.execute(
                """
                SELECT session_id
                FROM chat_sessions
                WHERE session_id = ? AND user_id = ?
                """,
                (session_id, user_id),
            ).fetchone()

            if session is None:
                return None

            rows = conn.execute(
                """
                SELECT message_id, session_id, role, content, created_at
                FROM chat_messages
                WHERE session_id = ?
                ORDER BY message_id ASC
                """,
                (session_id,),
            ).fetchall()

            return [dict(row) for row in rows]