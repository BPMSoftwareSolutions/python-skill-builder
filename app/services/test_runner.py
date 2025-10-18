"""
Test Runner Service
Executes tests and captures detailed results with error handling.
"""

import time
import traceback
from typing import Dict, Any, List, Optional
from .sandbox import Sandbox
from .assertion_parser import AssertionParser


class TestRunner:
    """
    Executes user code and tests in a safe sandbox environment.
    Captures detailed test results including pass/fail status and error information.
    """

    def __init__(self, timeout_seconds: int = 5):
        """
        Initialize test runner.
        
        Args:
            timeout_seconds: Maximum execution time per test
        """
        self.sandbox = Sandbox(timeout_seconds)
        self.assertion_parser = AssertionParser()

    def run_tests(self, user_code: str, test_code: str) -> Dict[str, Any]:
        """
        Execute user code and tests.
        
        Args:
            user_code: User's submitted code
            test_code: Test harness code that defines grade(user_ns) function
            
        Returns:
            Dict with test results including score, feedback, and execution details
        """
        start_time = time.time()
        result = {
            'success': False,
            'score': 0,
            'max_score': 100,
            'feedback': '',
            'tests': [],
            'execution_time': 0,
            'error': None,
            'trace': []
        }

        try:
            # Validate and execute user code
            user_ns, user_stdout, user_stderr = self.sandbox.execute(user_code)

            # Prepare test namespace
            import inspect
            import builtins
            test_builtins = self.sandbox.SAFE_BUILTINS.copy()
            test_builtins["__import__"] = builtins.__import__
            test_builtins["__name__"] = "__main__"
            test_builtins["__file__"] = "<tests>"

            test_ns = {
                "__builtins__": test_builtins,
                "inspect": inspect
            }

            # Execute test code
            exec(compile(test_code, "<tests>", "exec"), test_ns, test_ns)

            # Call grade function
            if "grade" not in test_ns or not callable(test_ns["grade"]):
                raise RuntimeError("Test script must define grade(user_ns) function")

            grade_result = test_ns["grade"](user_ns)

            # Extract results
            result['success'] = True
            result['score'] = int(grade_result.get('score', 0))
            result['max_score'] = int(grade_result.get('max_score', 100))
            result['feedback'] = str(grade_result.get('feedback', ''))

            # Extract test details if available
            if 'tests' in grade_result:
                result['tests'] = grade_result['tests']

            # Extract execution results if available
            if 'execution_results' in grade_result:
                result['execution_results'] = grade_result['execution_results']

        except SyntaxError as e:
            result['error'] = f"SyntaxError: {str(e)}"
            result['trace'] = traceback.format_exc().splitlines()
        except ValueError as e:
            result['error'] = f"Validation Error: {str(e)}"
            result['trace'] = traceback.format_exc().splitlines()
        except Exception as e:
            result['error'] = str(e)
            result['trace'] = traceback.format_exc().splitlines()

        result['execution_time'] = time.time() - start_time
        return result

    def run_test_suite(self, user_code: str, tests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute a suite of individual tests.
        
        Args:
            user_code: User's submitted code
            tests: List of test dicts with 'name', 'assertion', 'expected', 'mock_set'
            
        Returns:
            Dict with aggregated test results
        """
        start_time = time.time()
        results = {
            'success': True,
            'total_tests': len(tests),
            'passed_tests': 0,
            'failed_tests': 0,
            'execution_time': 0,
            'results': []
        }

        try:
            # Execute user code once
            user_ns, _, _ = self.sandbox.execute(user_code)

            # Run each test
            for test in tests:
                test_result = {
                    'id': test.get('id', 0),
                    'name': test.get('name', 'unknown'),
                    'status': 'pass',
                    'assertion': test.get('assertion', ''),
                    'expected': test.get('expected'),
                    'actual': None,
                    'error': None,
                    'execution_time': 0,
                    'mock_set': test.get('mock_set', 'valid')
                }

                test_start = time.time()

                try:
                    # Execute test assertion
                    assertion_code = test.get('assertion', '')
                    test_ns = {'__builtins__': self.sandbox.SAFE_BUILTINS}
                    test_ns.update(user_ns)

                    exec(compile(assertion_code, "<test>", "exec"), test_ns, test_ns)
                    test_result['status'] = 'pass'
                    results['passed_tests'] += 1

                except AssertionError as e:
                    test_result['status'] = 'fail'
                    test_result['error'] = str(e)
                    results['failed_tests'] += 1
                except Exception as e:
                    test_result['status'] = 'error'
                    test_result['error'] = str(e)
                    results['failed_tests'] += 1

                test_result['execution_time'] = time.time() - test_start
                results['results'].append(test_result)

        except Exception as e:
            results['success'] = False
            results['error'] = str(e)

        results['execution_time'] = time.time() - start_time
        return results

