
from pathlib import Path

from langchain_community.vectorstores import FAISS

from src.rag_core.retrieval.embeddings import load_embeddings


PROJECT_ROOT = Path(__file__).resolve().parents[3]
VECTORSTORE_PATH = PROJECT_ROOT / "data" / "multi_vectorstore"


def load_vectorstore() -> FAISS:
    """保存済みのFAISSインデックスを読み込む。"""

    index_file = VECTORSTORE_PATH / "index.faiss"
    metadata_file = VECTORSTORE_PATH / "index.pkl"

    if not index_file.is_file():
        raise FileNotFoundError(
            f"FAISSインデックスが見つかりません: {index_file}"
        )

    if not metadata_file.is_file():
        raise FileNotFoundError(
            f"FAISSのメタデータが見つかりません: {metadata_file}"
        )

    embeddings = load_embeddings()

    return FAISS.load_local(
        str(VECTORSTORE_PATH),
        embeddings,
        index_name="index",
        allow_dangerous_deserialization=True,
    )
