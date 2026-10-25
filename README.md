# RAG con LangChain, ChromaDB y Gemini

Sistema RAG (Retrieval-Augmented Generation) de extremo a extremo. Recibe una pregunta, busca los fragmentos más relevantes en una base vectorial y genera una respuesta que usa **exclusivamente** esa información. Si la respuesta no está en los documentos, el modelo responde "No lo sé".

El dataset de ejemplo es un manual técnico **ficticio** (gateway industrial AtlasNode G7), de modo que el modelo no puede conocer los datos por su cuenta: si responde bien, es gracias al contexto recuperado.

## Estructura

```
.
├── data/                    # Dataset: 4 archivos .md del manual
├── ingest.py                # Ingesta: carga, chunking, embeddings y ChromaDB
├── rag.py                   # Retriever, prompt, cadena LCEL y get_rag_response()
├── ask.py                   # Ejecuta las dos preguntas de prueba
├── test_ingest.py           # Tests de la ingesta
├── test_rag.py              # Tests del retriever, el prompt y la cadena
├── run_tests.sh             # Ejecuta todos los tests con pytest
├── requirements.txt
├── .env.example             # Plantilla de variables de entorno
└── vectorstore/             # Base vectorial (se genera sola, no se sube a git)
```

## Requisitos

- Python 3.10 o superior (probado con 3.14).
- Una API key gratuita de Gemini: <https://aistudio.google.com> → *Get API key*.

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edita `.env` y pega tu llave en `GOOGLE_API_KEY`. El archivo `.env` está en `.gitignore`: **nunca se sube al repositorio**.

| Variable | Para qué sirve |
|---|---|
| `GOOGLE_API_KEY` | Tu llave de la API de Gemini |
| `GEMINI_LLM_MODEL` | Modelo que genera la respuesta (`gemini-3.8-flash`) |
| `GEMINI_EMBED_MODEL` | Modelo de embeddings (`gemini-embedding-001`) |

Los nombres de modelo de Google cambian con el tiempo. Si la API devuelve un error de modelo no encontrado, consulta los modelos disponibles para tu cuenta y actualiza el `.env`.

## Uso

**1. Ingesta.** Lee `data/`, fragmenta los documentos y los guarda en `vectorstore/`:

```bash
python ingest.py
```

Si la base ya existe, el script no reindexa. Para reindexar desde cero (por ejemplo, tras cambiar los documentos), borra la carpeta `vectorstore/` y vuelve a ejecutarlo.

**2. Preguntas de prueba.** Ejecuta una pregunta con respuesta en los documentos y una pregunta trampa:

```bash
python ask.py
```

**3. Tests automáticos:**

```bash
./run_tests.sh
```

Los tests que usan el LLM tardan unos 30 segundos cada uno, y todos los que usan embeddings o LLM necesitan internet y la llave configurada.

Para usar el sistema desde tu propio código:

```python
import asyncio
from rag import get_rag_response

respuesta = asyncio.run(get_rag_response("¿Cuánto dura el reset?"))
print(respuesta.answer, respuesta.references)
```

## Cómo funciona

```
 data/*.md
    │  load_documents()       lee los archivos
    ▼
 Document (texto + source)
    │  split_documents()      RecursiveCharacterTextSplitter, 500 tokens, 50 de solape
    ▼
 chunks
    │  build_vectorstore()    embeddings de Gemini + ChromaDB persistente
    ▼
 vectorstore/

 Pregunta
    │  retriever              pregunta → embedding → búsqueda por similitud (top_k = 4)
    ▼
 format_docs()                une los chunks e incluye [Fuente: archivo]
    │  prompt                 reglas anti-alucinación + esquema JSON
    ▼
 LLM (Gemini)
    │  PydanticOutputParser
    ▼
 RagResponse(answer, references)
```

La cadena está escrita con LCEL en `rag.py`:

```python
{"context": get_retriever() | format_docs, "question": RunnablePassthrough()}
| prompt | get_llm() | parser
```

`get_rag_response(query)` la invoca de forma asíncrona (`ainvoke`) y devuelve un objeto `RagResponse` validado con Pydantic.

## Decisiones de diseño

- **Chunking por tokens.** `RecursiveCharacterTextSplitter.from_tiktoken_encoder` con `chunk_size=500` y `chunk_overlap=50`. El tokenizador de `tiktoken` (`cl100k_base`) es el de OpenAI, así que para Gemini el conteo es una aproximación. Prefiere cortar entre párrafos, por lo que el tamaño es un máximo y los chunks suelen ser algo más cortos. El solape solo actúa sobre trozos finales de menos de 50 tokens (en este dataset, sobre todo los títulos de sección).
- **Mismo modelo de embeddings para indexar y consultar.** `get_embeddings()` es la única función que lo define, y la usan tanto `ingest.py` como `rag.py`. Así no se pueden mezclar dos modelos por descuido.
- **`top_k = 4`.** Dentro del rango recomendado (3 a 5) para no saturar el contexto del modelo.
- **Persistencia.** `vectorstore_exists()` comprueba que la colección exista y tenga elementos antes de indexar, para no repetir trabajo ni duplicar datos.
- **Salida estructurada.** `RagResponse` tiene `answer` y `references` (nombres de archivo). El `PydanticOutputParser` valida el formato.
- **Telemetría de ChromaDB desactivada** (`anonymized_telemetry=False`).
- **Temperatura 0** en el LLM, para respuestas lo más deterministas posible.

## Resultados de las pruebas

Ejecutadas con `python ask.py`:

| Pregunta | Respuesta | Referencias |
|---|---|---|
| ¿Cuánto tiempo hay que mantener pulsado el botón RESET? | Se debe mantener pulsado el botón RESET durante 10 segundos. | `03_mantenimiento.md`, `04_solucion_problemas.md` |
| ¿Cuál es el precio del AtlasNode G7? (trampa) | No lo sé | ninguna |

En la pregunta trampa, el retriever igualmente devuelve 4 fragmentos (siempre devuelve `k` resultados, sean relevantes o no). Es el prompt el que evita la alucinación: el modelo reconoce que el contexto no contiene el precio y responde "No lo sé".

## Limitaciones

- El dataset es pequeño (4 documentos, 10 chunks), así que `top_k = 4` recupera cerca de la mitad de la base. En un corpus real la recuperación sería mucho más selectiva.
- Los fragmentos y las preguntas se envían a la API de Google. No uses este proyecto con documentos confidenciales sin revisar esa política.
- El modelo `gemini-3.8-flash` tarda alrededor de 30 segundos por respuesta.
