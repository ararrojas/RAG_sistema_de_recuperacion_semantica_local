import asyncio

from rag import get_rag_response

QUESTIONS = [
    "¿Cuánto tiempo hay que mantener pulsado el botón RESET?",
    "¿Cuál es el precio del AtlasNode G7?",
]


async def main() -> None:
    for query in QUESTIONS:
        response = await get_rag_response(query)
        print(f"Pregunta: {query}")
        print(f"Respuesta: {response.answer}")
        print(f"Referencias: {', '.join(response.references) or 'ninguna'}\n")


if __name__ == "__main__":
    asyncio.run(main())
