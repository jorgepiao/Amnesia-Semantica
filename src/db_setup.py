import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "corporate_policies"


def get_chroma_client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(
        path=CHROMA_PATH, settings=Settings(anonymized_telemetry=False)
    )


def get_or_create_collection(client: chromadb.PersistentClient):
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    return client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
        embedding_function=DefaultEmbeddingFunction(),
    )


def seed_documents(collection):
    documents = [
        {
            "id": "policy_travel_2023",
            "content": (
                "Política de Reembolso de Viajes 2023:\n"
                "Los viáticos se reembolsan al 80% del total presentando factura física.\n"
                "Se requiere aprobación del gerente directo para gastos mayores a $500."
            ),
            "metadata": {
                "timestamp": "2023-06-01",
                "status": "active",
                "title": "Política de Reembolso de Viajes 2023",
            },
        },
        {
            "id": "policy_travel_2026",
            "content": (
                "Política de Reembolso de Viajes 2026:\n"
                "Los viáticos se reembolsan al 100% del total presentando factura digital.\n"
                "Se requiere aprobación del gerente directo para gastos mayores a $1000.\n"
                "Los gastos de hotel tienen un tope de $200 por noche."
            ),
            "metadata": {
                "timestamp": "2026-01-15",
                "status": "active",
                "title": "Política de Reembolso de Viajes 2026",
            },
        },
        {
            "id": "policy_vacations_2025",
            "content": (
                "Política de Vacaciones 2025:\n"
                "Los empleados tienen derecho a 15 días hábiles de vacaciones al año.\n"
                "Las vacaciones deben solicitarse con al menos 2 semanas de anticipación."
            ),
            "metadata": {
                "timestamp": "2025-03-10",
                "status": "active",
                "title": "Política de Vacaciones 2025",
            },
        },
    ]

    existing_ids = set(collection.get()["ids"]) if collection.count() > 0 else set()
    new_docs = [d for d in documents if d["id"] not in existing_ids]

    if new_docs:
        collection.add(
            ids=[d["id"] for d in new_docs],
            documents=[d["content"] for d in new_docs],
            metadatas=[d["metadata"] for d in new_docs],
        )
        print(f"Seed: inserted {len(new_docs)} documents")
    else:
        print("Seed: collection already populated, skipping")

    return collection


def initialize_db():
    client = get_chroma_client()
    collection = get_or_create_collection(client)
    seed_documents(collection)
    return client, collection


if __name__ == "__main__":
    initialize_db()
    print("Database initialized successfully.")
