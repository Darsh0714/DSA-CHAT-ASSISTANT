from sentence_transformers import SentenceTransformer

model=SentenceTransformer("all-MiniLM-L6-v2")

print(model)
def generate_embeddings(chunks):
    texts=[]
    for chunk in chunks:
        texts.append(chunk["text"])

    embeddings=model.encode(texts)
    print(embeddings.shape)
    return embeddings
def generate_query_embedding(query):
    query_embedding=model.encode([query])
    return query_embedding