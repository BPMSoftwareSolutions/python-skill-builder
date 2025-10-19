"""
Unit tests for CodeMetrics class.
"""

import pytest
from app.services.code_metrics import CodeMetrics


class TestComplexityCalculation:
    """Test cyclomatic complexity calculation."""

    def test_simple_code_complexity(self):
        """Test complexity of simple code."""
        code = """
def add(a, b):
    return a + b
"""
        complexity = CodeMetrics.calculate_complexity(code)
        
        assert complexity == 1

    def test_if_statement_increases_complexity(self):
        """Test that if statements increase complexity."""
        code = """
def check(x):
    if x > 0:
        return True
    return False
"""
        complexity = CodeMetrics.calculate_complexity(code)
        
        assert complexity > 1

    def test_multiple_conditions_increase_complexity(self):
        """Test that multiple conditions increase complexity."""
        code = """
def check(x, y):
    if x > 0:
        if y > 0:
            return True
    return False
"""
        complexity = CodeMetrics.calculate_complexity(code)
        
        assert complexity > 2

    def test_loop_increases_complexity(self):
        """Test that loops increase complexity."""
        code = """
def sum_list(items):
    total = 0
    for item in items:
        total += item
    return total
"""
        complexity = CodeMetrics.calculate_complexity(code)
        
        assert complexity > 1

    def test_syntax_error_returns_zero(self):
        """Test that syntax errors return 0."""
        code = "def broken(\n    return"
        
        complexity = CodeMetrics.calculate_complexity(code)
        
        assert complexity == 0


class TestCoverageCalculation:
    """Test code coverage estimation."""

    def test_no_functions_full_coverage(self):
        """Test that code with no functions has full coverage."""
        code = "x = 1 + 1"
        
        coverage = CodeMetrics.calculate_coverage(code, "")
        
        assert coverage == 100.0

    def test_coverage_with_assertions(self):
        """Test coverage calculation with assertions."""
        code = """
def add(a, b):
    return a + b
"""
        test_code = """
assert add(1, 1) == 2
"""
        coverage = CodeMetrics.calculate_coverage(code, test_code)
        
        assert coverage > 0

    def test_coverage_capped_at_100(self):
        """Test that coverage is capped at 100%."""
        code = "def f(): pass"
        test_code = """
assert True
assert True
assert True
"""
        coverage = CodeMetrics.calculate_coverage(code, test_code)
        
        assert coverage <= 100.0


class TestDuplicationCalculation:
    """Test code duplication detection."""

    def test_no_duplication(self):
        """Test code with no duplication."""
        code = """
x = 1
y = 2
z = 3
"""
        duplication = CodeMetrics.calculate_duplication(code)
        
        assert duplication == 0.0

    def test_duplicate_lines_detected(self):
        """Test that duplicate lines are detected."""
        code = """
x = 1
x = 1
y = 2
"""
        duplication = CodeMetrics.calculate_duplication(code)
        
        assert duplication > 0.0

    def test_duplication_capped_at_100(self):
        """Test that duplication is capped at 100%."""
        code = """
x = 1
x = 1
x = 1
"""
        duplication = CodeMetrics.calculate_duplication(code)
        
        assert duplication <= 100.0


class TestTypeHintsDetection:
    """Test type hints detection."""

    def test_code_without_type_hints(self):
        """Test code without type hints."""
        code = """
def add(a, b):
    return a + b
"""
        has_hints = CodeMetrics.has_type_hints(code)
        
        assert has_hints is False

    def test_code_with_function_return_type_hint(self):
        """Test code with function return type hint."""
        code = """
def add(a, b) -> int:
    return a + b
"""
        has_hints = CodeMetrics.has_type_hints(code)
        
        assert has_hints is True

    def test_code_with_parameter_type_hints(self):
        """Test code with parameter type hints."""
        code = """
def add(a: int, b: int):
    return a + b
"""
        has_hints = CodeMetrics.has_type_hints(code)
        
        assert has_hints is True

    def test_code_with_variable_annotation(self):
        """Test code with variable annotation."""
        code = """
x: int = 5
"""
        has_hints = CodeMetrics.has_type_hints(code)
        
        assert has_hints is True

    def test_syntax_error_returns_false(self):
        """Test that syntax errors return False."""
        code = "def broken(\n    return"
        
        has_hints = CodeMetrics.has_type_hints(code)
        
        assert has_hints is False


class TestDocstringDetection:
    """Test docstring detection."""

    def test_code_without_docstring(self):
        """Test code without docstring."""
        code = """
def add(a, b):
    return a + b
"""
        has_docstring = CodeMetrics.has_docstring(code)
        
        assert has_docstring is False

    def test_code_with_function_docstring(self):
        """Test code with function docstring."""
        code = '''
def add(a, b):
    """Add two numbers."""
    return a + b
'''
        has_docstring = CodeMetrics.has_docstring(code)
        
        assert has_docstring is True

    def test_code_with_class_docstring(self):
        """Test code with class docstring."""
        code = '''
class Calculator:
    """A simple calculator."""
    pass
'''
        has_docstring = CodeMetrics.has_docstring(code)
        
        assert has_docstring is True

    def test_code_with_module_docstring(self):
        """Test code with module docstring."""
        code = '''
"""This is a module."""
x = 1
'''
        has_docstring = CodeMetrics.has_docstring(code)
        
        assert has_docstring is True

    def test_syntax_error_returns_false(self):
        """Test that syntax errors return False."""
        code = "def broken(\n    return"
        
        has_docstring = CodeMetrics.has_docstring(code)
        
        assert has_docstring is False


class TestMetricsSummary:
    """Test metrics summary generation."""

    def test_metrics_summary_includes_all_metrics(self):
        """Test that summary includes all metrics."""
        code = """
def add(a: int, b: int) -> int:
    '''Add two numbers.'''
    return a + b
"""
        summary = CodeMetrics.get_metrics_summary(code)
        
        assert "complexity" in summary
        assert "coverage" in summary
        assert "duplication" in summary
        assert "has_type_hints" in summary
        assert "has_docstring" in summary
        assert "lines_of_code" in summary

    def test_metrics_summary_values_are_correct_type(self):
        """Test that summary values have correct types."""
        code = "x = 1"
        summary = CodeMetrics.get_metrics_summary(code)
        
        assert isinstance(summary["complexity"], int)
        assert isinstance(summary["coverage"], float)
        assert isinstance(summary["duplication"], float)
        assert isinstance(summary["has_type_hints"], bool)
        assert isinstance(summary["has_docstring"], bool)
        assert isinstance(summary["lines_of_code"], int)

    def test_metrics_summary_well_written_code(self):
        """Test metrics for well-written code."""
        code = """
def add(a: int, b: int) -> int:
    '''Add two numbers together.'''
    return a + b
"""
        summary = CodeMetrics.get_metrics_summary(code)
        
        assert summary["has_type_hints"] is True
        assert summary["has_docstring"] is True
        assert summary["complexity"] == 1

