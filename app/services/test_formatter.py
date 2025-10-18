"""
Test Formatter Service
Formats test results for frontend display with assertion details and error traces.
"""

from typing import Dict, Any, List, Optional
from .assertion_parser import AssertionParser


class TestFormatter:
    """
    Formats test execution results for frontend consumption.
    Includes assertion details, error traces, execution time, and coverage info.
    """

    def __init__(self):
        """Initialize test formatter."""
        self.assertion_parser = AssertionParser()

    def format_test_result(self, test_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a single test result for frontend.
        
        Args:
            test_result: Raw test result dict
            
        Returns:
            Formatted test result
        """
        formatted = {
            'id': test_result.get('id', 0),
            'name': test_result.get('name', 'unknown'),
            'status': test_result.get('status', 'unknown'),
            'assertion': test_result.get('assertion', ''),
            'expected': test_result.get('expected'),
            'actual': test_result.get('actual'),
            'error': test_result.get('error'),
            'execution_time': test_result.get('execution_time', 0),
            'mock_set': test_result.get('mock_set', 'valid'),
            'message': self._generate_message(test_result)
        }

        return formatted

    def format_test_suite_results(self, suite_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format test suite results for frontend.
        
        Args:
            suite_result: Raw test suite result dict
            
        Returns:
            Formatted test suite result
        """
        formatted = {
            'success': suite_result.get('success', False),
            'total_tests': suite_result.get('total_tests', 0),
            'passed_tests': suite_result.get('passed_tests', 0),
            'failed_tests': suite_result.get('failed_tests', 0),
            'execution_time': suite_result.get('execution_time', 0),
            'mock_set': suite_result.get('mock_set', 'valid'),
            'results': [
                self.format_test_result(test)
                for test in suite_result.get('results', [])
            ],
            'summary': self._generate_summary(suite_result),
            'error': suite_result.get('error')
        }

        return formatted

    def format_api_response(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format test execution result for API response.
        
        Args:
            execution_result: Raw execution result
            
        Returns:
            API response dict
        """
        response = {
            'ok': execution_result.get('success', False),
            'total_tests': execution_result.get('total_tests', 0),
            'passed_tests': execution_result.get('passed_tests', 0),
            'failed_tests': execution_result.get('failed_tests', 0),
            'execution_time': execution_result.get('execution_time', 0),
            'mock_set': execution_result.get('mock_set', 'valid'),
            'results': [
                self.format_test_result(test)
                for test in execution_result.get('results', [])
            ]
        }

        if execution_result.get('error'):
            response['error'] = execution_result['error']

        return response

    def _generate_message(self, test_result: Dict[str, Any]) -> str:
        """
        Generate a human-readable message for a test result.
        
        Args:
            test_result: Test result dict
            
        Returns:
            Message string
        """
        status = test_result.get('status', 'unknown')
        name = test_result.get('name', 'unknown')

        if status == 'pass':
            return f"✓ {name} passed"
        elif status == 'fail':
            error = test_result.get('error', 'Assertion failed')
            return f"✗ {name} failed: {error}"
        elif status == 'error':
            error = test_result.get('error', 'Unknown error')
            return f"⚠ {name} error: {error}"
        else:
            return f"? {name} status unknown"

    def _generate_summary(self, suite_result: Dict[str, Any]) -> str:
        """
        Generate a summary message for test suite results.
        
        Args:
            suite_result: Test suite result dict
            
        Returns:
            Summary string
        """
        total = suite_result.get('total_tests', 0)
        passed = suite_result.get('passed_tests', 0)
        failed = suite_result.get('failed_tests', 0)

        if total == 0:
            return "No tests to run"

        if failed == 0:
            return f"All {total} tests passed! ✓"
        else:
            return f"{passed}/{total} tests passed, {failed} failed"

    def format_error_response(self, error: str, trace: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Format an error response for API.
        
        Args:
            error: Error message
            trace: Optional error trace lines
            
        Returns:
            Error response dict
        """
        response = {
            'ok': False,
            'error': error
        }

        if trace:
            response['trace'] = trace

        return response

    def format_coverage_info(self, coverage_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format coverage information for frontend.
        
        Args:
            coverage_data: Raw coverage data
            
        Returns:
            Formatted coverage info
        """
        return {
            'lines': coverage_data.get('lines', 0),
            'branches': coverage_data.get('branches', 0),
            'functions': coverage_data.get('functions', 0),
            'statements': coverage_data.get('statements', 0)
        }

