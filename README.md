# AI-Powered RAG Document Chat Assistant

A local document question-answering system built using Retrieval-Augmented Generation (RAG). The application processes PDF documents, generates semantic embeddings, indexes them using FAISS, retrieves relevant document context for user queries, and generates grounded responses using a locally hosted Phi-3 Mini language model through Ollama.

## Overview

Large Language Models (LLMs) can generate responses using their pretrained knowledge, but they do not automatically have access to private or user-provided documents.

This project addresses that limitation by implementing a Retrieval-Augmented Generation pipeline.

The system:

1. Extracts text from PDF documents.
2. Splits the extracted text into smaller chunks.
3. Converts each chunk into a vector embedding.
4. Stores the embeddings in a FAISS vector index.
5. Converts user questions into embeddings.
6. Retrieves the most relevant document chunks using similarity search.
7. Provides the retrieved context to a local language model.
8. Generates an answer based on the retrieved document information.

## Architecture

```text
                         Document
                            |
                            v
                    PDF Text Extraction
                            |
                            v
                         Chunking
                            |
                            v
                  Sentence Transformer
                     Embedding Model
                            |
                            v
                       FAISS Index
                            |
                     Persistent Storage
                            |
                            v
                       User Query
                            |
                            v
                     Query Embedding
                            |
                            v
                   FAISS Similarity Search
                            |
                            v
                  Relevant Document Chunks
                            |
                            v
                  Query + Retrieved Context
                            |
                            v
                     Phi-3 Mini LLM
                         via Ollama
                            |
                            v
                       Final Answer
```

## Retrieval-Augmented Generation

The application separates the retrieval and generation stages.

### Retrieval

The user's question is converted into an embedding using the same embedding model used for the document chunks. FAISS compares the query vector against the stored document vectors and returns the most relevant chunks.

```text
User Query
    |
    v
Query Embedding
    |
    v
FAISS Similarity Search
    |
    v
Relevant Document Chunks
```

### Generation

The retrieved document chunks are combined into a context and provided to the language model along with the user's question.

```text
User Query + Retrieved Context
              |
              v
          Phi-3 Mini
              |
              v
          Final Answer
```

The prompt instructs the language model to use the retrieved document context and avoid generating information that is not supported by the provided context.

## Technology Stack

| Technology            | Purpose                               |
| --------------------- | ------------------------------------- |
| Python                | Application development               |
| PyMuPDF               | PDF text extraction                   |
| Sentence Transformers | Semantic text embeddings              |
| all-MiniLM-L6-v2      | Embedding model                       |
| FAISS                 | Vector indexing and similarity search |
| Ollama                | Local LLM runtime                     |
| Phi-3 Mini            | Language generation                   |
| NumPy                 | Numerical and vector processing       |

## Project Structure

```text
DSA-CHAT-ASSISTANT/
|
├── app.py
├── README.md
├── requirements.txt
|
└── src/
    |
    ├── config.py
    |
    ├── ingestion/
    |   ├── pdf_reader.py
    |   └── chunker.py
    |
    ├── retrieval/
    |   ├── build_index.py
    |   ├── embeddings_generator.py
    |   └── vector_store.py
    |
    └── llm/
        └── llm_generator.py
```

## Implementation Details

### Document Ingestion

PDF documents are processed and their text content is extracted using PyMuPDF.

### Text Chunking

The extracted document text is divided into smaller chunks to make semantic retrieval more effective.

The current implementation uses a chunk size of approximately 100 words.

### Embedding Generation

Each document chunk is converted into a numerical vector using the `all-MiniLM-L6-v2` Sentence Transformer model.

The current embedding dimension is:

```text
384
```

For the current DSA document, the system generates:

```text
153 pages
311 chunks
311 × 384 embeddings
```

### Vector Indexing

The generated embeddings are stored in a FAISS `IndexFlatL2` index.

FAISS is used to perform efficient vector similarity searches against the document embeddings.

### Query Retrieval

When a user submits a question:

```text
Question
   |
   v
Query Embedding
   |
   v
FAISS Search
   |
   v
Top Relevant Chunks
```

The retrieved chunks are then used as context for the language model.

### Local Language Model

The project uses Phi-3 Mini through Ollama for local text generation.

The model receives:

```text
Context
+
User Question
```

and generates the final response.

## Persistent Indexing

The application separates document indexing from query processing.

The indexing pipeline is executed when the document collection changes:

```text
PDF
 |
 v
Chunks
 |
 v
Embeddings
 |
 v
FAISS Index
 |
 v
Persisted Index
```

The chat application then loads the existing index instead of rebuilding the embeddings for every user query.

This avoids unnecessary embedding generation and improves query-time efficiency.

## Example

### Input

```text
What is binary search?
```

### Retrieval

The system searches the FAISS index and retrieves document chunks containing information related to binary search.

### Generation

The retrieved chunks are passed to Phi-3 Mini as contextual information.

### Output

```text
Binary search is a fast search algorithm with a run-time
complexity of O(log n). It operates based on the
divide-and-conquer strategy.
```

## Running the Project

### Prerequisites

* Python 3.11 or compatible Python version
* Ollama
* Phi-3 Mini model

### Clone the Repository

```bash
git clone https://github.com/Darsh0714/DSA-CHAT-ASSISTANT.git
cd DSA-CHAT-ASSISTANT
```

### Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install the LLM

Install Ollama and download the Phi-3 Mini model:

```bash
ollama pull phi3:mini
```

Ensure the Ollama service is running before starting the application.

### Build the Vector Index

After configuring the document path in the project:

```bash
python -m src.retrieval.build_index
```

This creates the document embeddings and FAISS vector index.

### Start the Assistant

```bash
python app.py
```

The application starts an interactive command-line chat session:

```text
RAG system loaded successfully.
Type 'exit' to stop the assistant.

You: What is binary search?

Assistant: Binary search is a fast search algorithm...
```

Enter `exit` to terminate the application.

## Design Characteristics

### Local Execution

The language model is hosted locally using Ollama rather than relying on a cloud-based LLM API.

### Document-Grounded Responses

The application provides retrieved document context to the LLM and instructs it to use that context when generating responses.

### Persistent Retrieval Layer

The FAISS index is generated separately from the query application, preventing the system from recomputing all document embeddings for every question.

### Modular Architecture

The implementation separates document ingestion, retrieval, embedding generation, vector storage, and LLM generation into independent modules.

## Limitations

The current implementation has several limitations:

* Supports a single configured document workflow.
* Uses a fixed chunk size.
* Uses a fixed number of retrieved chunks.
* Does not currently implement similarity-score thresholding.
* Does not maintain conversational memory between related questions.
* Does not provide source citations in the generated response.
* Uses FAISS `IndexFlatL2`, which performs exact search and may require optimization for very large vector collections.
* The current interface is command-line based.

## Future Improvements

Potential improvements include:

* Streamlit-based web interface
* Multi-document ingestion
* Document metadata filtering
* Similarity-score thresholding
* Conversation memory
* Follow-up question handling
* Query rewriting
* Retrieval reranking
* Source and page citations
* Improved chunking and overlap strategies
* Advanced FAISS indexes for larger datasets
* Automated evaluation of retrieval and answer quality

## Key Concepts

This project demonstrates practical implementation of:

* Retrieval-Augmented Generation
* Semantic Search
* Vector Embeddings
* Vector Databases
* FAISS Similarity Search
* Local LLM Inference
* Prompt Engineering
* PDF Processing
* Context Retrieval
* Persistent Vector Indexing
* Modular Python Application Design

## Author

**Darshini R**

GitHub: https://github.com/Darsh0714
