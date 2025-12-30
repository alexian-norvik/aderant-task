"""General constants for the application."""

# Allowed built-in names for safe code execution
ALLOWED_BUILTINS = {
    "True": True,
    "False": False,
    "None": None,
    "len": len,
    "range": range,
    "str": str,
    "int": int,
    "float": float,
    "list": list,
    "dict": dict,
    "sum": sum,
    "min": min,
    "max": max,
    "abs": abs,
    "round": round,
    "sorted": sorted,
    "enumerate": enumerate,
    "zip": zip,
    "print": print,
}

# Functions that are not allowed in generated code
DANGEROUS_FUNCTIONS = {"exec", "eval", "compile", "open", "__import__"}

# Attributes that are not allowed to be accessed
DANGEROUS_ATTRIBUTES = {"__class__", "__bases__", "__subclasses__", "__globals__"}
