from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from src.schema import ChronoRAGState, RetrievedDocument
from src.db_setup import get_chroma_client, COLLECTION_NAME

TOP_K = 5

_ef = DefaultEmbeddingFunction()


def retrieve_documents(state: ChronoRAGState) -> ChronoRAGState:
    client = get_chroma_client()
    collection = client.get_collection(COLLECTION_NAME)

    query_embedding = _ef([state.user_query])
    if query_embedding is None:
        return state

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=TOP_K,
        where={"status": "active"},
    )

    docs = []
    if results["ids"]:
        for i, doc_id in enumerate(results["ids"][0]):
            metadata = results["metadatas"][0][i] if results["metadatas"] else {}
            content = results["documents"][0][i] if results["documents"] else ""
            docs.append(
                RetrievedDocument(
                    doc_id=doc_id,
                    content=content,
                    timestamp=metadata.get("timestamp", ""),
                    status=metadata.get("status", "active"),
                )
            )

    state.retrieved_docs = docs
    return state
