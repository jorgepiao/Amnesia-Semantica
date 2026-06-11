from pydantic import BaseModel, Field
from typing import List, Optional


class RetrievedDocument(BaseModel):
    doc_id: str
    content: str
    timestamp: str
    status: str = "active"


class DetectorOutput(BaseModel):
    conflict_detected: bool
    obsolete_doc_ids: List[str] = Field(default_factory=list)
    reasoning: str = ""


class ChronoRAGState(BaseModel):
    user_query: str
    retrieved_docs: List[RetrievedDocument] = Field(default_factory=list)
    conflict_detected: bool = False
    obsolete_doc_ids: List[str] = Field(default_factory=list)
    resolution_reasoning: Optional[str] = None
    final_answer: Optional[str] = None
