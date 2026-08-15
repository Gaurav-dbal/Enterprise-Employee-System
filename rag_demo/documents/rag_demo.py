import os
import numpy as np
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIGURATION
# ============================================================

DOCUMENT_PATH = "D:/Enterprise-Employee-System/rag_demo/documents/oracle_oic.txt"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

TOP_K = 3


# ============================================================
# 1. LOAD DOCUMENT
# ============================================================

def load_document():

    print("\n========== LOAD DOCUMENT ==========")

    try:

        with open(DOCUMENT_PATH, "r", encoding="utf-8") as file:

            document = file.read()

        print("Document loaded successfully.")
        print(f"Characters : {len(document)}")

        return document

    except FileNotFoundError:

        print("Document not found.")
        return None


# ============================================================
# 2. CHUNK DOCUMENT
# ============================================================

def create_chunks(document):

    print("\n========== CREATE CHUNKS ==========")

    chunks = document.split("\n\n")

    chunks = [
        chunk.strip()
        for chunk in chunks
        if chunk.strip()
    ]

    print(f"Total Chunks : {len(chunks)}")

    for index, chunk in enumerate(chunks):

        print("\n--------------------------------")
        print(f"Chunk {index + 1}")
        print("--------------------------------")
        print(chunk)

    return chunks


# ============================================================
# 3. CREATE EMBEDDINGS
# ============================================================

def create_embeddings(chunks):

    print("\n========== CREATE EMBEDDINGS ==========")

    print("Loading embedding model...")

    model = SentenceTransformer(EMBEDDING_MODEL)

    embeddings = model.encode(chunks)

    print("Embeddings created successfully.")

    print(f"Number of vectors : {len(embeddings)}")
    print(f"Vector dimensions : {embeddings.shape[1]}")

    return model, embeddings


# ============================================================
# 4. CREATE QUERY EMBEDDING
# ============================================================

def create_query_embedding(model, question):

    query_embedding = model.encode([question])

    return query_embedding[0]


# ============================================================
# 5. CALCULATE COSINE SIMILARITY
# ============================================================

def cosine_similarity(vector_a, vector_b):

    numerator = np.dot(vector_a, vector_b)

    denominator = (
        np.linalg.norm(vector_a)
        * np.linalg.norm(vector_b)
    )

    if denominator == 0:

        return 0

    return numerator / denominator


# ============================================================
# 6. SEARCH DOCUMENT
# ============================================================

def search_documents(question, chunks, embeddings, model):

    print("\n========== SEARCH ==========")

    print(f"Question : {question}")

    query_vector = create_query_embedding(
        model,
        question
    )

    results = []

    for index, document_vector in enumerate(embeddings):

        similarity = cosine_similarity(
            query_vector,
            document_vector
        )

        results.append(
            {
                "chunk_id": index + 1,
                "chunk": chunks[index],
                "similarity": similarity
            }
        )

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    top_results = results[:TOP_K]

    print("\n========== TOP RESULTS ==========")

    for result in top_results:

        print("\n--------------------------------")
        print(
            f"Chunk ID    : {result['chunk_id']}"
        )
        print(
            f"Similarity  : {result['similarity']:.4f}"
        )
        print("--------------------------------")
        print(result["chunk"])

    return top_results


# ============================================================
# 7. MAIN PROGRAM
# ============================================================

def main():

    print("\n==========================================")
    print("          SIMPLE RAG DEMO")
    print("==========================================")

    document = load_document()

    if document is None:

        return

    chunks = create_chunks(document)

    model, embeddings = create_embeddings(
        chunks
    )

    while True:

        print("\n==========================================")

        question = input(
            "\nAsk a question "
            "(type 'exit' to quit): "
        )

        if question.lower() == "exit":

            print("\nRAG Demo Finished.")
            break

        search_documents(
            question,
            chunks,
            embeddings,
            model
        )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()