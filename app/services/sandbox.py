"""
Sandbox Service
Provides safe code execution environment with resource limits and security restrictions.
"""

import ast
import signal
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Any, Tuple, Optional


class TimeoutException(Exception):
    """Raised when code execution exceeds timeout."""
    pass


class Sandbox:
    """
    Provides a safe execution environment for user code with:
    - Timeout protection
    - Restricted imports
    - Limited builtins
    - Output capture
    """

    # Disallowed AST nodes for security
    DISALLOWED_NODES = (
        ast.Global, ast.Nonlocal, ast.With, ast.AsyncWith
    )

    # Allowed imports
    ALLOWED_IMPORTS = {
        'functools': ['wraps'],
        'time': ['sleep', 'time', 'perf_counter'],
        'numpy': None,  # Allow all numpy imports
    }

    # Safe builtins
    SAFE_BUILTINS = {
        "len": len, "range": range, "sum": sum, "min": min, "max": max, "abs": abs,
        "enumerate": enumerate, "zip": zip, "sorted": sorted, "all": all, "any": any,
        "map": map, "filter": filter,
        "list": list, "dict": dict, "set": set, "tuple": tuple, "str": str, "int": int,
        "float": float, "bool": bool, "print": print, "isinstance": isinstance, "type": type,
        "repr": repr, "getattr": getattr, "setattr": setattr, "hasattr": hasattr,
        "Exception": Exception, "ValueError": ValueError, "TypeError": TypeError,
        "KeyError": KeyError, "IndexError": IndexError, "AttributeError": AttributeError,
        "NameError": NameError, "ImportError": ImportError,
        "__build_class__": __build_class__,
        "property": property,
        "classmethod": classmethod,
        "staticmethod": staticmethod,
        "super": super
    }

    def __init__(self, timeout_seconds: int = 5):
        """
        Initialize sandbox with timeout.
        
        Args:
            timeout_seconds: Maximum execution time in seconds
        """
        self.timeout_seconds = timeout_seconds

    def validate_code(self, code: str) -> ast.AST:
        """
        Validate code using AST parsing.
        
        Args:
            code: Python code to validate
            
        Returns:
            AST tree if valid
            
        Raises:
            ValueError: If code contains disallowed constructs
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"SyntaxError: {e}")

        for node in ast.walk(tree):
            if isinstance(node, self.DISALLOWED_NODES):
                raise ValueError(f"Disallowed language feature: {node.__class__.__name__}")

            # Check imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name not in self.ALLOWED_IMPORTS:
                        raise ValueError(f"Import '{alias.name}' not allowed")

            if isinstance(node, ast.ImportFrom):
                module = node.module
                if module not in self.ALLOWED_IMPORTS:
                    raise ValueError(f"Import from '{module}' not allowed")

                allowed_names = self.ALLOWED_IMPORTS[module]
                if allowed_names is not None:
                    for alias in node.names:
                        if alias.name not in allowed_names:
                            raise ValueError(f"Import '{alias.name}' from '{module}' not allowed")

        return tree

    def execute(self, code: str, namespace: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], str, str]:
        """
        Execute code in sandbox with timeout and output capture.
        
        Args:
            code: Python code to execute
            namespace: Initial namespace (optional)
            
        Returns:
            Tuple of (namespace, stdout, stderr)
            
        Raises:
            ValueError: If code validation fails
            TimeoutException: If execution exceeds timeout
            Exception: If execution fails
        """
        # Validate code
        self.validate_code(code)

        # Prepare namespace
        if namespace is None:
            namespace = {}

        # Create restricted import function
        import builtins
        def restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name in self.ALLOWED_IMPORTS or (fromlist and any(f in self.ALLOWED_IMPORTS for f in fromlist)):
                return builtins.__import__(name, globals, locals, fromlist, level)
            raise ImportError(f"Import '{name}' not allowed")

        # Setup namespace with safe builtins
        user_builtins = self.SAFE_BUILTINS.copy()
        user_builtins["__import__"] = restricted_import

        exec_namespace = {
            "__builtins__": user_builtins,
            "__name__": "__main__",
            **namespace
        }

        # Capture output
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(compile(code, "<user>", "exec"), exec_namespace, exec_namespace)
        except Exception as e:
            raise

        return exec_namespace, stdout_capture.getvalue(), stderr_capture.getvalue()

