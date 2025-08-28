#!/usr/bin/env python3
"""
Test runner for the Financial Analysis Bot test suite.
Supports both pytest and unittest execution.
"""
import os
import subprocess
import sys
import unittest
from io import StringIO

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestResult:
    """Custom test result class to track test statistics."""

    def __init__(self):
        self.tests_run = 0
        self.failures = 0
        self.errors = 0
        self.skipped = 0
        self.success = 0

    def add_result(self, result):
        """Add a test result."""
        self.tests_run += result.testsRun
        self.failures += len(result.failures)
        self.errors += len(result.errors)
        self.skipped += len(result.skipped)
        self.success = self.tests_run - self.failures - self.errors - self.skipped


def run_test_module(module_name, verbose=False):
    """Run tests for a specific module."""
    print(f"\n{'='*60}")
    print(f"Running {module_name} tests...")
    print("=" * 60)

    # Capture output if not verbose
    if not verbose:
        old_stdout = sys.stdout
        sys.stdout = StringIO()

    try:
        # Load and run the test module
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromName(module_name)
        runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
        result = runner.run(suite)

        # Restore stdout if it was captured
        if not verbose:
            sys.stdout = old_stdout

        # Print summary
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Skipped: {len(result.skipped)}")

        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")

        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")

        return result

    except Exception as e:
        print(f"Error running {module_name}: {e}")
        return None


def run_all_tests(verbose=False):
    """Run all test modules."""
    print("🧪 Running Financial Analysis Bot Test Suite")
    print("=" * 60)

    # Test modules to run
    test_modules = [
        "tests.test_utils",
        "tests.test_services",
        "tests.test_analysis",
        "tests.test_ui",
        "tests.test_integration",
    ]

    overall_result = TestResult()
    failed_modules = []

    for module in test_modules:
        try:
            result = run_test_module(module, verbose)
            if result:
                overall_result.add_result(result)
                if result.failures or result.errors:
                    failed_modules.append(module)
            else:
                failed_modules.append(module)
        except Exception as e:
            print(f"Failed to run {module}: {e}")
            failed_modules.append(module)

    # Print overall summary
    print(f"\n{'='*60}")
    print("OVERALL TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests run: {overall_result.tests_run}")
    print(f"Successful: {overall_result.success}")
    print(f"Failures: {overall_result.failures}")
    print(f"Errors: {overall_result.errors}")
    print(f"Skipped: {overall_result.skipped}")

    if failed_modules:
        print(f"\nModules with failures: {', '.join(failed_modules)}")

    success_rate = (
        (overall_result.success / overall_result.tests_run * 100)
        if overall_result.tests_run > 0
        else 0
    )
    print(f"Success rate: {success_rate:.1f}%")

    if overall_result.failures == 0 and overall_result.errors == 0:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n❌ {overall_result.failures + overall_result.errors} tests failed")
        return False


def run_specific_tests(test_pattern, verbose=False):
    """Run tests matching a specific pattern."""
    print(f"🧪 Running tests matching pattern: {test_pattern}")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_pattern)
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(suite)

    return result.wasSuccessful()


def run_with_pytest(args_list=None):
    """Run tests using pytest."""
    print("🧪 Running tests with pytest...")

    # Build pytest command
    cmd = ["python", "-m", "pytest", "tests/"]  # Always run from tests directory

    if args_list:
        cmd.extend(args_list)

    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(os.path.dirname(__file__)))
        return result.returncode == 0
    except Exception as e:
        print(f"Error running pytest: {e}")
        return False


def main():
    """Main test runner function."""
    import argparse

    parser = argparse.ArgumentParser(description="Run Financial Analysis Bot tests")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Run tests in verbose mode"
    )
    parser.add_argument(
        "--module",
        "-m",
        type=str,
        help="Run tests for specific module (e.g., tests.test_utils)",
    )
    parser.add_argument(
        "--pattern",
        "-p",
        type=str,
        help="Run tests matching pattern (e.g., tests.test_utils.TestFormatters)",
    )
    parser.add_argument(
        "--pytest",
        action="store_true",
        help="Use pytest instead of unittest (recommended)",
    )
    parser.add_argument(
        "--coverage", action="store_true", help="Run with coverage report (pytest only)"
    )

    args = parser.parse_args()

    # Use pytest if requested or if no specific unittest options are given
    if args.pytest or (not args.module and not args.pattern):
        pytest_args = []

        if args.verbose:
            pytest_args.append("-v")

        if args.coverage:
            pytest_args.extend(
                ["--cov=.", "--cov-report=html", "--cov-report=term-missing"]
            )

        if args.module:
            # Convert module path to file path for pytest
            module_path = args.module.replace(".", "/") + ".py"
            pytest_args.append(module_path)
        elif args.pattern:
            pytest_args.extend(["-k", args.pattern])

        success = run_with_pytest(pytest_args)
    else:
        # Fall back to unittest
        if args.pattern:
            success = run_specific_tests(args.pattern, args.verbose)
        elif args.module:
            result = run_test_module(args.module, args.verbose)
            success = result and not (result.failures or result.errors)
        else:
            success = run_all_tests(args.verbose)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
