from app.loader import load_documents

docs = load_documents()

for doc in docs:
    print(f"--- {doc['filename']} ---")
    print(doc['text'][:1000])  # print first 1000 chars
    print()
