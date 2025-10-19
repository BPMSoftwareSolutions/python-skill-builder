"""
Unit tests for TDD workflow schema and services
"""

import pytest
from app.schemas.tdd_workflow import StepContent, TDDWorkflowDefinition
from app.schemas.workshop import Workshop
from app.services.hints_analyzer import HintsAnalyzer
from app.services.error_messages import ErrorMessageGenerator, ErrorMessage
from app.schemas.validation import WorkshopValidator


class TestStepContent:
    """Tests for StepContent schema"""

    def test_create_step_content(self):
        """Test creating step content"""
        step = StepContent(
            objective="Write a failing test",
            instruction="Create a test for add(2, 3)",
            requirements=["Test name starts with test_", "Has assertion"],
            starter_code="def test_():\n    pass",
            example_code="def test_add():\n    assert add(2, 3) == 5",
            hints=["Use assert", "Follow naming convention"],
            success_criteria=["Test fails"],
            error_messages={"TEST_NAME_INVALID": "Test name must start with test_"}
        )
        assert step.objective == "Write a failing test"
        assert len(step.requirements) == 2
        assert len(step.hints) == 2

    def test_step_content_to_dict(self):
        """Test converting step content to dictionary"""
        step = StepContent(
            objective="Test objective",
            instruction="Test instruction",
            requirements=["Req 1"],
            hints=["Hint 1"]
        )
        data = step.to_dict()
        assert data['objective'] == "Test objective"
        assert data['instruction'] == "Test instruction"
        assert data['requirements'] == ["Req 1"]

    def test_step_content_from_dict(self):
        """Test creating step content from dictionary"""
        data = {
            'objective': 'Test objective',
            'instruction': 'Test instruction',
            'requirements': ['Req 1'],
            'hints': ['Hint 1']
        }
        step = StepContent.from_dict(data)
        assert step.objective == 'Test objective'
        assert step.requirements == ['Req 1']


class TestTDDWorkflowDefinition:
    """Tests for TDDWorkflowDefinition schema"""

    def test_create_workflow(self):
        """Test creating a TDD workflow"""
        step1 = StepContent(
            objective="Write test",
            instruction="Create test"
        )
        workflow = TDDWorkflowDefinition(
            feature_description="add(a, b) - Add two numbers",
            step_1_red_write_test=step1
        )
        assert workflow.feature_description == "add(a, b) - Add two numbers"
        assert workflow.step_1_red_write_test == step1

    def test_get_step(self):
        """Test getting a step by number"""
        step1 = StepContent(objective="Step 1", instruction="Do step 1")
        step3 = StepContent(objective="Step 3", instruction="Do step 3")
        workflow = TDDWorkflowDefinition(
            feature_description="Test feature",
            step_1_red_write_test=step1,
            step_3_green_write_code=step3
        )
        assert workflow.get_step(1) == step1
        assert workflow.get_step(3) == step3
        assert workflow.get_step(2) is None

    def test_workflow_to_dict(self):
        """Test converting workflow to dictionary"""
        step1 = StepContent(objective="Step 1", instruction="Do step 1")
        workflow = TDDWorkflowDefinition(
            feature_description="Test feature",
            step_1_red_write_test=step1
        )
        data = workflow.to_dict()
        assert data['feature_description'] == "Test feature"
        assert 'step_1_red_write_test' in data

    def test_workflow_from_dict(self):
        """Test creating workflow from dictionary"""
        data = {
            'feature_description': 'Test feature',
            'step_1_red_write_test': {
                'objective': 'Step 1',
                'instruction': 'Do step 1'
            }
        }
        workflow = TDDWorkflowDefinition.from_dict(data)
        assert workflow.feature_description == 'Test feature'
        assert workflow.step_1_red_write_test.objective == 'Step 1'


class TestHintsAnalyzer:
    """Tests for HintsAnalyzer service"""

    @pytest.fixture
    def sample_workflow(self):
        """Create a sample workflow for testing"""
        step1 = StepContent(
            objective="Write test",
            instruction="Create test",
            hints=["Hint 1", "Hint 2", "Hint 3"],
            example_code="def test_add():\n    assert add(2, 3) == 5"
        )
        step3 = StepContent(
            objective="Write code",
            instruction="Implement function",
            hints=["Start simple"],
            example_code="def add(a, b):\n    return a + b"
        )
        return TDDWorkflowDefinition(
            feature_description="add(a, b)",
            step_1_red_write_test=step1,
            step_3_green_write_code=step3
        )

    def test_get_hints_for_step(self, sample_workflow):
        """Test getting hints for a step"""
        analyzer = HintsAnalyzer(sample_workflow)
        hints = analyzer.get_hints_for_step(1)
        assert len(hints) == 3
        assert hints[0] == "Hint 1"

    def test_get_progressive_hints_level_1(self, sample_workflow):
        """Test getting level 1 progressive hints"""
        analyzer = HintsAnalyzer(sample_workflow)
        hints = analyzer.get_progressive_hints(1, 1)
        assert len(hints) >= 1

    def test_get_progressive_hints_level_3(self, sample_workflow):
        """Test getting level 3 progressive hints (with example)"""
        analyzer = HintsAnalyzer(sample_workflow)
        hints = analyzer.get_progressive_hints(1, 3)
        assert any("Example:" in h for h in hints)

    def test_get_example_code(self, sample_workflow):
        """Test getting example code"""
        analyzer = HintsAnalyzer(sample_workflow)
        code = analyzer.get_example_code(1)
        assert "def test_add" in code

    def test_get_solution_code(self, sample_workflow):
        """Test getting solution code"""
        analyzer = HintsAnalyzer(sample_workflow)
        code = analyzer.get_solution_code(3)
        assert "def add" in code

    def test_get_starter_code(self, sample_workflow):
        """Test getting starter code"""
        analyzer = HintsAnalyzer(sample_workflow)
        # Add starter code to step
        sample_workflow.step_1_red_write_test.starter_code = "def test_():\n    pass"
        code = analyzer.get_starter_code(1)
        assert "def test_" in code

    def test_get_step_requirements(self, sample_workflow):
        """Test getting step requirements"""
        sample_workflow.step_1_red_write_test.requirements = ["Req 1", "Req 2"]
        analyzer = HintsAnalyzer(sample_workflow)
        reqs = analyzer.get_step_requirements(1)
        assert len(reqs) == 2

    def test_get_success_criteria(self, sample_workflow):
        """Test getting success criteria"""
        sample_workflow.step_1_red_write_test.success_criteria = ["Criteria 1"]
        analyzer = HintsAnalyzer(sample_workflow)
        criteria = analyzer.get_success_criteria(1)
        assert len(criteria) == 1

    def test_analyzer_without_workflow(self):
        """Test analyzer without workflow"""
        analyzer = HintsAnalyzer(None)
        assert analyzer.get_hints_for_step(1) == []
        assert analyzer.get_example_code(1) is None


class TestErrorMessageGenerator:
    """Tests for ErrorMessageGenerator service"""

    def test_error_message_to_dict(self):
        """Test converting error message to dictionary"""
        error = ErrorMessage(
            type='error',
            code='TEST_NAME_INVALID',
            message='Test name must start with test_',
            hint='Use naming convention'
        )
        data = error.to_dict()
        assert data['type'] == 'error'
        assert data['code'] == 'TEST_NAME_INVALID'
        assert data['hint'] == 'Use naming convention'

    def test_generate_step_1_errors(self):
        """Test generating STEP 1 errors"""
        validation_result = {
            'test_name_invalid': True,
            'current_name': 'my_test'
        }
        errors = ErrorMessageGenerator.generate_step_1_errors(validation_result)
        assert len(errors) > 0
        assert errors[0].code == 'TEST_NAME_INVALID'

    def test_generate_step_1_no_assertions(self):
        """Test generating STEP 1 no assertions error"""
        validation_result = {'no_assertions': True}
        errors = ErrorMessageGenerator.generate_step_1_errors(validation_result)
        assert any(e.code == 'NO_ASSERTIONS' for e in errors)

    def test_generate_step_3_errors(self):
        """Test generating STEP 3 errors"""
        validation_result = {
            'function_not_found': True,
            'function_name': 'add'
        }
        errors = ErrorMessageGenerator.generate_step_3_errors(validation_result)
        assert len(errors) > 0
        assert errors[0].code == 'FUNCTION_NOT_FOUND'

    def test_generate_step_5_errors(self):
        """Test generating STEP 5 errors"""
        validation_result = {'no_improvement': True}
        errors = ErrorMessageGenerator.generate_step_5_errors(validation_result)
        assert any(e.code == 'NO_IMPROVEMENT' for e in errors)

    def test_generate_generic_error(self):
        """Test generating generic error"""
        error = ErrorMessageGenerator.generate_generic_error(
            'CUSTOM_ERROR',
            'Custom error message',
            'Custom hint'
        )
        assert error.code == 'CUSTOM_ERROR'
        assert error.message == 'Custom error message'


class TestWorkshopWithTDDWorkflow:
    """Tests for Workshop with TDD workflow"""

    def test_workshop_with_tdd_workflow(self):
        """Test creating workshop with TDD workflow"""
        step1 = StepContent(objective="Step 1", instruction="Do step 1")
        workflow = TDDWorkflowDefinition(
            feature_description="Test feature",
            step_1_red_write_test=step1
        )
        workshop = Workshop(
            id="test_workshop",
            title="Test Workshop",
            description="Test description",
            tdd_workflow=workflow
        )
        assert workshop.tdd_workflow == workflow

    def test_workshop_to_dict_with_workflow(self):
        """Test converting workshop with workflow to dict"""
        step1 = StepContent(objective="Step 1", instruction="Do step 1")
        workflow = TDDWorkflowDefinition(
            feature_description="Test feature",
            step_1_red_write_test=step1
        )
        workshop = Workshop(
            id="test_workshop",
            title="Test Workshop",
            description="Test description",
            tdd_workflow=workflow
        )
        data = workshop.to_dict()
        assert 'tdd_workflow' in data

    def test_workshop_from_dict_with_workflow(self):
        """Test creating workshop from dict with workflow"""
        data = {
            'id': 'test_workshop',
            'title': 'Test Workshop',
            'description': 'Test description',
            'tdd_workflow': {
                'feature_description': 'Test feature',
                'step_1_red_write_test': {
                    'objective': 'Step 1',
                    'instruction': 'Do step 1'
                }
            }
        }
        workshop = Workshop.from_dict(data)
        assert workshop.tdd_workflow is not None
        assert workshop.tdd_workflow.feature_description == 'Test feature'


class TestTDDWorkflowValidation:
    """Tests for TDD workflow validation"""

    def test_validate_tdd_workflow(self):
        """Test validating TDD workflow"""
        data = {
            'feature_description': 'Test feature',
            'step_1_red_write_test': {
                'objective': 'Step 1',
                'instruction': 'Do step 1'
            }
        }
        errors = WorkshopValidator.validate_tdd_workflow(data)
        assert len(errors) == 0

    def test_validate_tdd_workflow_missing_feature(self):
        """Test validating workflow without feature description"""
        data = {
            'step_1_red_write_test': {
                'objective': 'Step 1',
                'instruction': 'Do step 1'
            }
        }
        errors = WorkshopValidator.validate_tdd_workflow(data)
        assert any('feature_description' in e for e in errors)

    def test_validate_step_content(self):
        """Test validating step content"""
        data = {
            'objective': 'Test objective',
            'instruction': 'Test instruction'
        }
        errors = WorkshopValidator.validate_step_content(data)
        assert len(errors) == 0

    def test_validate_step_content_missing_objective(self):
        """Test validating step without objective"""
        data = {'instruction': 'Test instruction'}
        errors = WorkshopValidator.validate_step_content(data)
        assert any('objective' in e for e in errors)


class TestHintsAnalyzerEdgeCases:
    """Tests for HintsAnalyzer edge cases"""

    def test_analyze_error_with_matching_error_code(self):
        """Test analyzing error with matching error code"""
        step1 = StepContent(
            objective="Step 1",
            instruction="Do step 1",
            error_messages={
                "TEST_NAME_INVALID": "Test name must start with test_",
                "NO_ASSERTIONS": "No assertions found"
            }
        )
        workflow = TDDWorkflowDefinition(
            feature_description="Test",
            step_1_red_write_test=step1
        )
        analyzer = HintsAnalyzer(workflow)
        hints = analyzer.analyze_error_and_suggest_hints(1, "TEST_NAME_INVALID")
        assert len(hints) > 0
        assert "Test name" in hints[0]

    def test_analyze_error_without_matching_code(self):
        """Test analyzing error without matching error code"""
        step1 = StepContent(
            objective="Step 1",
            instruction="Do step 1",
            hints=["Hint 1", "Hint 2"],
            error_messages={"TEST_NAME_INVALID": "Test name error"}
        )
        workflow = TDDWorkflowDefinition(
            feature_description="Test",
            step_1_red_write_test=step1
        )
        analyzer = HintsAnalyzer(workflow)
        hints = analyzer.analyze_error_and_suggest_hints(1, "UNKNOWN_ERROR")
        assert len(hints) > 0

    def test_get_step_objective(self):
        """Test getting step objective"""
        step1 = StepContent(
            objective="Write a test",
            instruction="Do step 1"
        )
        workflow = TDDWorkflowDefinition(
            feature_description="Test",
            step_1_red_write_test=step1
        )
        analyzer = HintsAnalyzer(workflow)
        objective = analyzer.get_step_objective(1)
        assert objective == "Write a test"

    def test_get_step_instruction(self):
        """Test getting step instruction"""
        step1 = StepContent(
            objective="Step 1",
            instruction="Create a test for add(2, 3)"
        )
        workflow = TDDWorkflowDefinition(
            feature_description="Test",
            step_1_red_write_test=step1
        )
        analyzer = HintsAnalyzer(workflow)
        instruction = analyzer.get_step_instruction(1)
        assert instruction == "Create a test for add(2, 3)"

    def test_get_nonexistent_step(self):
        """Test getting nonexistent step"""
        step1 = StepContent(objective="Step 1", instruction="Do step 1")
        workflow = TDDWorkflowDefinition(
            feature_description="Test",
            step_1_red_write_test=step1
        )
        analyzer = HintsAnalyzer(workflow)
        assert analyzer.get_step_objective(99) is None
        assert analyzer.get_step_instruction(99) is None


class TestErrorMessageEdgeCases:
    """Tests for ErrorMessage edge cases"""

    def test_error_message_without_optional_fields(self):
        """Test error message without optional fields"""
        error = ErrorMessage(
            type='error',
            code='TEST_ERROR',
            message='Test error'
        )
        data = error.to_dict()
        assert 'current' not in data
        assert 'expected' not in data
        assert 'hint' not in data

    def test_generate_step_1_test_passed_error(self):
        """Test generating STEP 1 test passed error"""
        validation_result = {'test_passed_unexpectedly': True}
        errors = ErrorMessageGenerator.generate_step_1_errors(validation_result)
        assert any(e.code == 'TEST_PASSED' for e in errors)

    def test_generate_step_1_syntax_error(self):
        """Test generating STEP 1 syntax error"""
        validation_result = {
            'syntax_error': True,
            'error_details': 'Invalid syntax'
        }
        errors = ErrorMessageGenerator.generate_step_1_errors(validation_result)
        assert any(e.code == 'SYNTAX_ERROR' for e in errors)

    def test_generate_step_3_wrong_arg_count(self):
        """Test generating STEP 3 wrong argument count error"""
        validation_result = {
            'wrong_arg_count': True,
            'expected_args': 2,
            'actual_args': 1
        }
        errors = ErrorMessageGenerator.generate_step_3_errors(validation_result)
        assert any(e.code == 'WRONG_ARG_COUNT' for e in errors)

    def test_generate_step_3_test_failed(self):
        """Test generating STEP 3 test failed error"""
        validation_result = {
            'test_failed': True,
            'error_details': 'Expected 5, got None'
        }
        errors = ErrorMessageGenerator.generate_step_3_errors(validation_result)
        assert any(e.code == 'TEST_FAILED' for e in errors)

    def test_generate_step_5_test_failed(self):
        """Test generating STEP 5 test failed error"""
        validation_result = {'test_failed': True}
        errors = ErrorMessageGenerator.generate_step_5_errors(validation_result)
        assert any(e.code == 'TEST_FAILED' for e in errors)

    def test_generate_step_5_syntax_error(self):
        """Test generating STEP 5 syntax error"""
        validation_result = {
            'syntax_error': True,
            'error_details': 'Invalid syntax'
        }
        errors = ErrorMessageGenerator.generate_step_5_errors(validation_result)
        assert any(e.code == 'SYNTAX_ERROR' for e in errors)


class TestTDDWorkflowIntegration:
    """Integration tests for TDD workflow"""

    def test_complete_workflow_with_all_steps(self):
        """Test creating a complete workflow with all 6 steps"""
        steps = {
            1: StepContent(objective="Step 1", instruction="Do 1"),
            2: StepContent(objective="Step 2", instruction="Do 2"),
            3: StepContent(objective="Step 3", instruction="Do 3"),
            4: StepContent(objective="Step 4", instruction="Do 4"),
            5: StepContent(objective="Step 5", instruction="Do 5"),
            6: StepContent(objective="Step 6", instruction="Do 6"),
        }
        workflow = TDDWorkflowDefinition(
            feature_description="Complete workflow",
            step_1_red_write_test=steps[1],
            step_2_red_validation=steps[2],
            step_3_green_write_code=steps[3],
            step_4_green_validation=steps[4],
            step_5_refactor_improve=steps[5],
            step_6_refactor_validation=steps[6],
        )

        # Verify all steps are accessible
        for i in range(1, 7):
            assert workflow.get_step(i) is not None
            assert workflow.get_step(i).objective == f"Step {i}"

    def test_workflow_serialization_roundtrip(self):
        """Test workflow serialization and deserialization"""
        step1 = StepContent(
            objective="Write test",
            instruction="Create test",
            requirements=["Req 1"],
            hints=["Hint 1"],
            example_code="def test(): pass",
            error_messages={"ERROR": "Error message"}
        )
        workflow = TDDWorkflowDefinition(
            feature_description="Test feature",
            step_1_red_write_test=step1
        )

        # Serialize
        data = workflow.to_dict()

        # Deserialize
        workflow2 = TDDWorkflowDefinition.from_dict(data)

        # Verify
        assert workflow2.feature_description == workflow.feature_description
        assert workflow2.step_1_red_write_test.objective == step1.objective
        assert workflow2.step_1_red_write_test.requirements == step1.requirements

    def test_hints_analyzer_with_complete_workflow(self):
        """Test hints analyzer with complete workflow"""
        step1 = StepContent(
            objective="Write test",
            instruction="Create test",
            requirements=["Req 1", "Req 2"],
            hints=["Hint 1", "Hint 2", "Hint 3"],
            example_code="def test(): pass",
            success_criteria=["Criteria 1"],
            error_messages={"ERROR": "Error"}
        )
        workflow = TDDWorkflowDefinition(
            feature_description="Test",
            step_1_red_write_test=step1
        )
        analyzer = HintsAnalyzer(workflow)

        # Test all methods
        assert analyzer.get_step_objective(1) == "Write test"
        assert analyzer.get_step_instruction(1) == "Create test"
        assert len(analyzer.get_step_requirements(1)) == 2
        assert len(analyzer.get_hints_for_step(1)) == 3
        assert len(analyzer.get_success_criteria(1)) == 1
        assert analyzer.get_example_code(1) == "def test(): pass"

