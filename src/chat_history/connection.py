# src/chat_history/connection.py
"""SQLiteの接続管理モジュール。"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


# =========================================================
# 設定
# =========================================================

# プロジェクトのルートディレクトリ
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# データ保存先
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "chat_history.db"


# =========================================================
# 接続管理
# =========================================================

@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """SQLite接続を取得し、処理後に確実に閉じる。"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()