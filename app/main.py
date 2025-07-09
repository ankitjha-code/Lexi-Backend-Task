from fastapi import FastAPI
from pydantic import BaseModel
from app.embedder import retrieve_top_k
from app.rag_pipeline import generate_answer

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def get_rag_response(body: QueryRequest):
    query = body.query
    chunks = retrieve_top_k(query, k=3)
    answer = generate_answer(query, chunks)

    return {
        "answer": answer,
        "citations": chunks
    }
