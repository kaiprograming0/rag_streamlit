
"""RAGチャットUIの画面。

起動方法:
    python -m streamlit run src/chatbot_app.py
"""

import logging
import sys
from pathlib import Path

import streamlit as st



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

# =========================
# 1. プロジェクト設定
# =========================
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.chat_history.sqlite_repository import (
    SQLiteChatHistoryRepository,
)

from src.rag_core.pipeline import run_rag  # noqa: E402


# =========================
# DB設定
# =========================
repository = SQLiteChatHistoryRepository()

# =========================
# 保存対象のユーザー
# =========================
USER_ID = "local-user"

# 既存の会話を取得
sessions = repository.get_sessions(USER_ID)

if not sessions:
    st.error("保存先の会話がありません。")
    st.stop()

# 既存の会話を1つ選択
SESSION_ID = sessions[0]["session_id"]

# =========================
# 2. ページ設定
# =========================
st.set_page_config(
    page_title="RAGチャット",
    page_icon="💬",
)

st.title("💬 RAGチャット")
st.write("質問を入力すると、関連文書を検索して回答します。")


# =========================
# 3. 会話履歴の初期化
# =========================
if "messages" not in st.session_state:
    stored_messages = repository.get_session_messages(
        session_id=SESSION_ID,
        user_id=USER_ID,
    )

    st.session_state.messages = [
        {
            "role": message["role"],
            "content": message["content"],
        }
        for message in (stored_messages or [])
    ]


# =========================
# 4. サイドバーの設定
# =========================
with st.sidebar:
    st.title("設定")
    st.divider()

    st.subheader("検索設定")

    k = st.slider(
        "検索する文書数",
        min_value=1,
        max_value=10,
        value=3,
        step=1,
    )

    st.divider()

    if st.button("会話をリセット"):
        st.session_state.messages = []
        st.rerun()


# =========================
# 5. 過去の会話を表示
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            documents = message.get("documents", [])

            if documents:
                with st.expander("検索された文書を確認する"):
                    for i, document in enumerate(
                        documents,
                        start=1,
                    ):
                        st.markdown(f"**検索結果 {i}**")
                        st.write(document["page_content"])


# =========================
# 6. 質問を入力
# =========================
if question := st.chat_input("質問を入力してください"):

    # ユーザーの質問を保存・表示
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    try:
        # -------------------------
        # 7. RAG全体の処理を実行
        # -------------------------

        stored_messages = repository.get_session_messages(
            session_id=SESSION_ID,
            user_id=USER_ID,
        )

        chat_history = [
            {
                "role": message["role"],
                "content": message["content"],
            }
            for message in (stored_messages or [])
        ]

        with st.spinner("関連文書を検索して回答を生成しています..."):

            try:
                result = run_rag(
                    question=question,
                    k=k,
                    chat_history=chat_history,
                )
            except Exception:
                logger.exception("RAG処理でエラーが発生しました")
                raise

        answer = result["answer"]
        documents = result["source_documents"]

        # SQLiteに質問と回答を保存
        repository.add_message(
            session_id=SESSION_ID,
            role="user",
            content=question,
        )

        repository.add_message(
            session_id=SESSION_ID,
            role="assistant",
            content=answer,
        )

        # Documentオブジェクトを会話履歴に保存できる形式へ変換
        document_data = [
            {
                "page_content": document.page_content,
            }
            for document in documents
        ]

        # -------------------------
        # 8. AIの回答を保存・表示
        # -------------------------
        with st.chat_message("assistant"):
            st.markdown(answer)

            if document_data:
                with st.expander("検索された文書を確認する"):
                    for i, document in enumerate(
                        document_data,
                        start=1,
                    ):
                        st.markdown(f"**検索結果 {i}**")
                        st.write(document["page_content"])

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "documents": document_data,
            }
        )

    except (ValueError, FileNotFoundError) as e:
        st.error(str(e))

    except Exception:
        st.error(
            "処理中にエラーが発生しました。"
            "設定やアプリケーションのログを確認してください。"
        )
