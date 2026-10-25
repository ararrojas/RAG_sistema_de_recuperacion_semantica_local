import os

from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from ingest import COLLECTION_NAME, PERSIST_DIR, get_embeddings

TOP_K = 4


class RagResponse(BaseModel):
    answer: str = Field(description="Respuesta a la pregunta, basada solo en el contexto")
    references: list[str] = Field(
        description="Nombres de los archivos del contexto usados para responder; lista vacía si no se sabe"
    )


def get_retriever(top_k: int = TOP_K) -> BaseRetriever:
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(PERSIST_DIR),
        client_settings=Settings(anonymized_telemetry=False),
    )
    return vectorstore.as_retriever(search_kwargs={"k": top_k})


def format_docs(docs: list[Document]) -> str:
    return "\n\n".join(
        f"[Fuente: {doc.metadata['source']}]\n{doc.page_content}" for doc in docs
    )


SYSTEM_PROMPT = """Eres un asistente técnico. Responde SOLO con la información del CONTEXTO.
No uses conocimiento externo ni inventes datos.
Si la respuesta no está en el CONTEXTO, responde exactamente "No lo sé" en el campo answer y deja references vacío.
En references indica los nombres de los archivos del CONTEXTO que usaste.

{format_instructions}"""

parser = PydanticOutputParser(pydantic_object=RagResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "CONTEXTO:\n{context}\n\nPREGUNTA: {question}"),
    ]
).partial(format_instructions=parser.get_format_instructions())


def get_llm() -> ChatGoogleGenerativeAI:
    model = os.getenv("GEMINI_LLM_MODEL", "gemini-3.8-flash")
    return ChatGoogleGenerativeAI(model=model, temperature=0)


def build_chain() -> Runnable:
    return (
        {"context": get_retriever() | format_docs, "question": RunnablePassthrough()}
        | prompt
        | get_llm()
        | parser
    )


async def get_rag_response(query: str) -> RagResponse:
    return await build_chain().ainvoke(query)
