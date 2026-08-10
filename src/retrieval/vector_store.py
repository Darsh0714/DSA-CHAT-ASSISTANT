import faiss
import numpy as np

def create_index(dimension):
    index = faiss.IndexFlatL2(dimension)
    return index

def add_embeddings(index, embeddings):
    embeddings = np.array(embeddings, dtype=np.float32)
    index.add(embeddings)
    return index

def search_index(index,query_embedding,k):
    query_embedding=np.array(query_embedding,dtype=np.float32).reshape(1,-1)
    distances,indices=index.search(query_embedding,k)
    return distances,indices

def retrieve_chunks(chunks,indices,distances):
    retrieved_chunks=[]
    for i,distance in zip(indices[0],distances[0]):
        retrieved_chunks.append({
            "chunk":chunks[i],
            "distance":distance
            })
    return retrieved_chunks

def save_index(index, path):
    faiss.write_index(index, path)

def load_index(path):
    index = faiss.read_index(path)
    return index