"""
Code Metrics Calculator
Calculates code quality metrics for analysis and refactoring validation.
"""

import ast
import re
from typing import Dict, Any


class CodeMetrics:
    """
    Calculates various code quality metrics.
    """

    @staticmethod
    def calculate_complexity(code: str) -> int:
        """
        Calculate cyclomatic complexity of code.
        Counts decision points (if, for, while, except, etc.)
        
        Args:
            code: Python code string
            
        Returns:
            Complexity score (1 = simple, higher = more complex)
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return 0

        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1

        return complexity

    @staticmethod
    def calculate_coverage(code: str, test_code: str) -> float:
        """
        Estimate code coverage based on function definitions and test assertions.
        
        Args:
            code: User code
            test_code: Test code
            
        Returns:
            Coverage percentage (0-100)
        """
        try:
            code_tree = ast.parse(code)
            test_tree = ast.parse(test_code)
        except SyntaxError:
            return 0.0

        # Count functions in code
        functions = [
            node.name for node in ast.walk(code_tree)
            if isinstance(node, ast.FunctionDef)
        ]
        
        if not functions:
            return 100.0  # No functions = full coverage

        # Count test assertions
        assertions = [
            node for node in ast.walk(test_tree)
            if isinstance(node, ast.Assert)
        ]
        
        # Simple heuristic: coverage = assertions / functions * 100
        coverage = min(100.0, (len(assertions) / len(functions)) * 100)
        return coverage

    @staticmethod
    def calculate_duplication(code: str) -> float:
        """
        Estimate code duplication by looking for repeated patterns.
        
        Args:
            code: Python code string
            
        Returns:
            Duplication percentage (0-100)
        """
        lines = code.strip().split('\n')
        if len(lines) < 2:
            return 0.0

        # Count duplicate lines
        line_counts = {}
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                line_counts[stripped] = line_counts.get(stripped, 0) + 1

        duplicates = sum(count - 1 for count in line_counts.values() if count > 1)
        duplication = (duplicates / len(lines)) * 100 if lines else 0.0
        
        return min(100.0, duplication)

    @staticmethod
    def has_type_hints(code: str) -> bool:
        """
        Check if code contains type hints.
        
        Args:
            code: Python code string
            
        Returns:
            True if type hints are present
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return False

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check function annotations
                if node.returns is not None:
                    return True
                for arg in node.args.args:
                    if arg.annotation is not None:
                        return True
            elif isinstance(node, ast.AnnAssign):
                # Check variable annotations
                return True

        return False

    @staticmethod
    def has_docstring(code: str) -> bool:
        """
        Check if code contains docstrings.
        
        Args:
            code: Python code string
            
        Returns:
            True if docstrings are present
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return False

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                docstring = ast.get_docstring(node)
                if docstring:
                    return True

        return False

    @staticmethod
    def get_metrics_summary(code: str) -> Dict[str, Any]:
        """
        Get a summary of all code metrics.
        
        Args:
            code: Python code string
            
        Returns:
            Dictionary with all metrics
        """
        return {
            "complexity": CodeMetrics.calculate_complexity(code),
            "coverage": CodeMetrics.calculate_coverage(code, ""),
            "duplication": CodeMetrics.calculate_duplication(code),
            "has_type_hints": CodeMetrics.has_type_hints(code),
            "has_docstring": CodeMetrics.has_docstring(code),
            "lines_of_code": len(code.strip().split('\n'))
        }

