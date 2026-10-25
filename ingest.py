import os
from pathlib import Path

import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

DATA_DIR = Path(__file__).parent / "data"
EXTENSIONS = {".md", ".txt"}
PERSIST_DIR = Path(__file__).parent / "vectorstore"
COLLECTION_NAME = "atlasnode_manual"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def load_documents(data_dir: Path = DATA_DIR) -> list[Document]:
    documents = []
    for path in sorted(data_dir.iterdir()):
        if path.suffix.lower() not in EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8")
        documents.append(Document(page_content=text, metadata={"source": path.name}))
    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    model = os.getenv("GEMINI_EMBED_MODEL", "gemini-embedding-001")
    return GoogleGenerativeAIEmbeddings(model=f"models/{model}")


def vectorstore_exists() -> bool:
    if not PERSIST_DIR.exists():
        return False
    client = chromadb.PersistentClient(
        path=str(PERSIST_DIR),
        settings=Settings(anonymized_telemetry=False),
    )
    try:
        return client.get_collection(COLLECTION_NAME).count() > 0
    except Exception:
        return False


def build_vectorstore(chunks: list[Document]) -> Chroma:
    return Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        collection_name=COLLECTION_NAME,
        persist_directory=str(PERSIST_DIR),
        client_settings=Settings(anonymized_telemetry=False),
    )


def main() -> None:
    if vectorstore_exists():
        print("La base vectorial ya existe, se omite la ingesta.")
        return
    documents = load_documents()
    chunks = split_documents(documents)
    build_vectorstore(chunks)
    print(f"{len(documents)} documentos -> {len(chunks)} chunks guardados en {PERSIST_DIR.name}/")


if __name__ == "__main__":
    main()
