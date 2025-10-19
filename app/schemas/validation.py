"""
Data Validation Module
Validates workshop schemas and provides helpful error messages
"""

from typing import Any, Dict, List, Tuple
from .workshop import Workshop, WorkshopPhases
from .test_suite import TestSuite, TestCase
from .mock_data import MockDataSet, MockDataPoint
from .phase_guidance import PhaseGuidance
from .tdd_workflow import TDDWorkflowDefinition, StepContent


class ValidationError(Exception):
    """Custom validation error"""
    pass


class WorkshopValidator:
    """Validates workshop data structures"""

    @staticmethod
    def validate_workshop(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate workshop data
        
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check required fields
        if not data.get('id'):
            errors.append("Workshop must have an 'id' field")
        if not data.get('title'):
            errors.append("Workshop must have a 'title' field")
        if not data.get('description'):
            errors.append("Workshop must have a 'description' field")
        
        # Validate difficulty
        valid_difficulties = ['beginner', 'intermediate', 'advanced']
        if data.get('difficulty') and data['difficulty'] not in valid_difficulties:
            errors.append(
                f"Difficulty must be one of {valid_difficulties}, "
                f"got '{data['difficulty']}'"
            )
        
        # Validate estimated_minutes
        if data.get('estimated_minutes'):
            if not isinstance(data['estimated_minutes'], int) or data['estimated_minutes'] <= 0:
                errors.append("estimated_minutes must be a positive integer")
        
        # Validate TDD structure if present
        if data.get('phases'):
            phase_errors = WorkshopValidator.validate_phases(data['phases'])
            errors.extend(phase_errors)

        # Validate TDD workflow if present
        if data.get('tdd_workflow'):
            workflow_errors = WorkshopValidator.validate_tdd_workflow(data['tdd_workflow'])
            errors.extend(workflow_errors)

        # Validate backward compatibility fields
        if data.get('prompt') and not isinstance(data['prompt'], str):
            errors.append("prompt must be a string")
        if data.get('starter_code') and not isinstance(data['starter_code'], str):
            errors.append("starter_code must be a string")
        if data.get('hints') and not isinstance(data['hints'], list):
            errors.append("hints must be a list")
        
        return len(errors) == 0, errors

    @staticmethod
    def validate_phases(data: Dict[str, Any]) -> List[str]:
        """Validate phases structure"""
        errors = []
        
        if not data.get('test_suite'):
            errors.append("Phases must have a 'test_suite' field")
        else:
            suite_errors = WorkshopValidator.validate_test_suite(data['test_suite'])
            errors.extend(suite_errors)
        
        if data.get('mock_data_sets'):
            if not isinstance(data['mock_data_sets'], dict):
                errors.append("mock_data_sets must be a dictionary")
            else:
                for set_id, mock_set in data['mock_data_sets'].items():
                    set_errors = WorkshopValidator.validate_mock_data_set(mock_set)
                    errors.extend([f"Mock set '{set_id}': {e}" for e in set_errors])
        
        if data.get('guidance'):
            guidance_errors = WorkshopValidator.validate_guidance(data['guidance'])
            errors.extend(guidance_errors)
        
        return errors

    @staticmethod
    def validate_test_suite(data: Dict[str, Any]) -> List[str]:
        """Validate test suite structure"""
        errors = []
        
        if not data.get('id'):
            errors.append("Test suite must have an 'id' field")
        if not data.get('name'):
            errors.append("Test suite must have a 'name' field")
        if not data.get('description'):
            errors.append("Test suite must have a 'description' field")
        
        if not data.get('tests'):
            errors.append("Test suite must have at least one test")
        elif isinstance(data['tests'], list):
            for i, test in enumerate(data['tests']):
                test_errors = WorkshopValidator.validate_test_case(test)
                errors.extend([f"Test {i}: {e}" for e in test_errors])
        else:
            errors.append("tests must be a list")
        
        return errors

    @staticmethod
    def validate_test_case(data: Dict[str, Any]) -> List[str]:
        """Validate test case structure"""
        errors = []
        
        if not data.get('id'):
            errors.append("Test must have an 'id' field")
        if not data.get('name'):
            errors.append("Test must have a 'name' field")
        if not data.get('description'):
            errors.append("Test must have a 'description' field")
        if not data.get('assertion'):
            errors.append("Test must have an 'assertion' field")
        if 'expected' not in data:
            errors.append("Test must have an 'expected' field")
        
        if data.get('assertion_type'):
            valid_types = [
                'assertEqual', 'assertNotEqual', 'assertTrue', 'assertFalse',
                'assertIn', 'assertNotIn', 'assertRaises', 'assertAlmostEqual',
                'assertGreater', 'assertLess', 'assertGreaterEqual', 'assertLessEqual'
            ]
            if data['assertion_type'] not in valid_types:
                errors.append(f"Invalid assertion_type: {data['assertion_type']}")
        
        if data.get('difficulty'):
            valid_difficulties = ['easy', 'medium', 'hard']
            if data['difficulty'] not in valid_difficulties:
                errors.append(f"Test difficulty must be one of {valid_difficulties}")
        
        return errors

    @staticmethod
    def validate_mock_data_set(data: Dict[str, Any]) -> List[str]:
        """Validate mock data set structure"""
        errors = []
        
        if not data.get('id'):
            errors.append("Mock data set must have an 'id' field")
        if not data.get('name'):
            errors.append("Mock data set must have a 'name' field")
        if not data.get('description'):
            errors.append("Mock data set must have a 'description' field")
        
        if not data.get('data_points'):
            errors.append("Mock data set must have at least one data point")
        elif isinstance(data['data_points'], list):
            for i, point in enumerate(data['data_points']):
                point_errors = WorkshopValidator.validate_mock_data_point(point)
                errors.extend([f"Data point {i}: {e}" for e in point_errors])
        else:
            errors.append("data_points must be a list")
        
        return errors

    @staticmethod
    def validate_mock_data_point(data: Dict[str, Any]) -> List[str]:
        """Validate mock data point structure"""
        errors = []
        
        if 'inputs' not in data:
            errors.append("Data point must have an 'inputs' field")
        elif not isinstance(data['inputs'], list):
            errors.append("inputs must be a list")
        
        if 'expected' not in data:
            errors.append("Data point must have an 'expected' field")
        
        return errors

    @staticmethod
    def validate_guidance(data: Dict[str, Any]) -> List[str]:
        """Validate phase guidance structure"""
        errors = []

        for phase in ['red', 'green', 'refactor']:
            if not data.get(phase):
                errors.append(f"Guidance must have a '{phase}' phase")
            else:
                phase_data = data[phase]
                if not phase_data.get('objective'):
                    errors.append(f"{phase.upper()} phase must have an 'objective'")
                if not phase_data.get('guidance'):
                    errors.append(f"{phase.upper()} phase must have 'guidance' text")

        return errors

    @staticmethod
    def validate_tdd_workflow(data: Dict[str, Any]) -> List[str]:
        """Validate TDD workflow structure"""
        errors = []

        # Check required fields
        if not data.get('feature_description'):
            errors.append("TDD workflow must have a 'feature_description' field")

        # Check step 1 (required)
        if not data.get('step_1_red_write_test'):
            errors.append("TDD workflow must have 'step_1_red_write_test'")
        else:
            step_errors = WorkshopValidator.validate_step_content(data['step_1_red_write_test'])
            errors.extend([f"Step 1: {e}" for e in step_errors])

        # Check optional steps
        for step_num in [2, 3, 4, 5, 6]:
            step_key = f'step_{step_num}_' + {
                2: 'red_validation',
                3: 'green_write_code',
                4: 'green_validation',
                5: 'refactor_improve',
                6: 'refactor_validation'
            }[step_num]

            if data.get(step_key):
                step_errors = WorkshopValidator.validate_step_content(data[step_key])
                errors.extend([f"Step {step_num}: {e}" for e in step_errors])

        return errors

    @staticmethod
    def validate_step_content(data: Dict[str, Any]) -> List[str]:
        """Validate step content structure"""
        errors = []

        # Check required fields
        if not data.get('objective'):
            errors.append("Step must have an 'objective' field")
        if not data.get('instruction'):
            errors.append("Step must have an 'instruction' field")

        # Check optional fields are correct types
        if data.get('requirements') and not isinstance(data['requirements'], list):
            errors.append("'requirements' must be a list")
        if data.get('hints') and not isinstance(data['hints'], list):
            errors.append("'hints' must be a list")
        if data.get('success_criteria') and not isinstance(data['success_criteria'], list):
            errors.append("'success_criteria' must be a list")
        if data.get('error_messages') and not isinstance(data['error_messages'], dict):
            errors.append("'error_messages' must be a dictionary")

        return errors

