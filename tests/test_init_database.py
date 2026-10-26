
from rag_streamlit.src.chat_history.init_database import (
    init_db,
    create_session,
    add_message,
    get_sessions,
    get_session_messages,
    update_session_title,
)

# 1. DBとテーブルを作成
init_db()

# 2. チャットを作成
user_id = "test_user"
session_id = create_session(
    user_id=user_id,
    title="RAGの学習",
)

# 3. 質問と回答を保存
add_message(
    session_id,
    "user",
    "RAGとは何ですか？",
)

add_message(
    session_id,
    "assistant",
    "RAGは検索結果を利用して回答を生成する仕組みです。",
)

# 4. タイトルを変更
update_session_title(
    session_id,
    user_id,
    "RAGの基礎学習",
)

# 5. チャット一覧を取得
print("\n--- チャット一覧 ---")
for session in get_sessions(user_id):
    print(session)

# 6. 会話履歴を取得
print("\n--- 会話履歴 ---")
messages = get_session_messages(session_id, user_id)

if messages is not None:
    for message in messages:
        print(f"{message['role']}: {message['content']}")

# 7. DBの保存先を確認
from rag_streamlit.src.chat_history.init_database import DB_PATH
print(f"\nDB保存先: {DB_PATH}")
