"""
Assertion Parser Service
Parses assertion statements and extracts expected/actual values for detailed feedback.
"""

import re
from typing import Dict, Any, Optional, List, Tuple


class AssertionParser:
    """
    Parses assertion statements and extracts meaningful information
    for generating helpful error messages.
    """

    @staticmethod
    def parse_assertion(assertion_str: str) -> Dict[str, Any]:
        """
        Parse an assertion statement and extract components.

        Args:
            assertion_str: Assertion statement (e.g., "assertEqual(add(2, 3), 5)")

        Returns:
            Dict with assertion type, expected, actual, and message
        """
        result = {
            'type': 'unknown',
            'expected': None,
            'actual': None,
            'message': assertion_str,
            'raw': assertion_str
        }

        # Parse assertEqual - handle nested parentheses
        match = re.match(r'assertEqual\((.*),\s*([^,)]+)\)\s*$', assertion_str)
        if match:
            result['type'] = 'assertEqual'
            result['actual'] = match.group(1).strip()
            result['expected'] = match.group(2).strip()
            return result

        # Parse assertTrue
        match = re.match(r'assertTrue\((.*?)\)', assertion_str)
        if match:
            result['type'] = 'assertTrue'
            result['actual'] = match.group(1).strip()
            result['expected'] = 'True'
            return result

        # Parse assertFalse
        match = re.match(r'assertFalse\((.*?)\)', assertion_str)
        if match:
            result['type'] = 'assertFalse'
            result['actual'] = match.group(1).strip()
            result['expected'] = 'False'
            return result

        # Parse assertIn
        match = re.match(r'assertIn\((.*?),\s*(.*?)\)', assertion_str)
        if match:
            result['type'] = 'assertIn'
            result['actual'] = match.group(2).strip()
            result['expected'] = f"contains {match.group(1).strip()}"
            return result

        # Parse assertRaises
        match = re.match(r'assertRaises\((.*?),\s*(.*?)\)', assertion_str)
        if match:
            result['type'] = 'assertRaises'
            result['expected'] = f"raises {match.group(1).strip()}"
            result['actual'] = match.group(2).strip()
            return result

        return result

    @staticmethod
    def format_error_message(assertion: Dict[str, Any], error: Optional[str] = None) -> str:
        """
        Format a helpful error message from assertion data.
        
        Args:
            assertion: Parsed assertion dict
            error: Optional error message
            
        Returns:
            Formatted error message
        """
        assertion_type = assertion.get('type', 'unknown')
        expected = assertion.get('expected')
        actual = assertion.get('actual')

        if assertion_type == 'assertEqual':
            msg = f"Expected {expected}, but got {actual}"
        elif assertion_type == 'assertTrue':
            msg = f"Expected {actual} to be True"
        elif assertion_type == 'assertFalse':
            msg = f"Expected {actual} to be False"
        elif assertion_type == 'assertIn':
            msg = f"Expected {expected} in {actual}"
        elif assertion_type == 'assertRaises':
            msg = f"Expected {expected} when calling {actual}"
        else:
            msg = assertion.get('message', 'Assertion failed')

        if error:
            msg += f"\nError: {error}"

        return msg

    @staticmethod
    def extract_test_results(test_code: str) -> Dict[str, List[Any]]:
        """
        Extract expected test results from test code.
        
        Args:
            test_code: Test harness code
            
        Returns:
            Dict mapping function names to expected results
        """
        expected = {}

        # Extract function name
        func_pattern = r"if\s+'(\w+)'\s+not\s+in\s+ns"
        func_matches = re.findall(func_pattern, test_code)
        func_name = func_matches[0] if func_matches else 'unknown'

        # Find variable assignments like: expected=['1','2','Fizz',...]
        var_pattern = r'expected\s*=\s*(\[.*?\])'
        var_matches = re.findall(var_pattern, test_code)

        for match in var_matches:
            try:
                expected_value = eval(match)
                if isinstance(expected_value, list):
                    if func_name not in expected:
                        expected[func_name] = []
                    expected[func_name].append(expected_value)
            except:
                pass

        # Look for direct patterns like: if result != [4, 16]:
        pattern = r'if\s+result\d*\s*!=\s*(\[.*?\])'
        matches = re.findall(pattern, test_code)

        for match in matches:
            try:
                expected_value = eval(match)
                if isinstance(expected_value, list):
                    if func_name not in expected:
                        expected[func_name] = []
                    expected[func_name].append(expected_value)
            except:
                pass

        return expected

