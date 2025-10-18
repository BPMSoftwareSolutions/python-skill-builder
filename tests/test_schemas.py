"""
Unit tests for workshop schemas and validation
"""

import pytest
from app.schemas.test_suite import TestCase, TestSuite, AssertionType
from app.schemas.mock_data import MockDataPoint, MockDataSet
from app.schemas.phase_guidance import (
    RedPhaseGuidance, GreenPhaseGuidance, RefactorPhaseGuidance, PhaseGuidance
)
from app.schemas.workshop import Workshop, WorkshopPhases
from app.schemas.validation import WorkshopValidator, ValidationError


class TestTestCase:
    """Tests for TestCase schema"""

    def test_create_test_case(self):
        """Test creating a test case"""
        test = TestCase(
            id="test_1",
            name="test_add_positive",
            description="Add two positive numbers",
            assertion="assertEqual(add(2, 3), 5)",
            assertion_type=AssertionType.EQUAL,
            expected=5,
            inputs=[2, 3],
            difficulty="easy"
        )
        assert test.id == "test_1"
        assert test.name == "test_add_positive"
        assert test.expected == 5

    def test_test_case_to_dict(self):
        """Test converting test case to dictionary"""
        test = TestCase(
            id="test_1",
            name="test_add",
            description="Add test",
            assertion="assertEqual(add(2, 3), 5)",
            assertion_type=AssertionType.EQUAL,
            expected=5,
            inputs=[2, 3]
        )
        data = test.to_dict()
        assert data['id'] == "test_1"
        assert data['assertion_type'] == "assertEqual"

    def test_test_case_from_dict(self):
        """Test creating test case from dictionary"""
        data = {
            'id': 'test_1',
            'name': 'test_add',
            'description': 'Add test',
            'assertion': 'assertEqual(add(2, 3), 5)',
            'assertion_type': 'assertEqual',
            'expected': 5,
            'inputs': [2, 3]
        }
        test = TestCase.from_dict(data)
        assert test.id == 'test_1'
        assert test.expected == 5


class TestTestSuite:
    """Tests for TestSuite schema"""

    def test_create_test_suite(self):
        """Test creating a test suite"""
        suite = TestSuite(
            id="suite_1",
            name="Add Function Tests",
            description="Tests for add function"
        )
        assert suite.id == "suite_1"
        assert suite.total_tests == 0

    def test_add_test_to_suite(self):
        """Test adding tests to suite"""
        suite = TestSuite(
            id="suite_1",
            name="Add Function Tests",
            description="Tests for add function"
        )
        test = TestCase(
            id="test_1",
            name="test_add",
            description="Add test",
            assertion="assertEqual(add(2, 3), 5)",
            assertion_type=AssertionType.EQUAL,
            expected=5
        )
        suite.add_test(test)
        assert suite.total_tests == 1

    def test_get_test_from_suite(self):
        """Test getting a test from suite"""
        suite = TestSuite(
            id="suite_1",
            name="Add Function Tests",
            description="Tests for add function"
        )
        test = TestCase(
            id="test_1",
            name="test_add",
            description="Add test",
            assertion="assertEqual(add(2, 3), 5)",
            assertion_type=AssertionType.EQUAL,
            expected=5
        )
        suite.add_test(test)
        retrieved = suite.get_test("test_1")
        assert retrieved is not None
        assert retrieved.id == "test_1"


class TestMockDataPoint:
    """Tests for MockDataPoint schema"""

    def test_create_mock_data_point(self):
        """Test creating a mock data point"""
        point = MockDataPoint(
            inputs=[2, 3],
            expected=5,
            description="Simple addition"
        )
        assert point.inputs == [2, 3]
        assert point.expected == 5

    def test_mock_data_point_to_dict(self):
        """Test converting mock data point to dictionary"""
        point = MockDataPoint(
            inputs=[2, 3],
            expected=5
        )
        data = point.to_dict()
        assert data['inputs'] == [2, 3]
        assert data['expected'] == 5


class TestMockDataSet:
    """Tests for MockDataSet schema"""

    def test_create_mock_data_set(self):
        """Test creating a mock data set"""
        mock_set = MockDataSet(
            id="valid",
            name="Valid Inputs",
            description="Basic positive numbers"
        )
        assert mock_set.id == "valid"
        assert mock_set.total_points == 0

    def test_add_data_point_to_set(self):
        """Test adding data points to set"""
        mock_set = MockDataSet(
            id="valid",
            name="Valid Inputs",
            description="Basic positive numbers"
        )
        point = MockDataPoint(inputs=[2, 3], expected=5)
        mock_set.add_data_point(point)
        assert mock_set.total_points == 1

    def test_get_data_point_from_set(self):
        """Test getting data point from set"""
        mock_set = MockDataSet(
            id="valid",
            name="Valid Inputs",
            description="Basic positive numbers"
        )
        point = MockDataPoint(inputs=[2, 3], expected=5)
        mock_set.add_data_point(point)
        retrieved = mock_set.get_data_point(0)
        assert retrieved is not None
        assert retrieved.expected == 5


class TestPhaseGuidance:
    """Tests for PhaseGuidance schemas"""

    def test_create_red_phase_guidance(self):
        """Test creating RED phase guidance"""
        red = RedPhaseGuidance(
            objective="Understand requirements",
            guidance="Read the tests carefully",
            hints=["Look at test names", "Check assertions"]
        )
        assert red.objective == "Understand requirements"
        assert len(red.hints) == 2

    def test_create_green_phase_guidance(self):
        """Test creating GREEN phase guidance"""
        green = GreenPhaseGuidance(
            objective="Make tests pass",
            guidance="Write simple code",
            minimum_requirements="All tests must pass",
            hints=["Start simple"]
        )
        assert green.objective == "Make tests pass"
        assert green.minimum_requirements == "All tests must pass"

    def test_create_refactor_phase_guidance(self):
        """Test creating REFACTOR phase guidance"""
        refactor = RefactorPhaseGuidance(
            objective="Improve code quality",
            guidance="Keep tests green",
            guidelines=["Reduce complexity"],
            code_metrics={"target_complexity": 1}
        )
        assert refactor.objective == "Improve code quality"
        assert refactor.code_metrics["target_complexity"] == 1

    def test_create_complete_phase_guidance(self):
        """Test creating complete phase guidance"""
        red = RedPhaseGuidance(
            objective="Understand",
            guidance="Read tests"
        )
        green = GreenPhaseGuidance(
            objective="Implement",
            guidance="Make pass",
            minimum_requirements="All pass"
        )
        refactor = RefactorPhaseGuidance(
            objective="Improve",
            guidance="Keep green"
        )
        guidance = PhaseGuidance(red=red, green=green, refactor=refactor)
        assert guidance.red.objective == "Understand"
        assert guidance.green.objective == "Implement"
        assert guidance.refactor.objective == "Improve"


class TestWorkshop:
    """Tests for Workshop schema"""

    def test_create_basic_workshop(self):
        """Test creating a basic workshop"""
        workshop = Workshop(
            id="add_function",
            title="Add Function",
            description="Learn to add numbers"
        )
        assert workshop.id == "add_function"
        assert not workshop.has_tdd_structure()

    def test_create_tdd_workshop(self):
        """Test creating a TDD workshop"""
        suite = TestSuite(
            id="suite_1",
            name="Tests",
            description="Test suite"
        )
        phases = WorkshopPhases(test_suite=suite)
        workshop = Workshop(
            id="add_function",
            title="Add Function",
            description="Learn to add numbers",
            phases=phases
        )
        assert workshop.has_tdd_structure()

    def test_workshop_backward_compatibility(self):
        """Test workshop backward compatibility"""
        workshop = Workshop(
            id="add_function",
            title="Add Function",
            description="Learn to add numbers",
            prompt="Implement add function",
            starter_code="def add(a, b):\n    pass",
            hints=["Use + operator"]
        )
        assert workshop.prompt == "Implement add function"
        assert len(workshop.hints) == 1


class TestWorkshopValidator:
    """Tests for WorkshopValidator"""

    def test_validate_valid_workshop(self):
        """Test validating a valid workshop"""
        data = {
            'id': 'add_function',
            'title': 'Add Function',
            'description': 'Learn to add'
        }
        is_valid, errors = WorkshopValidator.validate_workshop(data)
        assert is_valid
        assert len(errors) == 0

    def test_validate_missing_required_fields(self):
        """Test validating workshop with missing fields"""
        data = {
            'id': 'add_function'
        }
        is_valid, errors = WorkshopValidator.validate_workshop(data)
        assert not is_valid
        assert len(errors) > 0

    def test_validate_invalid_difficulty(self):
        """Test validating workshop with invalid difficulty"""
        data = {
            'id': 'add_function',
            'title': 'Add Function',
            'description': 'Learn to add',
            'difficulty': 'invalid'
        }
        is_valid, errors = WorkshopValidator.validate_workshop(data)
        assert not is_valid

    def test_validate_valid_test_suite(self):
        """Test validating a valid test suite"""
        data = {
            'id': 'suite_1',
            'name': 'Tests',
            'description': 'Test suite',
            'tests': [
                {
                    'id': 'test_1',
                    'name': 'test_add',
                    'description': 'Add test',
                    'assertion': 'assertEqual(add(2, 3), 5)',
                    'assertion_type': 'assertEqual',
                    'expected': 5
                }
            ]
        }
        errors = WorkshopValidator.validate_test_suite(data)
        assert len(errors) == 0

    def test_validate_valid_mock_data_set(self):
        """Test validating a valid mock data set"""
        data = {
            'id': 'valid',
            'name': 'Valid Inputs',
            'description': 'Basic numbers',
            'data_points': [
                {
                    'inputs': [2, 3],
                    'expected': 5
                }
            ]
        }
        errors = WorkshopValidator.validate_mock_data_set(data)
        assert len(errors) == 0

    def test_validate_valid_guidance(self):
        """Test validating valid guidance"""
        data = {
            'red': {
                'objective': 'Understand',
                'guidance': 'Read tests'
            },
            'green': {
                'objective': 'Implement',
                'guidance': 'Make pass'
            },
            'refactor': {
                'objective': 'Improve',
                'guidance': 'Keep green'
            }
        }
        errors = WorkshopValidator.validate_guidance(data)
        assert len(errors) == 0

    def test_validate_missing_guidance_phase(self):
        """Test validating guidance with missing phase"""
        data = {
            'red': {
                'objective': 'Understand',
                'guidance': 'Read tests'
            }
        }
        errors = WorkshopValidator.validate_guidance(data)
        assert len(errors) > 0

    def test_validate_invalid_test_case(self):
        """Test validating invalid test case"""
        data = {
            'id': 'test_1'
        }
        errors = WorkshopValidator.validate_test_case(data)
        assert len(errors) > 0

    def test_validate_invalid_mock_data_point(self):
        """Test validating invalid mock data point"""
        data = {
            'inputs': [2, 3]
        }
        errors = WorkshopValidator.validate_mock_data_point(data)
        assert len(errors) > 0


class TestWorkshopSerialization:
    """Tests for workshop serialization"""

    def test_workshop_to_dict_and_back(self):
        """Test workshop serialization and deserialization"""
        suite = TestSuite(
            id="suite_1",
            name="Tests",
            description="Test suite"
        )
        test = TestCase(
            id="test_1",
            name="test_add",
            description="Add test",
            assertion="assertEqual(add(2, 3), 5)",
            assertion_type=AssertionType.EQUAL,
            expected=5
        )
        suite.add_test(test)

        phases = WorkshopPhases(test_suite=suite)
        workshop = Workshop(
            id="add_function",
            title="Add Function",
            description="Learn to add",
            phases=phases
        )

        data = workshop.to_dict()
        restored = Workshop.from_dict(data)

        assert restored.id == workshop.id
        assert restored.title == workshop.title
        assert restored.has_tdd_structure()

    def test_mock_data_set_serialization(self):
        """Test mock data set serialization"""
        mock_set = MockDataSet(
            id="valid",
            name="Valid Inputs",
            description="Basic numbers"
        )
        point = MockDataPoint(inputs=[2, 3], expected=5)
        mock_set.add_data_point(point)

        data = mock_set.to_dict()
        restored = MockDataSet.from_dict(data)

        assert restored.id == mock_set.id
        assert restored.total_points == 1

    def test_phase_guidance_serialization(self):
        """Test phase guidance serialization"""
        red = RedPhaseGuidance(
            objective="Understand",
            guidance="Read tests",
            hints=["Look at names"]
        )
        green = GreenPhaseGuidance(
            objective="Implement",
            guidance="Make pass",
            minimum_requirements="All pass"
        )
        refactor = RefactorPhaseGuidance(
            objective="Improve",
            guidance="Keep green"
        )
        guidance = PhaseGuidance(red=red, green=green, refactor=refactor)

        data = guidance.to_dict()
        restored = PhaseGuidance.from_dict(data)

        assert restored.red.objective == red.objective
        assert restored.green.objective == green.objective
        assert restored.refactor.objective == refactor.objective

