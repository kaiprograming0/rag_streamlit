
from langchain_core.documents import Document
from pydantic import BaseModel, ConfigDict, Field

from src.rag_core.generation.llm import load_llm
from src.rag_core.generation.prompts import create_rag_prompt



class GenerationRequest(BaseModel):
    """回答生成の入力データ"""

    model_config = ConfigDict(strict=True)

    question: str = Field(min_length=1)


class GenerationResponse(BaseModel):
    """回答生成の出力データ"""

    model_config = ConfigDict(strict=True)

    answer: str = Field(min_length=1)



def generate_answer(
    question: str,
    documents: list[Document],
    chat_history: list[dict[str, str]] | None = None,
) -> str:
    """検索結果を参考文書としてLLMの回答を生成する。"""

    if not isinstance(question, str) or not question.strip():
        raise ValueError("質問を入力してください。")

    if not documents:
        return "質問に関連する参考文書が見つかりませんでした。"

    context = "\n\n".join(
        f"[参考文書 {i}]\n{doc.page_content}"
        for i, doc in enumerate(documents, start=1)
    )

    history_text = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in (chat_history or [])
        if message.get("role") in ("user", "assistant")
        and isinstance(message.get("content"), str)
    )


    prompt = create_rag_prompt()
    llm = load_llm()

    chain = prompt | llm

    response = chain.invoke(
        {
            "question": question.strip(),
            "context": context,
            "chat_history": history_text or "過去の会話はありません。",
        }
    )

    answer = response.content

    if not isinstance(answer, str):
        raise TypeError(
            "LLMの回答が文字列ではありません。"
        )

    return answer