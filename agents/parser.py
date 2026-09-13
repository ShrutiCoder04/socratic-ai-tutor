import json
from google import genai
from google.genai import types
from PIL import Image

def parse_multimodal_submission(client: genai.Client, image: Image.Image = None, text_submission: str = "") -> dict:
    """
    Extracts structured steps from multimodal user artifacts (handwritten images, latex, or code).
    """
    prompt = """
    You are a multimodal assignment parser. Analyze the student's submission.
    Extract the work into a structured JSON response with keys:
    - 'submission_type': either 'math' or 'code'
    - 'problem_statement': brief summary of the problem
    - 'steps': list of individual strings representing each step or line of derivation/code
    - 'step_expectations': list of reference expressions or intended transformations for each step
    Return raw valid JSON only.
    """
    
    contents = [prompt]
    if image is not None:
        contents.append(image)
    if text_submission:
        contents.append(f"Student Text Submission:\n{text_submission}")
        
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    try:
        return json.loads(response.text)
    except Exception:
        return {
            "submission_type": "math",
            "problem_statement": "General Problem",
            "steps": [text_submission or "Uploaded step"],
            "step_expectations": [""]
        }
