from app.loader import load_documents
from app.embedder import build_faiss_index

docs = load_documents("data")
build_faiss_index(docs)

print("✅ FAISS index built and saved to /vector_store")
