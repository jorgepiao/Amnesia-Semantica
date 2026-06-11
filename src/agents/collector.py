from src.schema import ChronoRAGState
from src.db_setup import get_chroma_client, COLLECTION_NAME


def garbage_collector(state: ChronoRAGState) -> ChronoRAGState:
    if not state.conflict_detected or not state.obsolete_doc_ids:
        return state

    client = get_chroma_client()
    collection = client.get_collection(COLLECTION_NAME)

    for doc_id in state.obsolete_doc_ids:
        try:
            result = collection.get(ids=[doc_id])
            if result["ids"]:
                current_meta = result["metadatas"][0] if result["metadatas"] else {}
                current_meta["status"] = "obsolete"
                collection.update(ids=[doc_id], metadatas=[current_meta])
                print(f"Collector: marcado '{doc_id}' como obsolete")
            else:
                print(f"Collector: '{doc_id}' no encontrado en DB")
        except Exception as e:
            print(f"Collector: error al actualizar '{doc_id}': {e}")

    state.retrieved_docs = [
        d for d in state.retrieved_docs if d.doc_id not in state.obsolete_doc_ids
    ]

    return state
