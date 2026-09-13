from tools.math_verifier import verify_math_equivalence
from tools.code_sandbox import execute_code_safely
from agents.state import TutorState, StepVerification

def run_verification(state: TutorState, expectations: list) -> TutorState:
    """
    Iterates over parsed steps and verifies each with external deterministic tools.
    """
    state.verifications = []
    state.active_error_step = None
    
    for idx, step in enumerate(state.parsed_steps):
        expected = expectations[idx] if idx < len(expectations) else ""
        
        if state.submission_type == "math":
            is_valid, msg = verify_math_equivalence(step, expected)
        else:
            is_valid, msg = execute_code_safely(step)
            
        verification = StepVerification(
            step_number=idx + 1,
            raw_content=step,
            is_correct=is_valid,
            diagnostic_details=msg
        )
        state.verifications.append(verification)
        
        # Locate first error
        if not is_valid and state.active_error_step is None:
            state.active_error_step = idx + 1
            
    state.resolved = (state.active_error_step is None)
    return state
