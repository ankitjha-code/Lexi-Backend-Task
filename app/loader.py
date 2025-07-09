import os
import pdfplumber
import docx

def load_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text

def load_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def load_documents(folder_path="data"):
    documents = []

    for fname in os.listdir(folder_path):
        path = os.path.join(folder_path, fname)

        if fname.endswith(".pdf"):
            text = load_pdf(path)
        elif fname.endswith(".docx"):
            text = load_docx(path)
        else:
            continue  # skip unsupported files

        if text:
            documents.append({
                "filename": fname,
                "text": text
            })

    return documents
