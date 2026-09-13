from google import genai
from google.genai import types
from agents.state import TutorState

def generate_socratic_intervention(client: genai.Client, state: TutorState) -> str:
    """
    Generates a targeted Socratic hint based on the active error step and scaffolding tier.
    Enforces strict zero answer leakage policy.
    """
    if state.resolved:
        return "Excellent job! All steps in your derivation have been verified deterministically."

    error_step_obj = state.verifications[state.active_error_step - 1]
    
    tier_instructions = {
        1: "Tier 1 (Location Cue): Tell the student which line contains a discrepancy, without explaining the specific math rule or giving the correction.",
        2: "Tier 2 (Conceptual Probe): Ask a targeted Socratic guiding question about the mathematical or logical rule applied in this step.",
        3: "Tier 3 (Sub-problem/Isomorphism): Provide a simplified mini-analogy or smaller sub-problem for them to solve.",
        4: "Tier 4 (Escalation): Inform the student that this concept requires human instructor review and summarize the misunderstanding for their teacher."
    }
    
    system_prompt = f"""
    You are an Autonomous Socratic Tutor.
    STRICT POLICY: NEVER reveal the final calculation or direct answer.
    
    Current State:
    - Step with Error: Step {state.active_error_step} -> "{error_step_obj.raw_content}"
    - Tool Diagnostic: {error_step_obj.diagnostic_details}
    - Current Scaffolding Tier: {state.hint_tier} / 4
    - Scaffolding Rule: {tier_instructions.get(state.hint_tier, tier_instructions[1])}
    
    Respond directly to the student in an encouraging, concise tone.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=system_prompt
    )
    return response.text
