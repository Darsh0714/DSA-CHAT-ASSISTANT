import pickle

from src.ingestion.pdf_reader import read_pdf
from src.ingestion.chunker import create_chunks

from src.retrieval.embeddings_generator import generate_embeddings

from src.retrieval.vector_store import (
    create_index,
    add_embeddings,
    save_index
)


PDF_PATH = r"C:\\Users\\YourPC\Downloads\\PDF_Folder\\DSA.pdf"

INDEX_PATH = "data/faiss.index"
CHUNKS_PATH = "data/chunks.pkl"


# 1. Read PDF
pages = read_pdf(PDF_PATH)

print(f"Pages: {len(pages)}")


# 2. Create chunks
chunks = create_chunks(pages, 100)

print(f"Chunks: {len(chunks)}")


# 3. Generate embeddings
embeddings = generate_embeddings(chunks)

print(f"Embeddings shape: {embeddings.shape}")


# 4. Create FAISS index
index = create_index(384)


# 5. Add embeddings
index = add_embeddings(index, embeddings)


# 6. Save FAISS index
save_index(index, INDEX_PATH)


# 7. Save chunks
with open(CHUNKS_PATH, "wb") as file:
    pickle.dump(chunks, file)


print("FAISS index saved.")
print("Chunks saved.")
