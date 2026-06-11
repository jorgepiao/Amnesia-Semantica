from src.db_setup import initialize_db
from src.graph import build_graph


def main():
    print("=" * 60)
    print("Amnesia Semántica — Sistema de Depuración Semántica con RAG")
    print("=" * 60)

    initialize_db()
    graph = build_graph()

    query = "¿Cuál es la política de reembolso de viajes?"
    print(f"\nConsulta: '{query}'\n")

    final_state = graph.invoke({"user_query": query})

    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    print(f"Conflicto detectado: {final_state.get('conflict_detected', False)}")
    print(f"IDs obsoletos: {final_state.get('obsolete_doc_ids', [])}")
    print(f"Razonamiento: {final_state.get('resolution_reasoning', 'N/A')}")
    print("\n--- Respuesta para el usuario ---")
    print(final_state.get("final_answer", "Error: no se generó respuesta"))

    print("\n" + "=" * 60)
    print("VERIFICACIÓN: consultando nuevamente (debe ignorar docs obsoletos)...")
    print("=" * 60)

    second_state = graph.invoke({"user_query": query})
    docs_retrieved = len(second_state.get("retrieved_docs", []))
    print(f"Documentos recuperados en segunda consulta: {docs_retrieved}")
    for d in second_state.get("retrieved_docs", []):
        print(f"  - {d.doc_id} (status: {d.status})")

    print("\nPrueba completada exitosamente.")


if __name__ == "__main__":
    main()
