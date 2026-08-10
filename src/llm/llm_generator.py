import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3:mini"


def generate_answer(question, context):

    prompt = f"""
You are a document-based AI assistant.

Your job is to answer the user's question using ONLY the provided context.

STRICT RULES:

1. Use only information present in the context.
2. Do not add information from your own knowledge.
3. Do not guess or make assumptions.
4. If the context does not contain the answer, say:
   "I don't have enough information in the provided documents."
5. If the question is incomplete or unclear, say:
   "Please provide a complete question."
6. Keep the answer concise and directly answer the question.

Context:
{context}

User Question:
{question}

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]