import chromadb
import tiktoken
from chromadb.config import Settings

import ingest
from ingest import (
    CHUNK_SIZE,
    build_vectorstore,
    get_embeddings,
    load_documents,
    split_documents,
    vectorstore_exists,
)


def test_load_documents_reads_all_files():
    docs = load_documents()
    assert len(docs) == 4
    assert all(doc.metadata["source"].endswith(".md") for doc in docs)


def test_split_documents_respects_chunk_size():
    chunks = split_documents(load_documents())
    encoding = tiktoken.get_encoding("cl100k_base")
    assert len(chunks) == 10
    assert all(len(encoding.encode(c.page_content)) <= CHUNK_SIZE for c in chunks)
    assert all("source" in c.metadata for c in chunks)


def test_get_embeddings_returns_vector():
    vector = get_embeddings().embed_query("boton RESET")
    assert len(vector) == 3072


def test_vectorstore_is_built_once(tmp_path, monkeypatch):
    monkeypatch.setattr(ingest, "PERSIST_DIR", tmp_path / "vectorstore")
    assert not vectorstore_exists()

    build_vectorstore(split_documents(load_documents()))
    assert vectorstore_exists()

    client = chromadb.PersistentClient(
        path=str(tmp_path / "vectorstore"),
        settings=Settings(anonymized_telemetry=False),
    )
    assert client.get_collection(ingest.COLLECTION_NAME).count() == 10


def test_main_skips_ingestion_when_store_exists(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(ingest, "PERSIST_DIR", tmp_path / "vectorstore")
    ingest.main()
    ingest.main()
    output = capsys.readouterr().out
    assert "4 documentos -> 10 chunks" in output
    assert "ya existe" in output
