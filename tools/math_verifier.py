"""SymPy-based mathematical verification tool.

Verifies algebraic and calculus steps using symbolic equivalence.
"""

from typing import Tuple
from sympy import *
from sympy.parsing.sympy_parser import parse_expr

def verify_math_step(step_content: str, expected_form: str) -> Tuple[bool, str]:
    """
    Verifies a mathematical step using SymPy symbolic equivalence.
    
    Args:
        step_content: The student's step (e.g., "x + 2 = 5")
        expected_form: Expected result (e.g., "x = 3")
    
    Returns:
        (is_correct, diagnostic_message)
    """
    
    try:
        # Parse both sides
        student_expr = parse_expr(step_content)
        expected_expr = parse_expr(expected_form)
        
        # Check equivalence
        if simplify(student_expr - expected_expr) == 0:
            return True, "Step is mathematically correct."
        else:
            # Provide diagnostic
            simplified = simplify(student_expr)
            return False, f"Expected {expected_expr}, but got {simplified}."
    
    except Exception as e:
        return False, f"Parse error: {str(e)}"
