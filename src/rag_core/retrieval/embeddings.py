
from langchain_openai import AzureOpenAIEmbeddings

from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_ENDPOINT,
    DEFAULT_EMBEDDING_MODEL,
    EMBEDDING_MODELS,
)


def load_embeddings() -> AzureOpenAIEmbeddings:
    """Azure OpenAIの埋め込みモデルを初期化する。"""

    try:
        deployment_name = EMBEDDING_MODELS[DEFAULT_EMBEDDING_MODEL]
    except KeyError as exc:
        raise ValueError(
            f"埋め込みモデルの設定が見つかりません: "
            f"{DEFAULT_EMBEDDING_MODEL}"
        ) from exc

    return AzureOpenAIEmbeddings(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_deployment=deployment_name,
    )
