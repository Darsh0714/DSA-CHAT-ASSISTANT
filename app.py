import pickle

from src.retrieval.vector_store import (
    load_index,
    search_index,
    retrieve_chunks
)

from src.retrieval.embeddings_generator import generate_query_embedding
from src.llm.llm_generator import generate_answer


# 1. Load saved FAISS index
index = load_index("data/faiss.index")


# 2. Load saved chunks
with open("data/chunks.pkl", "rb") as file:
    chunks = pickle.load(file)


print("RAG system loaded successfully.")
print("Type 'exit' to stop the assistant.")

while True:

    # 1. Ask user a question
    query = input("\nYou: ")

    # 2. Exit condition
    if query.lower() == "exit":
        print("Assistant: Goodbye!")
        break

    # 3. Generate query embedding
    query_embedding = generate_query_embedding(query)

    # 4. Search FAISS
    distances, indices = search_index(
        index,
        query_embedding,
        3
    )

    # 5. Retrieve relevant chunks
    retrieved_chunks = retrieve_chunks(
        chunks,
        indices,
        distances
    )

    # 6. Build context
    context = ""

    for result in retrieved_chunks:
        context += result["chunk"]["text"] + "\n\n"

    # 7. Generate answer
    answer = generate_answer(
        query,
        context
    )

    # 8. Display answer
    print("\nAssistant:", answer)