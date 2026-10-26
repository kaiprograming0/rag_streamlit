
"""設定ファイルAIなどの
"""

import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.getenv(
    "AZURE_OPENAI_API_VERSION",
    "2024-10-21",
)

# Embeddingモデル一覧
EMBEDDING_MODELS = {
    "small": "text-embedding-3-small",
    #"large": "text-embedding-3-large",
}

# Chatモデル一覧
CHAT_MODELS = {
    "mini": "gpt-4.1-mini-1",
    # Azureにデプロイ済みのモデルを追加する
    # "gpt4": "実際のデプロイ名",
}

# デフォルトモデル
DEFAULT_EMBEDDING_MODEL = "small"
DEFAULT_CHAT_MODEL = "mini"

# FAISS保存先
VECTORSTORE_PATH = PROJECT_ROOT / "data" / "multi_vectorstore"
