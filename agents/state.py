from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class StepVerification:
    """Represents the verification result for a single step."""
    step_number: int
    raw_content: str
    is_correct: bool
    diagnostic_details: str

@dataclass
class TutorState:
    """Maintains the session state for the tutoring loop."""
    submission_type: str = "math"  # "math" or "code"
    parsed_steps: List[str] = field(default_factory=list)
    step_expectations: List[str] = field(default_factory=list)
    verifications: List[StepVerification] = field(default_factory=list)
    active_error_step: Optional[int] = None
    hint_tier: int = 1  # 1-4 scaffolding levels
    resolved: bool = False
    conversation_history: List[Dict[str, str]] = field(default_factory=list)
