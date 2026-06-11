# Amnesia Semántica

Sistema multi-agente con LangGraph y RAG que actúa como un **recolector de basura semántica**: recupera documentos de una base de datos vectorial, analiza sus contenidos y fechas para detectar contradicciones lógicas (anacronismos) y depura automáticamente la información obsoleta antes de responder.

## ¿Cómo funciona?

Cuando un usuario realiza una consulta, el sistema orquesta una pipeline de cuatro agentes especializados conectados mediante un grafo de estado (`StateGraph`):

1. **Retriever** — Convierte la consulta a un vector con all-MiniLM-L6-v2 y busca los documentos más relevantes en ChromaDB filtrando solo los activos.
2. **Detector** — Envía los documentos recuperados a GPT-5 para que analice si dos o más políticas corporativas tratan el mismo tema con reglas contradictorias en fechas distintas. Si detecta un conflicto, identifica el documento más antiguo como obsoleto.
3. **Garbage Collector** — Solo se activa si hay conflicto. Conecta a ChromaDB y actualiza los metadatos del documento antiguo cambiando su estado a `obsolete`, asegurando que no vuelva a aparecer en futuras consultas.
4. **Synthesizer** — Redacta una respuesta final en lenguaje natural usando GPT-5, basándose exclusivamente en los documentos vigentes y mencionando si hubo una limpieza automática.

El sistema está diseñado para mantener la coherencia temporal de una base de conocimiento corporativa. Al detectar automáticamente políticas reemplazadas y marcarlas como obsoletas, garantiza que las respuestas siempre reflejen la versión más reciente de cada norma.

```
Usuario → Retriever → Detector (GPT-5) → Garbage Collector → Synthesizer (GPT-5)
                    ↘ (sin conflicto) ↗
```

## Requisitos

- Python 3.11+
- API key de OpenAI

## Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd amnesia-semantica

# 2. Crear y activar entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar API key
cp .env.template .env
# Editar .env y pegar tu API key de OpenAI
```

## Uso

```bash
python main.py
```

La primera ejecución descarga automáticamente el modelo de embeddings all-MiniLM-L6-v2 (~80 MB) necesario para ChromaDB.

## Configuración

| Variable | Valor por defecto | Descripción |
|---|---|---|
| `OPENAI_API_KEY` | — | API key de OpenAI (requerida) |
| `LLM_MODEL_NAME` | `gpt-5` | Modelo LLM a utilizar |
