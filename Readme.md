# 🧠 Lexi Legal RAG Backend

A fully offline Retrieval-Augmented Generation (RAG) backend that takes legal queries, retrieves relevant text from real court judgments (PDF/DOCX), and generates an answer with citations — using **only free and open-source tools**.

---

## ⚙️ Tech Stack

| Component    | Tool                                       |
| ------------ | ------------------------------------------ |
| Backend      | FastAPI                                    |
| Embeddings   | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector Store | FAISS (local)                              |
| LLM          | Ollama (`mistral` / `llama3`)              |
| Parser       | `pdfplumber`, `python-docx`                |

---

## 🚀 Features

- ✅ Upload legal `.pdf` / `.docx` documents
- ✅ Extract & chunk text for semantic search
- ✅ Embed using free SentenceTransformer
- ✅ Query via `/query` endpoint
- ✅ Get generated answer + source citations
- ✅ 100% offline — no paid APIs needed

---

## 📁 Project Structure

lexi.sg-rag-backend-test/
├── app/
│ ├── main.py # FastAPI app
│ ├── loader.py # Document loader
│ ├── embedder.py # Chunking, embeddings, FAISS logic
│ ├── rag_pipeline.py # RAG logic (retrieval + LLM)
│ ├── test_loader.py # Test PDF/DOCX extraction
│ ├── test_rag.py # Test full pipeline
│
├── scripts/
│ └── build_index.py # Build embeddings/index
│
├── data/ # Put your legal documents here
│ ├── example.pdf
│ └── case.docx
│
├── vector_store/ # FAISS index + metadata
├── requirements.txt
└── README.md # You're reading it!

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repo & Set Up Virtual Environment

```bash
git clone https://github.com/<your-username>/lexi.sg-rag-backend-test
cd lexi.sg-rag-backend-test

python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

pip install -r requirements.txt


```

### 2️⃣ Start Ollama (Free Local LLM)

- Download and install Ollama: [https://ollama.com/download](https://ollama.com/download)
- Start the model in your terminal:

```bash
ollama run mistral
```

✅ Ollama listens on `http://localhost:11434` and serves as an OpenAI-compatible local LLM.

- To use a different model (e.g., `llama3`):

```bash
ollama run llama3
```

Then update the model name in `rag_pipeline.py` to `"llama3"`.

---

### 3️⃣ Prepare Documents

Place your legal files in the `/data/` folder:

```
/data/
├── Anil Kumar v. Roop Kumar Sharma.docx
├── Dakshin PSPCL vs. Sudesh Rani.pdf
```

---

### 4️⃣ Build Embedding Index

```bash
python scripts/build_index.py
```

✅ This will:

- Chunk the documents
- Embed them using sentence-transformers
- Store everything in FAISS at `/vector_store`

---

### 5️⃣ Run the Backend

```bash
uvicorn app.main:app --reload
```

Visit the Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 🔍 Example: Use the `/query` Endpoint

**POST** `/query`

**Request:**

```json
{
  "query": "Is an Indian insurance company liable if a vehicle insured in India meets an accident in Nepal?"
}
```

**Response:**

```json
{
  "answer": "Yes, the insurer is liable if...",
  "citations": [
    {
      "text": "Once a vehicle is insured qua third party it is insured for all geographical areas...",
      "source": "Anil Kumar v. Roop Kumar Sharma.docx"
    },
    {
      "text": "Section 149 (3) makes the Insurance Company liable to satisfy the decree...",
      "source": "Anil Kumar v. Roop Kumar Sharma.docx"
    }
  ]
}
```

---

### 🧠 How the RAG Flow Works

- **Document Loading:** PDF & DOCX files are parsed to extract clean text.
- **Chunking:** Text is split into ~300-word segments with overlap.
- **Embedding:** Chunks are embedded using `all-MiniLM-L6-v2`.
- **Vector Store:** FAISS stores embeddings + metadata (file name, chunk ID).

**Query Flow:**

1. User sends a question.
2. Query is embedded and top K similar chunks are retrieved.
3. Chunks + query are sent to Ollama (LLM).
4. Final answer and citations are returned.

---

### ❗ Troubleshooting

- **🐍 Error:** `openai.ChatCompletion.create` fails  
   **Fix:** You may be using `openai` version ≥ 1.0.  
   Downgrade to 0.28 (recommended for Ollama):

  ```bash
  pip uninstall openai
  pip install openai==0.28
  ```

  Or upgrade code to use the new client class.

- **🧠 Ollama gives connection error?**  
   Make sure you ran:

  ```bash
  ollama run mistral
  ```

  Also ensure port `11434` is available.

- **📄 Document parsing issues?**  
   Ensure your files are valid PDF/DOCX formats. Check the `scripts/build_index.py` for any parsing errors.
- **🔍 No results for queries?**  
   Ensure you have built the index with `python scripts/build_index.py` after adding new documents.
- **📦 Missing dependencies?**
  Check your `requirements.txt` file and ensure all packages are installed.
- **📂 Data folder empty?**
  Make sure you have placed your legal documents in the `/data/` folder.
- **❓ Other issues?**
  Check the logs for any errors and ensure all services (Ollama, FastAPI) are running correctly.

---

## 🙏 Acknowledgement

Special thanks to the authors of the libraries and tools used in this project.

## 📞 Contact

For any inquiries, please reach out to [devx.ankitx@gmail.com](mailto:devx.ankitx@gmail.com).
