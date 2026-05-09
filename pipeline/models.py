from pydantic import BaseModel
from typing import Optional, Any

class PipelineResult(BaseModel):
    job_id: str
    extracted_data: dict[str, Any]
    classification: str
    confidence: float
    vector_id: Optional[str] = None
    status: str
    processing_time_ms: Optional[int] = None
