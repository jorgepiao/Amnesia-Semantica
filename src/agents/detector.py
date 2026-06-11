import json
from typing import List
from src.schema import ChronoRAGState, RetrievedDocument, DetectorOutput
from src.llm import llm


def _llm_detect(docs: List[RetrievedDocument]) -> DetectorOutput:
    if len(docs) < 2:
        return DetectorOutput(conflict_detected=False)

    docs_text = "\n\n---\n\n".join(
        f"ID: {d.doc_id}\nTimestamp: {d.timestamp}\nContenido:\n{d.content}"
        for d in docs
    )

    system_prompt = (
        "Eres un analista de políticas corporativas. "
        "Tu tarea es detectar contradicciones lógicas entre documentos "
        "que hablen del mismo tema pero tengan fechas distintas. "
        "Debes devolver exclusivamente un JSON con la siguiente estructura:\n"
        '{"conflict_detected": bool, "obsolete_doc_ids": [string], "reasoning": string}\n\n'
        "Reglas:\n"
        "- conflict_detected: true solo si dos o más documentos tratan el mismo tema "
        "y tienen reglas contradictorias\n"
        "- obsolete_doc_ids: lista con los IDs de los documentos más antiguos que "
        "quedan obsoletos (solo los que se contradicen con uno más reciente)\n"
        "- reasoning: explicación breve en español de por qué hay conflicto\n"
        '- Si no hay conflicto, devuelve {"conflict_detected": false, "obsolete_doc_ids": [], "reasoning": ""}'
    )

    user_prompt = (
        f"Analiza los siguientes documentos y determina si hay contradicciones:\n\n{docs_text}"
    )

    raw = llm.chat(system_prompt, user_prompt, max_tokens=400, temperature=0.2)
    data = json.loads(raw)

    return DetectorOutput(
        conflict_detected=data.get("conflict_detected", False),
        obsolete_doc_ids=data.get("obsolete_doc_ids", []),
        reasoning=data.get("reasoning", ""),
    )


def detect_anachronisms(state: ChronoRAGState) -> ChronoRAGState:
    output = _llm_detect(state.retrieved_docs)
    state.conflict_detected = output.conflict_detected
    state.obsolete_doc_ids = output.obsolete_doc_ids
    state.resolution_reasoning = output.reasoning
    return state
