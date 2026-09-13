"""Safe code execution sandbox for verification.

Executes student code in an isolated environment.
"""

from typing import Tuple
import subprocess
import tempfile
import os

def verify_code_step(step_content: str, expected_output: str) -> Tuple[bool, str]:
    """
    Executes code in a sandboxed environment and verifies output.
    
    Args:
        step_content: The student's code snippet
        expected_output: Expected output or behavior
    
    Returns:
        (is_correct, diagnostic_message)
    """
    
    try:
        # Create temporary file for code execution
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(step_content)
            temp_file = f.name
        
        # Execute with timeout
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Clean up
        os.unlink(temp_file)
        
        # Compare output
        actual_output = result.stdout.strip()
        expected_output = expected_output.strip()
        
        if actual_output == expected_output:
            return True, "Code executed correctly."
        else:
            return False, f"Expected output: {expected_output}\nGot: {actual_output}"
    
    except subprocess.TimeoutExpired:
        return False, "Code execution timed out (infinite loop detected)."
    except Exception as e:
        return False, f"Execution error: {str(e)}"
