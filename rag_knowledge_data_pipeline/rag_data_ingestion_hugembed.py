import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from app.config import settings

load_dotenv()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

PINECONE_API_KEY = settings.pinecone_api_key
PINECONE_ENV = settings.pinecone_env
INDEX_NAME = "rag-customer-bot-huggingface"


def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def extract_txt_text(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_pdf_text(file_path)
    elif ext == ".txt":
        return extract_txt_text(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.split_text(text)

def embed_text(chunks):
    embeddings = model.encode(chunks, convert_to_numpy=True)
    return embeddings


def upload_to_pinecone(chunks, embeddings):
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Create index if not exists
    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=INDEX_NAME,
            dimension=len(embeddings[0]),
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            ),
        )

    index = pc.Index(INDEX_NAME)

    vectors = []
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        vectors.append({
            "id": f"chunk-{i}",
            "values": emb.tolist(),  # Convert numpy array to list
            "metadata": {"text": chunk}
        })

    index.upsert(vectors)



if __name__ == "__main__":
    file_path = "kb_doc_support.txt"  # Can be PDF or TXT

    print("Extracting text...")
    text = extract_text(file_path)

    print("Splitting into chunks...")
    chunks = split_text(text)

    print("Generating embeddings with MiniLM...")
    embeddings = embed_text(chunks)

    print("Uploading to Pinecone...")
    upload_to_pinecone(chunks, embeddings)

    print("Done! File uploaded to Pinecone.")
