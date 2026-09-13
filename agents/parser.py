"""Multimodal submission parser agent.

Extracts structured steps and expected transformations from images or text.
"""

from typing import Dict, List, Optional, Any
from PIL.Image import Image
from google import genai

def parse_multimodal_submission(
    client: genai.Client,
    image: Optional[Image] = None,
    text_submission: Optional[str] = None
) -> Dict[str, Any]:
    """
    Parses a student submission (image or text) into structured steps.
    
    Args:
        client: Gemini API client
        image: Optional PIL Image of handwritten/diagram work
        text_submission: Optional text input of code or typed derivation
    
    Returns:
        Dict with keys:
        - submission_type: "math" or "code"
        - problem_statement: Extracted problem
        - steps: List of parsed step strings
        - step_expectations: Expected transformations for verification
    """
    
    # Build the prompt
    system_prompt = """
    You are an expert mathematics and code reviewer.
    Extract and structure the student's submission into clear, discrete steps.
    
    For math: Extract each algebraic/calculus/logic step with full expressions.
    For code: Extract each logical block or function call.
    
    Return JSON with:
    {
        "submission_type": "math" or "code",
        "problem_statement": "The original problem",
        "steps": ["Step 1 content", "Step 2 content", ...],
        "step_expectations": ["Expected form or output after step 1", ...]
    }
    
    Ensure step_expectations has exactly as many entries as steps.
    """
    
    # Prepare content for Gemini
    content_parts = [system_prompt]
    
    if image:
        # Convert PIL image to bytes for API
        import io
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        content_parts.append({
            "mime_type": "image/png",
            "data": img_byte_arr.getvalue()
        })
    
    if text_submission:
        content_parts.append(f"Student submission:\n{text_submission}")
    
    # Call Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=content_parts
    )
    
    # Parse JSON response
    import json
    try:
        result = json.loads(response.text)
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        result = {
            "submission_type": "math",
            "problem_statement": text_submission or "Handwritten problem",
            "steps": [text_submission or "Image submitted"],
            "step_expectations": ["Verification pending"]
        }
    
    return result
