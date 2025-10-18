"""
Unit tests for Test Runner Service
Tests safe code execution, test parsing, and result formatting.
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import services directly from app/services
from app.services.sandbox import Sandbox
from app.services.test_runner import TestRunner
from app.services.assertion_parser import AssertionParser
from app.services.test_executor import TestExecutor
from app.services.test_formatter import TestFormatter


class TestSandbox:
    """Tests for Sandbox service."""

    def test_sandbox_initialization(self):
        """Test sandbox initializes with timeout."""
        sandbox = Sandbox(timeout_seconds=5)
        assert sandbox.timeout_seconds == 5

    def test_validate_simple_code(self):
        """Test validation of simple Python code."""
        sandbox = Sandbox()
        code = "x = 5\ny = 10\nz = x + y"
        tree = sandbox.validate_code(code)
        assert tree is not None

    def test_validate_syntax_error(self):
        """Test validation catches syntax errors."""
        sandbox = Sandbox()
        code = "x = 5\ny = "
        with pytest.raises(ValueError, match="SyntaxError"):
            sandbox.validate_code(code)

    def test_validate_disallowed_global(self):
        """Test validation catches disallowed global statement."""
        sandbox = Sandbox()
        code = "global x\nx = 5"
        with pytest.raises(ValueError, match="Disallowed"):
            sandbox.validate_code(code)

    def test_validate_disallowed_import(self):
        """Test validation catches disallowed imports."""
        sandbox = Sandbox()
        code = "import os"
        with pytest.raises(ValueError, match="not allowed"):
            sandbox.validate_code(code)

    def test_execute_simple_code(self):
        """Test execution of simple code."""
        sandbox = Sandbox()
        code = "x = 5\ny = 10\nz = x + y"
        namespace, stdout, stderr = sandbox.execute(code)
        assert namespace['x'] == 5
        assert namespace['y'] == 10
        assert namespace['z'] == 15

    def test_execute_with_function(self):
        """Test execution of code with function definition."""
        sandbox = Sandbox()
        code = """
def add(a, b):
    return a + b

result = add(2, 3)
"""
        namespace, stdout, stderr = sandbox.execute(code)
        assert namespace['result'] == 5

    def test_execute_with_print(self):
        """Test execution captures print output."""
        sandbox = Sandbox()
        code = "print('Hello, World!')"
        namespace, stdout, stderr = sandbox.execute(code)
        assert "Hello, World!" in stdout

    def test_execute_with_error(self):
        """Test execution handles runtime errors."""
        sandbox = Sandbox()
        code = "x = 1 / 0"
        with pytest.raises(ZeroDivisionError):
            sandbox.execute(code)

    def test_execute_with_allowed_import(self):
        """Test execution with allowed imports."""
        sandbox = Sandbox()
        code = "from functools import wraps"
        namespace, stdout, stderr = sandbox.execute(code)
        assert 'wraps' in namespace

    def test_execute_with_disallowed_import_from(self):
        """Test execution catches disallowed import from."""
        sandbox = Sandbox()
        code = "from os import path"
        with pytest.raises(ValueError, match="not allowed"):
            sandbox.execute(code)


class TestAssertionParser:
    """Tests for Assertion Parser service."""

    def test_parse_assertEqual(self):
        """Test parsing assertEqual assertion."""
        parser = AssertionParser()
        result = parser.parse_assertion("assertEqual(add(2, 3), 5)")
        assert result['type'] == 'assertEqual'
        assert result['actual'] == 'add(2, 3)'
        assert result['expected'] == '5'

    def test_parse_assertTrue(self):
        """Test parsing assertTrue assertion."""
        parser = AssertionParser()
        result = parser.parse_assertion("assertTrue(x > 0)")
        assert result['type'] == 'assertTrue'
        assert result['actual'] == 'x > 0'
        assert result['expected'] == 'True'

    def test_parse_assertFalse(self):
        """Test parsing assertFalse assertion."""
        parser = AssertionParser()
        result = parser.parse_assertion("assertFalse(x < 0)")
        assert result['type'] == 'assertFalse'
        assert result['actual'] == 'x < 0'
        assert result['expected'] == 'False'

    def test_parse_assertIn(self):
        """Test parsing assertIn assertion."""
        parser = AssertionParser()
        result = parser.parse_assertion("assertIn(1, [1, 2, 3])")
        assert result['type'] == 'assertIn'

    def test_parse_assertRaises(self):
        """Test parsing assertRaises assertion."""
        parser = AssertionParser()
        result = parser.parse_assertion("assertRaises(ValueError, func)")
        assert result['type'] == 'assertRaises'

    def test_parse_unknown_assertion(self):
        """Test parsing unknown assertion type."""
        parser = AssertionParser()
        result = parser.parse_assertion("someUnknownAssertion(x)")
        assert result['type'] == 'unknown'

    def test_format_error_message_assertEqual(self):
        """Test formatting error message for assertEqual."""
        parser = AssertionParser()
        assertion = {
            'type': 'assertEqual',
            'expected': '5',
            'actual': '4'
        }
        msg = parser.format_error_message(assertion)
        assert "Expected 5" in msg
        assert "got 4" in msg

    def test_extract_test_results(self):
        """Test extracting expected results from test code."""
        parser = AssertionParser()
        test_code = """
if 'fizzbuzz' not in ns:
    raise ValueError("fizzbuzz not defined")
expected = ['1', '2', 'Fizz', '4', 'Buzz']
result = ns['fizzbuzz'](5)
if result != expected:
    raise AssertionError(f"Expected {expected}, got {result}")
"""
        results = parser.extract_test_results(test_code)
        assert 'fizzbuzz' in results


class TestTestRunner:
    """Tests for Test Runner service."""

    def test_test_runner_initialization(self):
        """Test test runner initializes."""
        runner = TestRunner(timeout_seconds=5)
        assert runner.sandbox is not None
        assert runner.assertion_parser is not None

    def test_run_tests_with_passing_code(self):
        """Test running tests with passing code."""
        runner = TestRunner()
        user_code = """
def add(a, b):
    return a + b
"""
        test_code = """
def grade(ns):
    if 'add' not in ns:
        return {'score': 0, 'max_score': 100, 'feedback': 'add not defined'}
    
    result = ns['add'](2, 3)
    if result != 5:
        return {'score': 0, 'max_score': 100, 'feedback': 'add(2, 3) should return 5'}
    
    return {'score': 100, 'max_score': 100, 'feedback': 'Great!'}
"""
        result = runner.run_tests(user_code, test_code)
        assert result['success'] is True
        assert result['score'] == 100

    def test_run_tests_with_failing_code(self):
        """Test running tests with failing code."""
        runner = TestRunner()
        user_code = """
def add(a, b):
    return a + b + 1
"""
        test_code = """
def grade(ns):
    result = ns['add'](2, 3)
    if result != 5:
        return {'score': 0, 'max_score': 100, 'feedback': 'add(2, 3) should return 5'}
    return {'score': 100, 'max_score': 100, 'feedback': 'Great!'}
"""
        result = runner.run_tests(user_code, test_code)
        assert result['success'] is True
        assert result['score'] == 0

    def test_run_tests_with_syntax_error(self):
        """Test running tests with syntax error in user code."""
        runner = TestRunner()
        user_code = "def add(a, b)\n    return a + b"
        test_code = "def grade(ns): return {'score': 0, 'max_score': 100, 'feedback': ''}"
        result = runner.run_tests(user_code, test_code)
        assert result['success'] is False
        assert result['error'] is not None

    def test_run_test_suite(self):
        """Test running a suite of tests."""
        runner = TestRunner()
        user_code = """
def add(a, b):
    return a + b
"""
        tests = [
            {
                'id': 1,
                'name': 'test_add_positive',
                'assertion': 'assert add(2, 3) == 5',
                'expected': 5,
                'mock_set': 'valid'
            }
        ]
        result = runner.run_test_suite(user_code, tests)
        assert result['total_tests'] == 1


class TestTestFormatter:
    """Tests for Test Formatter service."""

    def test_formatter_initialization(self):
        """Test formatter initializes."""
        formatter = TestFormatter()
        assert formatter.assertion_parser is not None

    def test_format_test_result_pass(self):
        """Test formatting a passing test result."""
        formatter = TestFormatter()
        test_result = {
            'id': 1,
            'name': 'test_add',
            'status': 'pass',
            'assertion': 'assertEqual(add(2, 3), 5)',
            'expected': 5,
            'actual': 5,
            'error': None,
            'execution_time': 0.001,
            'mock_set': 'valid'
        }
        formatted = formatter.format_test_result(test_result)
        assert formatted['status'] == 'pass'
        assert '✓' in formatted['message']

    def test_format_test_result_fail(self):
        """Test formatting a failing test result."""
        formatter = TestFormatter()
        test_result = {
            'id': 1,
            'name': 'test_add',
            'status': 'fail',
            'assertion': 'assertEqual(add(2, 3), 5)',
            'expected': 5,
            'actual': 4,
            'error': 'Expected 5, got 4',
            'execution_time': 0.001,
            'mock_set': 'valid'
        }
        formatted = formatter.format_test_result(test_result)
        assert formatted['status'] == 'fail'
        assert '✗' in formatted['message']

    def test_format_api_response(self):
        """Test formatting API response."""
        formatter = TestFormatter()
        execution_result = {
            'success': True,
            'total_tests': 2,
            'passed_tests': 2,
            'failed_tests': 0,
            'execution_time': 0.002,
            'mock_set': 'valid',
            'results': []
        }
        response = formatter.format_api_response(execution_result)
        assert response['ok'] is True
        assert response['total_tests'] == 2

