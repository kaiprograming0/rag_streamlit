
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate


PROJECT_ROOT = Path(__file__).resolve().parents[3]
PROMPT_PATH = PROJECT_ROOT / "prompt" / "answer_generation.prompt"

RAG_SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")



from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate


PROJECT_ROOT = Path(__file__).resolve().parents[3]
PROMPT_PATH = PROJECT_ROOT / "prompt" / "answer_generation.prompt"

RAG_SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")


def create_rag_prompt() -> ChatPromptTemplate:
    """RAG用のプロンプトテンプレートを生成する。"""

    return ChatPromptTemplate.from_messages(
        [
            ("system", RAG_SYSTEM_PROMPT),
            ("human","""
## 過去の会話
{chat_history}

## 今回の質問
{question}

## 参考文書
{context}
""",
            ),
        ]
    )

'''
def create_rag_prompt() -> ChatPromptTemplate:
    """RAG用のプロンプトテンプレートを生成する。"""

    return ChatPromptTemplate.from_messages(
        [
            ("system", RAG_SYSTEM_PROMPT),
            ("human", "{question}"),
        ]
    )
'''