import asyncio

import pytest
from pydantic import ValidationError

import ingest
from langchain_core.documents import Document
from rag import TOP_K, RagResponse, format_docs, get_rag_response, get_retriever, prompt


def test_rag_response_accepts_valid_data():
    response = RagResponse(answer="10 segundos", references=["03_mantenimiento.md"])
    assert response.model_dump() == {
        "answer": "10 segundos",
        "references": ["03_mantenimiento.md"],
    }


def test_rag_response_requires_references():
    with pytest.raises(ValidationError):
        RagResponse(answer="sin referencias")


@pytest.fixture(scope="module")
def retriever():
    ingest.main()
    return get_retriever()


def test_retriever_finds_reset_answer(retriever):
    docs = asyncio.run(retriever.ainvoke("¿Cuánto tiempo hay que mantener pulsado el botón RESET?"))
    assert len(docs) == TOP_K
    assert any("10 segundos" in doc.page_content for doc in docs)


def test_retriever_always_returns_top_k_even_without_answer(retriever):
    docs = asyncio.run(retriever.ainvoke("¿Cuál es el precio del AtlasNode G7?"))
    assert len(docs) == TOP_K
    assert not any("precio" in doc.page_content.lower() for doc in docs)


def test_format_docs_labels_each_chunk_with_its_source():
    docs = [
        Document(page_content="texto uno", metadata={"source": "a.md"}),
        Document(page_content="texto dos", metadata={"source": "b.md"}),
    ]
    assert format_docs(docs) == "[Fuente: a.md]\ntexto uno\n\n[Fuente: b.md]\ntexto dos"


def test_prompt_includes_context_question_and_rules():
    text = prompt.format(context="CTX", question="PREG")
    assert "CTX" in text and "PREG" in text
    assert "No lo sé" in text
    assert "references" in text


def test_answer_found_in_documents(retriever):
    response = asyncio.run(get_rag_response("¿Cuánto tiempo hay que mantener pulsado el botón RESET?"))
    assert "10" in response.answer
    assert "03_mantenimiento.md" in response.references or "04_solucion_problemas.md" in response.references


def test_trap_question_does_not_hallucinate(retriever):
    response = asyncio.run(get_rag_response("¿Cuál es el precio del AtlasNode G7?"))
    assert "no lo sé" in response.answer.lower()
    assert response.references == []
