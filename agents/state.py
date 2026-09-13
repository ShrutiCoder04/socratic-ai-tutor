from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class StepVerification(BaseModel):
    step_number: int
    raw_content: str
    is_correct: bool
    diagnostic_details: str

class TutorState(BaseModel):
    submission_type: str = "math"  # "math" or "code"
    raw_submission: str = ""
    parsed_steps: List[str] = Field(default_factory=list)
    verifications: List[StepVerification] = Field(default_factory=list)
    active_error_step: Optional[int] = None
    hint_tier: int = 1  # Tier 1 (Location) -> Tier 2 (Socratic) -> Tier 3 (Sub-problem) -> Tier 4 (Escalate)
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)
    resolved: bool = False
