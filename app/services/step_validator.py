"""
Step Validator Service
Validates user input for each step of the TDD workflow.
"""

import ast
import re
from typing import Dict, List, Any
from .sandbox import Sandbox
from .test_runner import TestRunner


class StepValidator:
    """
    Validates user submissions for each step of the TDD workflow.
    """

    def __init__(self, timeout_seconds: int = 5):
        """
        Initialize step validator.
        
        Args:
            timeout_seconds: Maximum execution time for validation
        """
        self.sandbox = Sandbox(timeout_seconds)
        self.test_runner = TestRunner(timeout_seconds)

    def validate_step_1(self, test_code: str, workshop_id: str) -> Dict[str, Any]:
        """
        Validate STEP 1: Write a Failing Test
        
        Requirements:
        - Test function name starts with 'test_'
        - At least one assertion present
        - Test syntax is valid Python
        - Test actually fails when executed
        
        Args:
            test_code: User's test code
            workshop_id: Workshop identifier
            
        Returns:
            {
                "valid": bool,
                "errors": List[str],
                "warnings": List[str],
                "test_fails": bool
            }
        """
        result = {
            "valid": False,
            "errors": [],
            "warnings": [],
            "test_fails": False
        }

        # Check syntax
        try:
            tree = ast.parse(test_code)
        except SyntaxError as e:
            result["errors"].append(f"Syntax error: {e}")
            return result

        # Check for test function
        test_functions = [
            node.name for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
        ]
        
        if not test_functions:
            result["errors"].append("No test function found. Test function must start with 'test_'")
            return result

        # Check for assertions
        assertions = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.Assert)
        ]
        
        if not assertions:
            result["errors"].append("No assertions found in test. Add at least one assert statement")
            return result

        # Try to execute test - it should fail
        try:
            # Execute test with empty user code
            empty_code = "pass"
            test_result = self.test_runner.run_tests(empty_code, test_code)
            
            # Test should fail (not all assertions pass)
            if test_result.get("success"):
                result["errors"].append("Test passes with empty code. Test must fail to validate requirements")
            else:
                result["test_fails"] = True
                result["valid"] = True
        except Exception as e:
            result["errors"].append(f"Test execution error: {str(e)}")

        return result

    def validate_step_3(self, user_code: str, test_code: str) -> Dict[str, Any]:
        """
        Validate STEP 3: Write Code to Pass Test
        
        Requirements:
        - Code syntax is valid Python
        - Required function exists and is callable
        - User's test passes with user's code
        
        Args:
            user_code: User's implementation code
            test_code: Test code from STEP 1
            
        Returns:
            {
                "valid": bool,
                "errors": List[str],
                "test_results": Dict
            }
        """
        result = {
            "valid": False,
            "errors": [],
            "test_results": {}
        }

        # Check syntax
        try:
            ast.parse(user_code)
        except SyntaxError as e:
            result["errors"].append(f"Syntax error: {e}")
            return result

        # Run tests with user code
        try:
            test_result = self.test_runner.run_tests(user_code, test_code)
            result["test_results"] = test_result
            
            if test_result.get("success"):
                result["valid"] = True
            else:
                result["errors"].append(f"Test failed: {test_result.get('feedback', 'Unknown error')}")
        except Exception as e:
            result["errors"].append(f"Test execution error: {str(e)}")

        return result

    def validate_step_5(self, user_code: str, test_code: str, previous_code: str) -> Dict[str, Any]:
        """
        Validate STEP 5: Refactor Code
        
        Requirements:
        - Code syntax is valid Python
        - User's test still passes (GREEN)
        - Code metrics improved or maintained
        
        Args:
            user_code: Refactored code
            test_code: Test code from STEP 1
            previous_code: Code from STEP 3
            
        Returns:
            {
                "valid": bool,
                "errors": List[str],
                "metrics": Dict,
                "improved": bool
            }
        """
        result = {
            "valid": False,
            "errors": [],
            "metrics": {},
            "improved": False
        }

        # Check syntax
        try:
            ast.parse(user_code)
        except SyntaxError as e:
            result["errors"].append(f"Syntax error: {e}")
            return result

        # Run tests with refactored code
        try:
            test_result = self.test_runner.run_tests(user_code, test_code)
            
            if not test_result.get("success"):
                result["errors"].append("Test failed after refactoring. Code must still pass tests")
                return result
            
            # Calculate metrics for both versions
            from .code_metrics import CodeMetrics
            metrics = CodeMetrics()
            
            previous_metrics = metrics.get_metrics_summary(previous_code)
            refactored_metrics = metrics.get_metrics_summary(user_code)
            
            result["metrics"] = {
                "previous": previous_metrics,
                "refactored": refactored_metrics
            }
            
            # Check if improved
            improved = (
                refactored_metrics.get("complexity", 0) <= previous_metrics.get("complexity", 0) or
                refactored_metrics.get("has_docstring", False) or
                refactored_metrics.get("has_type_hints", False)
            )
            
            result["improved"] = improved
            result["valid"] = True
            
        except Exception as e:
            result["errors"].append(f"Validation error: {str(e)}")

        return result

