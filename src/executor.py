"""Safely execute generated pandas code."""

import ast
from dataclasses import dataclass

import pandas as pd

from .common.constants import ALLOWED_BUILTINS, DANGEROUS_ATTRIBUTES, DANGEROUS_FUNCTIONS


@dataclass
class ExecutionResult:
    """Result of code execution."""

    success: bool
    result: pd.DataFrame | pd.Series | object | None = None
    error: str | None = None
    code: str = ""


class SafeCodeExecutor:
    """Execute pandas code in a restricted environment."""

    def __init__(self, dataframes: dict[str, pd.DataFrame]):
        self.dataframes = dataframes

    def validate_code(self, code: str) -> tuple[bool, str]:
        """Validate code for safety using AST analysis."""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error: {e}"

        # Check for dangerous operations
        for node in ast.walk(tree):
            # Block imports
            if isinstance(node, ast.Import | ast.ImportFrom):
                return False, "Imports are not allowed"

            # Block exec/eval calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in DANGEROUS_FUNCTIONS:
                        return False, f"Function '{node.func.id}' is not allowed"

            # Block attribute access to dangerous methods
            if isinstance(node, ast.Attribute):
                if node.attr in DANGEROUS_ATTRIBUTES:
                    return False, f"Attribute '{node.attr}' is not allowed"

        return True, ""

    def execute(self, code: str) -> ExecutionResult:
        """Execute the code and return the result."""
        # Validate first
        is_valid, error_msg = self.validate_code(code)
        if not is_valid:
            return ExecutionResult(success=False, error=error_msg, code=code)

        # Build execution environment
        exec_globals = {
            "__builtins__": ALLOWED_BUILTINS,
            "pd": pd,
        }
        exec_locals = dict(self.dataframes)

        try:
            exec(code, exec_globals, exec_locals)

            # Get the result variable
            if "result" in exec_locals:
                result = exec_locals["result"]
                return ExecutionResult(success=True, result=result, code=code)
            else:
                return ExecutionResult(
                    success=False,
                    error="Code did not produce a 'result' variable",
                    code=code,
                )
        except Exception as e:
            return ExecutionResult(success=False, error=str(e), code=code)
