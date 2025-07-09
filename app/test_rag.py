from app.rag_pipeline import generate_answer
from app.embedder import retrieve_top_k

query = "Is an insurance company liable to pay compensation if a transport vehicle had no valid permit?"

chunks = retrieve_top_k(query, k=3)
answer = generate_answer(query, chunks)

print("🧠 Answer:\n", answer)
print("\n📚 Citations:")
for c in chunks:
    print(f"- From {c['source']}:\n  {c['text'][:200]}...\n")
