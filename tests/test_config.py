"""
Test configuration and utilities.
"""

import os
import sys
import unittest
from unittest.mock import patch

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class BaseTestCase(unittest.TestCase):
    """Base test case with common setup and utilities."""

    def setUp(self):
        """Common setup for all tests."""
        # Patch logging to avoid log output during tests
        self.logging_patcher = patch("logging.getLogger")
        self.mock_logger = self.logging_patcher.start()

        # Patch pandas configuration to avoid warnings
        self.pandas_patcher = patch("config.settings.configure_pandas")
        self.pandas_patcher.start()

    def tearDown(self):
        """Common teardown for all tests."""
        self.logging_patcher.stop()
        self.pandas_patcher.stop()

    def assertContainsAll(self, container, items):
        """Assert that container contains all items."""
        for item in items:
            self.assertIn(item, container, f"'{item}' not found in container")

    def assertIsValidResponse(self, response, success=True):
        """Assert that response has valid structure."""
        self.assertIsInstance(response, dict)
        self.assertIn("success", response)
        self.assertEqual(response["success"], success)

        if success:
            self.assertIn("data", response)
            self.assertIsNone(response.get("error"))
        else:
            self.assertIn("error", response)
            self.assertIsNotNone(response["error"])


class MockTestCase(BaseTestCase):
    """Base test case with mock data utilities."""

    def setUp(self):
        """Setup with mock data."""
        super().setUp()
        from tests.test_fixtures import MockData

        self.mock_data = MockData()

    def get_mock_company_data(self):
        """Get mock company data."""
        return self.mock_data.get_mock_company_info()

    def get_mock_statements(self):
        """Get mock financial statements."""
        return self.mock_data.get_mock_financial_statements()

    def get_mock_service_response(self, success=True, data=None, error=None):
        """Get mock service response."""
        return self.mock_data.get_mock_service_response(success, data, error)


# Test discovery configuration
def load_tests(loader, tests, pattern):
    """Custom test loader for better test organization."""
    suite = unittest.TestSuite()

    # Load tests from all test modules
    test_modules = [
        "tests.test_utils",
        "tests.test_services",
        "tests.test_analysis",
        "tests.test_ui",
        "tests.test_integration",
    ]

    for module in test_modules:
        try:
            module_tests = loader.loadTestsFromName(module)
            suite.addTests(module_tests)
        except ImportError as e:
            print(f"Warning: Could not load {module}: {e}")

    return suite
