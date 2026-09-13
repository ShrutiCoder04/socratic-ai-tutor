"""Deterministic verification orchestrator.

Runs math and code verification tools on each step.
"""

from typing import List
from agents.state import TutorState, StepVerification
from tools.math_verifier import verify_math_step
from tools.code_sandbox import verify_code_step

def run_verification(state: TutorState, expectations: List[str]) -> TutorState:
    """
    Runs deterministic verification on each parsed step.
    
    Args:
        state: Current TutorState with parsed_steps
        expectations: Expected outputs/forms for each step
    
    Returns:
        Updated TutorState with verification results
    """
    
    state.verifications = []
    
    for i, step in enumerate(state.parsed_steps):
        expected = expectations[i] if i < len(expectations) else "Verification pending"
        
        if state.submission_type == "math":
            is_correct, diagnostic = verify_math_step(step, expected)
        elif state.submission_type == "code":
            is_correct, diagnostic = verify_code_step(step, expected)
        else:
            is_correct, diagnostic = False, "Unknown submission type"
        
        verification = StepVerification(
            step_number=i + 1,
            raw_content=step,
            is_correct=is_correct,
            diagnostic_details=diagnostic
        )
        state.verifications.append(verification)
        
        # Identify first error
        if not is_correct and state.active_error_step is None:
            state.active_error_step = i + 1
    
    # Mark as resolved if all steps are correct
    state.resolved = all(v.is_correct for v in state.verifications)
    
    return state
