
"""SQLiteデータベースの初期化モジュール。

実行例
    python src/chat_history/init_database.py
"""

from src.chat_history.connection import DB_PATH, get_connection


def init_db() -> None:
    """データベースにテーブルとインデックスを作成する。"""
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS chat_sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL DEFAULT '新しいチャット',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS chat_messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                role TEXT NOT NULL
                    CHECK (role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (session_id)
                    REFERENCES chat_sessions(session_id)
                    ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_sessions_user
                ON chat_sessions(user_id, updated_at);

            CREATE INDEX IF NOT EXISTS idx_messages_session
                ON chat_messages(session_id, message_id);
            """
        )


if __name__ == "__main__":
    init_db()
    print(f"SQLite DB initialized: {DB_PATH}")