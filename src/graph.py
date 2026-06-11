from langgraph.graph import StateGraph
from src.schema import ChronoRAGState
from src.agents import (
    retrieve_documents,
    detect_anachronisms,
    garbage_collector,
    generate_answer,
)


def route_after_detection(state: ChronoRAGState) -> str:
    if state.conflict_detected:
        return "garbage_collector"
    return "synthesizer"


def build_graph() -> StateGraph:
    builder = StateGraph(ChronoRAGState)

    builder.add_node("retriever", retrieve_documents)
    builder.add_node("detector", detect_anachronisms)
    builder.add_node("garbage_collector", garbage_collector)
    builder.add_node("synthesizer", generate_answer)

    builder.set_entry_point("retriever")

    builder.add_edge("retriever", "detector")
    builder.add_conditional_edges(
        "detector",
        route_after_detection,
        {
            "garbage_collector": "garbage_collector",
            "synthesizer": "synthesizer",
        },
    )
    builder.add_edge("garbage_collector", "synthesizer")
    builder.set_finish_point("synthesizer")

    return builder.compile()
