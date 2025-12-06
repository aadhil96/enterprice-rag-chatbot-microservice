import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# 1. Azure OpenAI Embeddings Setup
# -----------------------------
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")

embedding_function = AzureOpenAIEmbeddings(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_deployment=AZURE_EMBEDDING_DEPLOYMENT
)

# -----------------------------
# 2. Pinecone Setup
# -----------------------------
PINECONE_API_KEY = "pcsk_ETWrN_37yEWTqjw6Shup7CRemByR7BaGjdcC2eXTWTEQxTh6pJDgLvemQamNktmKkA2mh"
PINECONE_ENV = "https://developer-quickstart-py-oz2lrcq.svc.aped-4627-b74a.pinecone.io"
INDEX_NAME = "rag-customer-bot-azure"


# -----------------------------
# 3. File Extraction Functions
# -----------------------------
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


# -----------------------------
# 4. Split Text into Chunks
# -----------------------------
def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    return splitter.split_text(text)


# -----------------------------
# 5. Embed Text
# -----------------------------
def embed_text(chunks):
    embeddings = embedding_function.embed_documents(chunks)
    return embeddings


# -----------------------------
# 6. Upload to Pinecone
# -----------------------------
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
            "values": emb,
            "metadata": {"text": chunk}
        })

    index.upsert(vectors)


# -----------------------------
# 7. Main
# -----------------------------
if __name__ == "__main__":
    file_path = "kb_doc_support.txt"  # Can be PDF or TXT

    print("Extracting text...")
    text = extract_text(file_path)

    print("Splitting into chunks...")
    chunks = split_text(text)

    print("Generating embeddings...")
    embeddings = embed_text(chunks)

    print("Uploading to Pinecone...")
    upload_to_pinecone(chunks, embeddings)

    print("Done! File uploaded to Pinecone.")
