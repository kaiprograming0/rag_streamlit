
from langchain_openai import AzureChatOpenAI

from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_ENDPOINT,
)


# 現在利用しているAzure OpenAIのデプロイ名
CHAT_DEPLOYMENT_NAME = "gpt-4.1-mini-1"


def load_llm() -> AzureChatOpenAI:
    """Azure OpenAIのチャットモデルを初期化する。"""

    return AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_deployment=CHAT_DEPLOYMENT_NAME,
        temperature=0,
    )
