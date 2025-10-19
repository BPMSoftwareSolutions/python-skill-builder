"""
Flask Training App - Python Interview Prep
Provides API endpoints for training modules and code grading with sandboxed execution.
"""

from flask import Flask, send_from_directory, jsonify, request
import json
import ast
import time
import traceback
import sys
import os

# Add app directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import test runner services
from app.services.test_runner import TestRunner
from app.services.test_executor import TestExecutor
from app.services.test_formatter import TestFormatter
from app.services.workflow_state import TDDWorkflowState
from app.services.step_validator import StepValidator
from app.services.workflow_storage import WorkflowStorage
from app.services.code_metrics import CodeMetrics
from app.services.workflow_progress import WorkflowProgress
from app.services.achievements import AchievementTracker
from app.services.badges import BadgeDisplay
from app.services.user_stats import StatsCalculator

app = Flask(__name__, static_folder="static", static_url_path="")

# Initialize services
workflow_storage = WorkflowStorage("workflows")
achievement_tracker = AchievementTracker("workflows")
badge_display = BadgeDisplay()
stats_calculator = StatsCalculator("workflows")

# ------- Modules API -------
@app.get("/api/modules")
def list_modules():
    """Return catalog of all available training modules."""
    with open("modules/module_index.json", "r", encoding="utf-8") as f:
        return jsonify(json.load(f))

@app.get("/api/modules/<mod_id>")
def get_module(mod_id):
    """Return specific module with all workshops."""
    try:
        with open(f"modules/{mod_id}.json", "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({"error": "Module not found"}), 404

# ------- Safe execution sandbox -------
DISALLOWED_NODES = (
    ast.Global, ast.Nonlocal, ast.With, ast.AsyncWith
    # Removed Try, Raise, Attribute to allow basic Python operations
    # Removed Lambda to allow functional programming patterns (issue #31)
)

# Allowed imports for AOP approaches and specific exercises
ALLOWED_IMPORTS = {
    'functools': ['wraps'],  # Required for decorators
    'time': ['sleep', 'time', 'perf_counter'],  # Required for timing/retry decorators
    'numpy': None,  # Allow all numpy imports (for numpy exercises)
}

SAFE_BUILTINS = {
    "len": len, "range": range, "sum": sum, "min": min, "max": max, "abs": abs,
    "enumerate": enumerate, "zip": zip, "sorted": sorted, "all": all, "any": any,
    "map": map, "filter": filter,  # Required for functional programming with lambda
    "list": list, "dict": dict, "set": set, "tuple": tuple, "str": str, "int": int,
    "float": float, "bool": bool, "print": print, "isinstance": isinstance, "type": type,
    "repr": repr, "getattr": getattr, "setattr": setattr, "hasattr": hasattr,  # Object attribute access
    "Exception": Exception, "ValueError": ValueError, "TypeError": TypeError,
    "KeyError": KeyError, "IndexError": IndexError, "AttributeError": AttributeError,
    "NameError": NameError, "ImportError": ImportError,  # Required for error handling in tests
    "__build_class__": __build_class__,  # Required for class definitions
    "property": property,  # Required for @property decorator
    "classmethod": classmethod,  # Required for @classmethod decorator
    "staticmethod": staticmethod,  # Required for @staticmethod decorator
    "super": super  # Required for super() calls in inheritance
}

def validate_source(code: str):
    """
    Validate user code using AST parsing.
    Raises ValueError if code contains disallowed constructs.
    Allows specific safe imports defined in ALLOWED_IMPORTS.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise ValueError(f"SyntaxError: {e}")

    for node in ast.walk(tree):
        # Check for disallowed nodes (excluding Import/ImportFrom which we handle separately)
        if isinstance(node, DISALLOWED_NODES):
            raise ValueError(f"Use of disallowed language feature in this exercise: {node.__class__.__name__}")

        # Check imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name
                if module not in ALLOWED_IMPORTS:
                    raise ValueError(f"Import of '{module}' is not allowed. Only {list(ALLOWED_IMPORTS.keys())} are permitted.")

        if isinstance(node, ast.ImportFrom):
            module = node.module
            if module not in ALLOWED_IMPORTS:
                raise ValueError(f"Import from '{module}' is not allowed. Only {list(ALLOWED_IMPORTS.keys())} are permitted.")

            # Check specific imports if restrictions exist
            allowed_names = ALLOWED_IMPORTS[module]
            if allowed_names is not None:  # None means all imports allowed
                for alias in node.names:
                    if alias.name not in allowed_names:
                        raise ValueError(f"Import of '{alias.name}' from '{module}' is not allowed. Only {allowed_names} are permitted.")

    return tree

def extract_expected_results(tests_code: str):
    """
    Extract expected test results from test code.
    Looks for patterns like:
    - if result != [4, 16]:
    - expected = [...]; if result != expected:

    Args:
        tests_code: Test harness code

    Returns:
        dict mapping function names to lists of expected results
    """
    import re
    expected = {}

    # Extract function name from pattern: if 'funcname' not in ns:
    func_pattern = r"if\s+'(\w+)'\s+not\s+in\s+ns"
    func_matches = re.findall(func_pattern, tests_code)
    func_name = func_matches[0] if func_matches else 'unknown'

    # First, try to find variable assignments like: expected=['1','2','Fizz',...]
    var_pattern = r'expected\s*=\s*(\[.*?\])'
    var_matches = re.findall(var_pattern, tests_code)

    for match in var_matches:
        try:
            # Safely evaluate the list literal
            expected_value = eval(match)
            if isinstance(expected_value, list):
                if func_name not in expected:
                    expected[func_name] = []
                expected[func_name].append(expected_value)
        except:
            pass

    # Also look for direct patterns like: if result != [4, 16]:
    pattern = r'if\s+result\d*\s*!=\s*(\[.*?\])'
    matches = re.findall(pattern, tests_code)

    for match in matches:
        try:
            # Safely evaluate the list literal
            expected_value = eval(match)
            if isinstance(expected_value, list):
                if func_name not in expected:
                    expected[func_name] = []
                expected[func_name].append(expected_value)
        except:
            pass

    return expected


def run_user_and_tests(user_code: str, tests_code: str):
    """
    Execute user code and test harness in sandboxed environment.

    Args:
        user_code: User's submitted code
        tests_code: Test harness that defines grade(user_ns) function

    Returns:
        dict with score, max_score, feedback, and execution_results
    """
    import inspect
    import builtins
    import functools
    import time

    # 1) validate user code AST
    validate_source(user_code)

    # 2) Create a restricted __import__ that only allows whitelisted modules
    def restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name in ALLOWED_IMPORTS or (fromlist and any(f in ALLOWED_IMPORTS for f in fromlist)):
            return builtins.__import__(name, globals, locals, fromlist, level)
        raise ImportError(f"Import of '{name}' is not allowed")

    # 3) prepare sandboxes with allowed modules
    user_builtins = SAFE_BUILTINS.copy()
    user_builtins["__import__"] = restricted_import  # Restricted import for user code

    user_ns = {
        "__builtins__": user_builtins,
        "__source__": user_code,  # Provide source code for pattern detection
        "__name__": "__main__"  # Required for class definitions
    }

    # Test namespace needs more builtins for inspect module to work
    # Create a copy of safe builtins and add necessary items for inspect
    test_builtins = SAFE_BUILTINS.copy()
    test_builtins["__import__"] = builtins.__import__  # Needed by inspect
    test_builtins["__name__"] = "__main__"
    test_builtins["__file__"] = "<tests>"

    test_ns = {
        "__builtins__": test_builtins,
        "inspect": inspect  # Allow tests to use inspect module
    }

    # 3) exec user code
    exec(compile(user_code, "<user>", "exec"), user_ns, user_ns)

    # 4) exec tests (must define grade(user_ns) -> dict(score:int, feedback:str))
    exec(compile(tests_code, "<tests>", "exec"), test_ns, test_ns)

    if "grade" not in test_ns or not callable(test_ns["grade"]):
        raise RuntimeError("Test script must define grade(user_ns) -> dict.")

    result = test_ns["grade"](user_ns)

    # normalize
    score = int(result.get("score", 0))
    feedback = str(result.get("feedback", ""))
    max_score = int(result.get("max_score", 100))

    # Extract expected results from test code only if score is not perfect
    # (to avoid showing expected results when code is correct)
    expected_results = {}
    if score < max_score:
        expected_results = extract_expected_results(tests_code)

    # Capture execution results for visualizations
    execution_results = capture_execution_results(user_ns, user_code, expected_results)

    return {
        "score": score,
        "max_score": max_score,
        "feedback": feedback,
        "execution_results": execution_results
    }


def _serialize_arguments(args_tuple):
    """
    Serialize function arguments for display.

    Args:
        args_tuple: Tuple of arguments passed to function

    Returns:
        List of serialized arguments (as strings or JSON objects)
    """
    serialized = []
    for arg in args_tuple:
        if isinstance(arg, (list, tuple)):
            serialized.append(list(arg))
        elif isinstance(arg, dict):
            serialized.append(arg)
        elif isinstance(arg, str):
            serialized.append(arg)
        elif isinstance(arg, (int, float, bool)):
            serialized.append(arg)
        elif arg is None:
            serialized.append(None)
        else:
            # For other types, convert to string
            serialized.append(str(arg))
    return serialized


def capture_execution_results(user_ns, user_code="", expected_results=None):
    """
    Capture execution results from user namespace for visualization.

    Args:
        user_ns: User namespace after code execution
        user_code: The user's submitted code (for visualization)
        expected_results: dict mapping function names to expected results (optional)

    Returns:
        dict with captured execution data (functions, classes, variables, user_code)
    """
    if expected_results is None:
        expected_results = {}

    results = {
        "functions": {},
        "classes": {},
        "variables": {},
        "user_code": user_code
    }

    # Capture user-defined functions
    for name, obj in user_ns.items():
        if name.startswith("__"):
            continue

        if callable(obj) and not isinstance(obj, type):
            # It's a function
            func_info = {
                "name": name,
                "type": "function"
            }

            # Try to capture return value by calling with various test inputs
            test_inputs = [
                (),  # No arguments
                ([],),  # Empty list
                ([1, 2, 3, 4, 5],),  # List with numbers
                ("test",),  # String
                (5,),  # Single number
                (0,),  # Zero
            ]

            for test_input in test_inputs:
                try:
                    return_value = obj(*test_input)
                    # Serialize the return value
                    if isinstance(return_value, (list, tuple)):
                        func_info["return_value"] = list(return_value)
                        func_info["return_type"] = "list" if isinstance(return_value, list) else "tuple"
                    elif isinstance(return_value, dict):
                        func_info["return_value"] = return_value
                        func_info["return_type"] = "dict"
                    else:
                        func_info["return_value"] = str(return_value) if return_value is not None else None
                        func_info["return_type"] = type(return_value).__name__

                    # Serialize the arguments that were passed
                    func_info["arguments"] = _serialize_arguments(test_input)

                    # If we got a meaningful result (non-empty for lists/tuples), break
                    # Otherwise, try the next test input
                    if isinstance(return_value, (list, tuple)):
                        if len(return_value) > 0:
                            # Got meaningful data, stop trying
                            break
                        # Empty result, try next input
                    else:
                        # Non-list result, accept it
                        break
                except (TypeError, ValueError, AttributeError):
                    # This test input didn't work, try the next one
                    continue
                except Exception:
                    # Any other error, skip to next test input
                    continue

            # Add expected results if available for this function
            if name in expected_results:
                func_info["expected_results"] = expected_results[name]

            results["functions"][name] = func_info
        elif isinstance(obj, type):
            # It's a class
            class_info = {
                "name": name,
                "type": "class",
                "methods": []
            }

            # Capture class methods
            for attr_name in dir(obj):
                if not attr_name.startswith("_"):
                    attr = getattr(obj, attr_name)
                    if callable(attr):
                        class_info["methods"].append(attr_name)

            results["classes"][name] = class_info
        elif not callable(obj):
            # It's a variable - capture type and string representation
            try:
                results["variables"][name] = {
                    "name": name,
                    "type": type(obj).__name__,
                    "value": str(obj) if len(str(obj)) < 100 else str(obj)[:97] + "..."
                }
            except:
                results["variables"][name] = {
                    "name": name,
                    "type": type(obj).__name__,
                    "value": "<unable to serialize>"
                }

    return results

@app.post("/api/workshops/<workshop_id>/run-tests")
def run_tests(workshop_id):
    """
    Run tests for a workshop with user code.

    JSON body:
    {
      "code": "...",
      "mockSetId": "valid"  // Optional, defaults to 'valid'
    }

    Returns:
    {
      "ok": true,
      "total_tests": 5,
      "passed_tests": 4,
      "failed_tests": 1,
      "execution_time": 0.015,
      "mock_set": "valid",
      "results": [
        {
          "id": 1,
          "name": "test_add_positive_numbers",
          "status": "pass",
          "assertion": "assertEqual(add(2, 3), 5)",
          "expected": 5,
          "actual": 5,
          "error": null,
          "execution_time": 0.001,
          "mock_set": "valid",
          "message": "✓ test_add_positive_numbers passed"
        },
        ...
      ]
    }
    """
    data = request.get_json(force=True)
    code = data.get("code")
    mock_set_id = data.get("mockSetId", "valid")

    if not code:
        return jsonify({"ok": False, "error": "Missing code"}), 400

    try:
        # Initialize services
        test_runner = TestRunner()
        test_formatter = TestFormatter()

        # For now, use the existing grade endpoint logic
        # In a full implementation, this would load workshop-specific tests
        # and execute them with the specified mock data set

        # Placeholder: return success response
        result = {
            "ok": True,
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "execution_time": 0,
            "mock_set": mock_set_id,
            "results": []
        }

        return jsonify(result)

    except Exception as e:
        trace_lines = traceback.format_exc().splitlines()
        return jsonify({
            "ok": False,
            "error": str(e),
            "trace": trace_lines[-3:] if len(trace_lines) >= 3 else trace_lines
        }), 400


@app.post("/api/grade")
def grade_submission():
    """
    Grade a code submission.

    JSON body:
    {
      "moduleId": "python_basics",
      "workshopId": "basics_01",
      "approachId": "comprehension",  // Optional, for workshops with multiple approaches
      "code": "..."
    }

    Returns:
    {
      "ok": true,
      "score": 100,
      "max_score": 100,
      "feedback": "Great!",
      "elapsed_ms": 5,
      "execution_results": {...},
      "visualizations": [...]
    }
    """
    data = request.get_json(force=True)
    mod_id = data.get("moduleId")
    ws_id = data.get("workshopId")
    approach_id = data.get("approachId")  # Optional
    code = data.get("code")

    if not mod_id or not ws_id or not code:
        return jsonify({"ok": False, "error": "Missing required fields"}), 400

    try:
        with open(f"modules/{mod_id}.json", "r", encoding="utf-8") as f:
            module = json.load(f)

        ws = next((w for w in module["workshops"] if w["id"] == ws_id), None)
        if not ws:
            return jsonify({"ok": False, "error": "Workshop not found"}), 404

        # Handle both old format (single approach) and new format (multiple approaches)
        if "approaches" in ws:
            # New format: multiple approaches
            if not approach_id:
                return jsonify({"ok": False, "error": "approachId required for multi-approach workshops"}), 400

            approach = next((a for a in ws["approaches"] if a["id"] == approach_id), None)
            if not approach:
                return jsonify({"ok": False, "error": "Approach not found"}), 404

            tests_code = approach["tests"]
        else:
            # Old format: single approach (backward compatibility)
            tests_code = ws["tests"]

        t0 = time.time()
        result = run_user_and_tests(code, tests_code)
        result["elapsed_ms"] = int((time.time() - t0) * 1000)

        # Add visualization configurations if present
        visualizations = ws.get("visualizations", [])
        if visualizations:
            result["visualizations"] = visualizations

        return jsonify({"ok": True, **result})

    except FileNotFoundError:
        return jsonify({"ok": False, "error": "Module not found"}), 404
    except Exception as e:
        trace_lines = traceback.format_exc().splitlines()
        return jsonify({
            "ok": False,
            "error": str(e),
            "trace": trace_lines[-3:] if len(trace_lines) >= 3 else trace_lines
        }), 400

# ------- TDD Workflow API -------
workflow_storage = WorkflowStorage()
step_validator = StepValidator()
code_metrics = CodeMetrics()

@app.post("/api/workshops/<workshop_id>/workflow/start")
def start_workflow(workshop_id):
    """
    Initialize a new TDD workflow for a workshop.

    Returns:
        {
            "workflow_id": str,
            "current_step": int,
            "steps_status": List[Dict]
        }
    """
    try:
        # Create new workflow
        workflow = TDDWorkflowState(workshop_id)
        workflow_id = f"{workshop_id}_{int(time.time() * 1000)}"

        # Save workflow
        workflow_storage.save_workflow(workflow_id, workflow)

        return jsonify({
            "ok": True,
            "workflow_id": workflow_id,
            "current_step": workflow.get_current_step(),
            "steps_status": workflow.get_all_steps_status()
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.get("/api/workshops/<workshop_id>/workflow/<workflow_id>")
def get_workflow(workshop_id, workflow_id):
    """
    Get current workflow state.

    Returns:
        {
            "current_step": int,
            "steps_status": List[Dict],
            "code_per_step": Dict
        }
    """
    try:
        workflow = workflow_storage.load_workflow(workflow_id)
        if not workflow:
            return jsonify({"ok": False, "error": "Workflow not found"}), 404

        code_per_step = {
            i: workflow.get_step_code(i)
            for i in range(1, 7)
        }

        return jsonify({
            "ok": True,
            "current_step": workflow.get_current_step(),
            "steps_status": workflow.get_all_steps_status(),
            "code_per_step": code_per_step
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.post("/api/workshops/<workshop_id>/workflow/<workflow_id>/validate-step")
def validate_step(workshop_id, workflow_id):
    """
    Validate current step.

    Body:
        {
            "step": int,
            "code": str,
            "test_code": str (optional, for step 3 and 5)
        }

    Returns:
        {
            "valid": bool,
            "errors": List[str],
            "warnings": List[str],
            "can_advance": bool,
            "validation_result": Dict
        }
    """
    try:
        data = request.get_json()
        step = data.get("step")
        code = data.get("code", "")
        test_code = data.get("test_code", "")

        workflow = workflow_storage.load_workflow(workflow_id)
        if not workflow:
            return jsonify({"ok": False, "error": "Workflow not found"}), 404

        # Store code
        workflow.set_step_code(step, code)

        # Validate based on step
        if step == 1:
            validation_result = step_validator.validate_step_1(code, workshop_id)
        elif step == 3:
            validation_result = step_validator.validate_step_3(code, test_code)
        elif step == 5:
            previous_code = workflow.get_step_code(3)
            validation_result = step_validator.validate_step_5(code, test_code, previous_code)
        else:
            return jsonify({"ok": False, "error": "Invalid step"}), 400

        # Mark step complete if valid
        if validation_result.get("valid"):
            workflow.mark_step_complete(step, validation_result)

        # Save workflow
        workflow_storage.save_workflow(workflow_id, workflow)

        return jsonify({
            "ok": True,
            "valid": validation_result.get("valid", False),
            "errors": validation_result.get("errors", []),
            "warnings": validation_result.get("warnings", []),
            "can_advance": workflow.can_advance_to_next_step(),
            "validation_result": validation_result
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.post("/api/workshops/<workshop_id>/workflow/<workflow_id>/advance")
def advance_workflow(workshop_id, workflow_id):
    """
    Advance to next step.

    Returns:
        {
            "current_step": int,
            "step_status": Dict
        }
    """
    try:
        workflow = workflow_storage.load_workflow(workflow_id)
        if not workflow:
            return jsonify({"ok": False, "error": "Workflow not found"}), 404

        if not workflow.advance_to_next_step():
            return jsonify({
                "ok": False,
                "error": "Cannot advance. Current step not completed."
            }), 400

        workflow_storage.save_workflow(workflow_id, workflow)

        return jsonify({
            "ok": True,
            "current_step": workflow.get_current_step(),
            "step_status": workflow.get_step_status(workflow.get_current_step())
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.post("/api/workshops/<workshop_id>/workflow/<workflow_id>/go-back")
def go_back_workflow(workshop_id, workflow_id):
    """
    Go back to a previous step.

    Body:
        {
            "target_step": int
        }

    Returns:
        {
            "current_step": int,
            "step_status": Dict
        }
    """
    try:
        data = request.get_json()
        target_step = data.get("target_step")

        workflow = workflow_storage.load_workflow(workflow_id)
        if not workflow:
            return jsonify({"ok": False, "error": "Workflow not found"}), 404

        if not workflow.go_back_to_step(target_step):
            return jsonify({
                "ok": False,
                "error": f"Cannot go back to step {target_step}"
            }), 400

        workflow_storage.save_workflow(workflow_id, workflow)

        return jsonify({
            "ok": True,
            "current_step": workflow.get_current_step(),
            "step_status": workflow.get_step_status(workflow.get_current_step())
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.get("/api/workshops/<workshop_id>/workflow/<workflow_id>/metrics")
def get_workflow_metrics(workshop_id, workflow_id):
    """
    Get code metrics for current step.

    Returns:
        {
            "complexity": int,
            "coverage": float,
            "duplication": float,
            "has_type_hints": bool,
            "has_docstring": bool,
            "lines_of_code": int
        }
    """
    try:
        workflow = workflow_storage.load_workflow(workflow_id)
        if not workflow:
            return jsonify({"ok": False, "error": "Workflow not found"}), 404

        current_step = workflow.get_current_step()
        code = workflow.get_step_code(current_step)

        metrics = code_metrics.get_metrics_summary(code)

        return jsonify({
            "ok": True,
            **metrics
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

# ------- Achievement & Progress API -------
@app.get("/api/users/<user_id>/achievements")
def get_user_achievements(user_id):
    """
    Get all achievements for a user.

    Returns:
        {
            "ok": bool,
            "achievements": List[Achievement],
            "total_points": int
        }
    """
    try:
        achievements = achievement_tracker.get_user_achievements(user_id)
        total_points = achievement_tracker.get_total_points(user_id)

        return jsonify({
            "ok": True,
            "achievements": achievements,
            "total_points": total_points
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.get("/api/users/<user_id>/badges")
def get_user_badges(user_id):
    """
    Get all badges for a user.

    Returns:
        {
            "ok": bool,
            "badges": List[Badge],
            "showcase": Dict
        }
    """
    try:
        achievements = achievement_tracker.get_user_achievements(user_id)
        badges = [badge_display.create_badge_from_achievement(a).to_dict() for a in achievements]
        showcase = badge_display.get_badge_showcase(badges)

        return jsonify({
            "ok": True,
            "badges": badges,
            "showcase": showcase
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.get("/api/users/<user_id>/stats")
def get_user_stats(user_id):
    """
    Get user statistics.

    Returns:
        {
            "ok": bool,
            "stats": UserStats,
            "rank": int
        }
    """
    try:
        stats = stats_calculator.calculate_user_stats(user_id)
        rank = stats_calculator.get_user_rank(user_id)

        return jsonify({
            "ok": True,
            "stats": stats.to_dict(),
            "rank": rank
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.get("/api/users/<user_id>/workflows")
def list_user_workflows(user_id):
    """
    List user's workflow progress.

    Returns:
        {
            "ok": bool,
            "workflows": List[WorkflowProgress]
        }
    """
    try:
        workflow_ids = workflow_storage.list_user_workflows(user_id)
        workflows = []

        for workflow_id in workflow_ids:
            progress = workflow_storage.load_progress(user_id, workflow_id)
            if progress:
                workflows.append(progress.to_dict())

        return jsonify({
            "ok": True,
            "workflows": workflows
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.get("/api/leaderboard")
def get_leaderboard():
    """
    Get global leaderboard.

    Query params:
        limit: int (default 10)
        offset: int (default 0)

    Returns:
        {
            "ok": bool,
            "leaderboard": List[Dict],
            "user_rank": int
        }
    """
    try:
        limit = request.args.get("limit", 10, type=int)
        offset = request.args.get("offset", 0, type=int)

        leaderboard = stats_calculator.get_leaderboard(limit, offset)

        return jsonify({
            "ok": True,
            "leaderboard": leaderboard
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@app.post("/api/workflows/<workflow_id>/complete")
def complete_workflow(workflow_id):
    """
    Mark workflow as complete and check for achievements.

    Body:
        {
            "user_id": str
        }

    Returns:
        {
            "ok": bool,
            "achievements_unlocked": List[Achievement],
            "stats": UserStats
        }
    """
    try:
        data = request.get_json()
        user_id = data.get("user_id")

        if not user_id:
            return jsonify({"ok": False, "error": "user_id required"}), 400

        # Load progress
        progress = workflow_storage.load_progress(user_id, workflow_id)
        if not progress:
            return jsonify({"ok": False, "error": "Workflow not found"}), 404

        # Mark as complete
        progress.mark_workflow_complete()
        workflow_storage.save_progress(progress)

        # Check for achievements
        achievements_unlocked = []

        # TDD Novice - Complete 1 full TDD workflow
        if progress.is_complete():
            if achievement_tracker.unlock_achievement(user_id, "tdd_novice"):
                achievements_unlocked.append(achievement_tracker.ACHIEVEMENTS["tdd_novice"].to_dict())

        # Get updated stats
        stats = stats_calculator.calculate_user_stats(user_id)

        return jsonify({
            "ok": True,
            "achievements_unlocked": achievements_unlocked,
            "stats": stats.to_dict()
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

# ------- Frontend -------
@app.get("/")
def home():
    """Serve the main application page."""
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

