from app.embedder import retrieve_top_k
import openai

# Use Ollama locally via OpenAI-compatible API
openai.api_key = "ollama"
openai.api_base = "http://localhost:11434/v1"  # Ollama local endpoint

def generate_answer(query, retrieved_contexts):
    context_text = "\n\n".join([f"{i+1}. {chunk['text']}" for i, chunk in enumerate(retrieved_contexts)])

    prompt = f"""Answer the following legal question using the provided context.
Only use the context below to answer. If the context does not help, say you don’t know.

Context:
{context_text}

Question: {query}
Answer:"""

    response = openai.ChatCompletion.create(
        model="mistral",  # or "llama3" if you downloaded that
        messages=[
            {"role": "system", "content": "You are a helpful legal assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )

    return response['choices'][0]['message']['content']
