"""
Test Executor Service
Loads test suites from workshop data and executes them with mock data.
"""

import time
from typing import Dict, Any, List, Optional
from .test_runner import TestRunner


class TestExecutor:
    """
    Executes test suites from workshop data with mock data sets.
    Aggregates results and generates test reports.
    """

    def __init__(self, timeout_seconds: int = 5):
        """
        Initialize test executor.
        
        Args:
            timeout_seconds: Maximum execution time per test
        """
        self.test_runner = TestRunner(timeout_seconds)

    def execute_workshop_tests(
        self,
        user_code: str,
        workshop: Dict[str, Any],
        mock_set_id: str = 'valid'
    ) -> Dict[str, Any]:
        """
        Execute all tests for a workshop with specified mock data set.
        
        Args:
            user_code: User's submitted code
            workshop: Workshop dict with 'tests' and 'mockData' fields
            mock_set_id: ID of mock data set to use ('valid', 'edge', 'stress')
            
        Returns:
            Dict with test execution results
        """
        start_time = time.time()
        result = {
            'success': False,
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'execution_time': 0,
            'mock_set': mock_set_id,
            'results': [],
            'error': None
        }

        try:
            # Get tests from workshop
            tests = workshop.get('tests', [])
            if not tests:
                result['error'] = 'No tests found in workshop'
                return result

            result['total_tests'] = len(tests)

            # Get mock data set
            mock_data = self._get_mock_data(workshop, mock_set_id)

            # Execute tests with mock data
            for test in tests:
                test_result = self._execute_single_test(
                    user_code,
                    test,
                    mock_data
                )
                result['results'].append(test_result)

                if test_result['status'] == 'pass':
                    result['passed_tests'] += 1
                else:
                    result['failed_tests'] += 1

            result['success'] = True

        except Exception as e:
            result['error'] = str(e)

        result['execution_time'] = time.time() - start_time
        return result

    def _get_mock_data(self, workshop: Dict[str, Any], mock_set_id: str) -> Dict[str, Any]:
        """
        Get mock data set from workshop.
        
        Args:
            workshop: Workshop dict
            mock_set_id: Mock set ID
            
        Returns:
            Mock data dict
        """
        mock_data_sets = workshop.get('mockData', {})
        return mock_data_sets.get(mock_set_id, {})

    def _execute_single_test(
        self,
        user_code: str,
        test: Dict[str, Any],
        mock_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a single test with mock data.
        
        Args:
            user_code: User's code
            test: Test dict with 'name', 'assertion', 'expected'
            mock_data: Mock data for this test
            
        Returns:
            Test result dict
        """
        start_time = time.time()
        result = {
            'id': test.get('id', 0),
            'name': test.get('name', 'unknown'),
            'status': 'pass',
            'assertion': test.get('assertion', ''),
            'expected': test.get('expected'),
            'actual': None,
            'error': None,
            'execution_time': 0,
            'mock_data': mock_data
        }

        try:
            # Run test using test runner
            test_result = self.test_runner.run_tests(user_code, test.get('assertion', ''))

            if test_result['error']:
                result['status'] = 'fail'
                result['error'] = test_result['error']
            else:
                result['status'] = 'pass'

        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)

        result['execution_time'] = time.time() - start_time
        return result

    def generate_test_report(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a test report from execution results.
        
        Args:
            execution_result: Result from execute_workshop_tests
            
        Returns:
            Formatted test report
        """
        total = execution_result.get('total_tests', 0)
        passed = execution_result.get('passed_tests', 0)
        failed = execution_result.get('failed_tests', 0)

        pass_rate = (passed / total * 100) if total > 0 else 0

        report = {
            'summary': {
                'total_tests': total,
                'passed_tests': passed,
                'failed_tests': failed,
                'pass_rate': round(pass_rate, 2),
                'execution_time': execution_result.get('execution_time', 0),
                'mock_set': execution_result.get('mock_set', 'valid')
            },
            'details': execution_result.get('results', []),
            'status': 'pass' if failed == 0 else 'fail'
        }

        return report

