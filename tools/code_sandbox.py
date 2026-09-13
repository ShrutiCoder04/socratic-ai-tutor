import sys
import io
import contextlib
from typing import Tuple

def execute_code_safely(code_str: str, timeout_seconds: int = 3) -> Tuple[bool, str]:
    """
    Executes student code within an isolated buffer environment and captures standard output/errors.
    """
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    
    # Simple safe environment globals
    safe_globals = {
        "__builtins__": {
            "range": range,
            "len": len,
            "print": print,
            "int": int,
            "float": float,
            "str": str,
            "list": list,
            "dict": dict,
            "set": set,
            "min": min,
            "max": max,
            "sum": sum,
            "abs": abs,
        }
    }
    
    try:
        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
            exec(code_str, safe_globals)
        return True, stdout_buffer.getvalue().strip()
    except Exception as e:
        return False, f"Runtime Error: {type(e).__name__} - {str(e)}"
