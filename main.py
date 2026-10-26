from src.rag.retrieval import retrieve_documents
from src.rag.generation import generate_answer

question = "10月17,18日との学びは何ですか？"

# Retrieval
documents = retrieve_documents(
    question=question,
    k=3,
)

# Generation
answer = generate_answer(
    question=question,
    documents=documents,
    model_name="mini",
)

print(answer)