import sympy as sp
from typing import Tuple

def verify_math_equivalence(step_expr_str: str, expected_expr_str: str) -> Tuple[bool, str]:
    """
    Deterministically verifies if a student's derivation step matches the expected transformation
    using SymPy symbolic manipulation to prevent LLM mathematical hallucinations.
    """
    try:
        x, y, z, t, u, v = sp.symbols('x y z t u v')
        
        # Parse expressions safely
        step_expr = sp.sympify(step_expr_str, evaluate=True)
        expected_expr = sp.sympify(expected_expr_str, evaluate=True)
        
        diff = sp.simplify(step_expr - expected_expr)
        
        if diff == 0:
            return True, "Symbolically identical"
        else:
            return False, f"Divergence detected. Difference simplifies to: {diff}"
    except Exception as e:
        return False, f"Parsing / Verification Error: {str(e)}"
