"""
Error Message Generator Service
Generates human-friendly error messages for each TDD step
"""

from typing import List, Dict, Any, Optional


class ErrorMessage:
    """Represents a single error message"""
    
    def __init__(
        self,
        type: str,
        code: str,
        message: str,
        current: Optional[str] = None,
        expected: Optional[str] = None,
        hint: Optional[str] = None
    ):
        """
        Initialize error message
        
        Args:
            type: 'error' or 'warning'
            code: Error code (e.g., 'TEST_NAME_INVALID')
            message: Human-friendly message
            current: Current value
            expected: Expected value
            hint: Helpful hint
        """
        self.type = type
        self.code = code
        self.message = message
        self.current = current
        self.expected = expected
        self.hint = hint
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = {
            'type': self.type,
            'code': self.code,
            'message': self.message,
        }
        if self.current:
            data['current'] = self.current
        if self.expected:
            data['expected'] = self.expected
        if self.hint:
            data['hint'] = self.hint
        return data


class ErrorMessageGenerator:
    """Generates step-specific error messages"""

    @staticmethod
    def generate_step_1_errors(validation_result: Dict[str, Any]) -> List[ErrorMessage]:
        """
        Generate STEP 1 (RED - Write Test) error messages
        
        Args:
            validation_result: Validation result from step validator
            
        Returns:
            List of error messages
        """
        errors = []
        
        # Check for test name validation
        if validation_result.get('test_name_invalid'):
            errors.append(ErrorMessage(
                type='error',
                code='TEST_NAME_INVALID',
                message='Test name must start with "test_"',
                current=validation_result.get('current_name'),
                expected='test_<function>_<scenario>',
                hint='Follow naming convention: test_<function>_<scenario>'
            ))
        
        # Check for missing assertions
        if validation_result.get('no_assertions'):
            errors.append(ErrorMessage(
                type='error',
                code='NO_ASSERTIONS',
                message='No assertions found in test',
                hint='Use "assert" to check the result: assert result == expected'
            ))
        
        # Check if test passed when it should fail
        if validation_result.get('test_passed_unexpectedly'):
            errors.append(ErrorMessage(
                type='error',
                code='TEST_PASSED',
                message='Test passed, but it should fail!',
                hint='The function doesn\'t exist yet, so the test should fail'
            ))
        
        # Check for syntax errors
        if validation_result.get('syntax_error'):
            errors.append(ErrorMessage(
                type='error',
                code='SYNTAX_ERROR',
                message='Syntax error in test code',
                current=validation_result.get('error_details'),
                hint='Check your Python syntax'
            ))
        
        return errors

    @staticmethod
    def generate_step_3_errors(validation_result: Dict[str, Any]) -> List[ErrorMessage]:
        """
        Generate STEP 3 (GREEN - Write Code) error messages
        
        Args:
            validation_result: Validation result from step validator
            
        Returns:
            List of error messages
        """
        errors = []
        
        # Check if function not found
        if validation_result.get('function_not_found'):
            errors.append(ErrorMessage(
                type='error',
                code='FUNCTION_NOT_FOUND',
                message=f'Function "{validation_result.get("function_name")}" not defined',
                hint='Create a function with the correct name'
            ))
        
        # Check for wrong number of arguments
        if validation_result.get('wrong_arg_count'):
            errors.append(ErrorMessage(
                type='error',
                code='WRONG_ARG_COUNT',
                message=f'Function requires {validation_result.get("expected_args")} arguments but got {validation_result.get("actual_args")}',
                hint='Check the function signature'
            ))
        
        # Check if test failed
        if validation_result.get('test_failed'):
            errors.append(ErrorMessage(
                type='error',
                code='TEST_FAILED',
                message='Your test failed with your code',
                current=validation_result.get('error_details'),
                hint='Check the error message and adjust your implementation'
            ))
        
        # Check for syntax errors
        if validation_result.get('syntax_error'):
            errors.append(ErrorMessage(
                type='error',
                code='SYNTAX_ERROR',
                message='Syntax error in code',
                current=validation_result.get('error_details'),
                hint='Check your Python syntax'
            ))
        
        return errors

    @staticmethod
    def generate_step_5_errors(validation_result: Dict[str, Any]) -> List[ErrorMessage]:
        """
        Generate STEP 5 (REFACTOR - Improve Code) error messages
        
        Args:
            validation_result: Validation result from step validator
            
        Returns:
            List of error messages
        """
        errors = []
        
        # Check if test still passes
        if validation_result.get('test_failed'):
            errors.append(ErrorMessage(
                type='error',
                code='TEST_FAILED',
                message='Test failed after refactoring',
                hint='Keep the functionality the same! Only improve style and quality.'
            ))
        
        # Check if code was improved
        if validation_result.get('no_improvement'):
            errors.append(ErrorMessage(
                type='warning',
                code='NO_IMPROVEMENT',
                message='Code not improved',
                hint='Try adding type hints, docstring, or improving variable names'
            ))
        
        # Check for syntax errors
        if validation_result.get('syntax_error'):
            errors.append(ErrorMessage(
                type='error',
                code='SYNTAX_ERROR',
                message='Syntax error in refactored code',
                current=validation_result.get('error_details'),
                hint='Check your Python syntax'
            ))
        
        return errors

    @staticmethod
    def generate_generic_error(
        error_code: str,
        message: str,
        hint: Optional[str] = None,
        error_type: str = 'error'
    ) -> ErrorMessage:
        """
        Generate a generic error message
        
        Args:
            error_code: Error code
            message: Error message
            hint: Optional hint
            error_type: 'error' or 'warning'
            
        Returns:
            Error message
        """
        return ErrorMessage(
            type=error_type,
            code=error_code,
            message=message,
            hint=hint
        )

