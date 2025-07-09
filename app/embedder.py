from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def build_faiss_index(documents, index_path="vector_store"):
    if not os.path.exists(index_path):
        os.makedirs(index_path)

    all_chunks = []
    metadata = []

    for doc in documents:
        chunks = chunk_text(doc['text'])
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            metadata.append({
                "source": doc["filename"],
                "chunk_id": i
            })

    embeddings = model.encode(all_chunks)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index
    faiss.write_index(index, f"{index_path}/faiss.index")

    # Save metadata + original chunks
    with open(f"{index_path}/metadata.pkl", "wb") as f:
        pickle.dump((all_chunks, metadata), f)


def load_faiss_index(index_path="vector_store"):
    index = faiss.read_index(f"{index_path}/faiss.index")
    with open(f"{index_path}/metadata.pkl", "rb") as f:
        texts, metadata = pickle.load(f)
    return index, texts, metadata

def retrieve_top_k(query, k=3, index_path="vector_store"):
    index, texts, metadata = load_faiss_index(index_path)
    query_embedding = model.encode([query])
    scores, indices = index.search(query_embedding, k)

    results = []
    for i in indices[0]:
        results.append({
            "text": texts[i],
            "source": metadata[i]["source"]
        })

    return results
