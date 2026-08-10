import os
def create_chunks(pages,chunk_size):
    
    chunks=[]
    for page in pages:
        text=page["text"]
        words=text.split()

        for i in range(0,len(words),chunk_size):
            chunk_words=words[i:i + chunk_size]
            chunk_text=" ".join(chunk_words)

            chunks.append({
                "document_name":page["document_name"],
                "page_number":page["page_number"],
                "chunk_number":(i//chunk_size)+1,
                "text":chunk_text
            })
    return chunks 