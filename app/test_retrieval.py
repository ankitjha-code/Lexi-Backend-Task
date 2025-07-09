from app.embedder import retrieve_top_k

query = "In the light of the above principles, the real report, which would determine whether there was a theft of electricity or not, would be the report of the M & T Laboratory."

results = retrieve_top_k(query, k=3)

for r in results:
    print("📌 Source:", r["source"])
    print("🔹 Text:", r["text"][:300])
    print()
