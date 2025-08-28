#!/usr/bin/env python3
"""
Simple test suite for the Financial Analysis Bot.
Tests core functionality without complex mocking.
"""
import os
import sys
import unittest

# Add the parent directory to the path so we can import project modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCoreModules(unittest.TestCase):
    """Test core module functionality."""

    def test_imports(self):
        """Test that all modules can be imported."""
        try:
            # Test main application
            # Test analyzers
            from analysis.company_analyzer import CompanyAnalyzer
            from analysis.comparison_analyzer import ComparisonAnalyzer
            from analysis.metrics_analyzer import MetricsAnalyzer
            from analysis.statement_analyzer import StatementAnalyzer
            from config.settings import configure_pandas
            from main import FinancialAnalysisApp
            # Test services
            from services.financial_data_service import FinancialDataService
            from ui.display_formatter import DisplayFormatter
            # Test UI components
            from ui.menu_handler import MenuHandler
            from utils.error_handling import validate_ticker_symbol
            # Test utilities
            from utils.formatters import (format_currency, format_large_number,
                                          format_percentage)
            from utils.input_validation import InputValidator
            from utils.visualizations import plot_text_bar

            self.assertTrue(True, "All imports successful")

        except ImportError as e:
            self.fail(f"Import failed: {e}")

    def test_application_initialization(self):
        """Test application initialization."""
        try:
            # Patch logging to avoid output
            import unittest.mock

            with unittest.mock.patch("utils.error_handling.setup_logging"):
                from main import FinancialAnalysisApp

                app = FinancialAnalysisApp()

                # Check that all components are initialized
                self.assertIsNotNone(app.data_service)
                self.assertIsNotNone(app.company_analyzer)
                self.assertIsNotNone(app.metrics_analyzer)
                self.assertIsNotNone(app.statement_analyzer)
                self.assertIsNotNone(app.comparison_analyzer)
                self.assertIsNotNone(app.menu_handler)
                self.assertIsNotNone(app.display_formatter)

        except Exception as e:
            self.fail(f"Application initialization failed: {e}")

    def test_utility_functions(self):
        """Test utility functions."""
        from utils.error_handling import validate_ticker_symbol
        from utils.formatters import (format_currency, format_large_number,
                                      format_percentage)

        # Test formatters
        self.assertEqual(format_large_number(1500000000), "1.50 B")
        self.assertEqual(format_percentage(0.15), "15.00%")
        self.assertEqual(format_currency(1234.56), "$1,234.56")

        # Test validation
        self.assertTrue(validate_ticker_symbol("AAPL"))
        self.assertFalse(validate_ticker_symbol("123"))
        self.assertFalse(validate_ticker_symbol(""))

    def test_data_service_basic(self):
        """Test basic data service functionality."""
        from services.financial_data_service import FinancialDataService

        service = FinancialDataService()

        # Test basic validation (doesn't require network)
        self.assertFalse(service.validate_ticker(""))
        self.assertFalse(service.validate_ticker(None))
        self.assertFalse(service.validate_ticker(123))

    def test_analyzers_basic(self):
        """Test basic analyzer functionality."""
        from analysis.company_analyzer import CompanyAnalyzer
        from analysis.comparison_analyzer import ComparisonAnalyzer
        from analysis.metrics_analyzer import MetricsAnalyzer
        from analysis.statement_analyzer import StatementAnalyzer

        # Test initialization
        company_analyzer = CompanyAnalyzer()
        metrics_analyzer = MetricsAnalyzer()
        statement_analyzer = StatementAnalyzer()
        comparison_analyzer = ComparisonAnalyzer()

        self.assertIsNotNone(company_analyzer)
        self.assertIsNotNone(metrics_analyzer)
        self.assertIsNotNone(statement_analyzer)
        self.assertIsNotNone(comparison_analyzer)

        # Test with mock data
        mock_data = {
            "longName": "Test Company",
            "sector": "Technology",
            "currentPrice": 100.0,
            "marketCap": 1000000000,
        }

        # Test company analyzer
        result = company_analyzer.analyze_company_profile(mock_data)
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)

        # Test metrics analyzer
        result = metrics_analyzer.get_comprehensive_metrics(mock_data)
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)

    def test_ui_components_basic(self):
        """Test basic UI component functionality."""
        from ui.display_formatter import DisplayFormatter
        from ui.menu_handler import MenuHandler

        menu_handler = MenuHandler()
        display_formatter = DisplayFormatter()

        self.assertIsNotNone(menu_handler)
        self.assertIsNotNone(display_formatter)

        # Test menu handler
        choice_handler = menu_handler.get_analysis_choice_handler()
        self.assertIsInstance(choice_handler, dict)
        self.assertEqual(len(choice_handler), 9)

        # Test display formatter
        error = Exception("Test error")
        formatted = display_formatter.format_error_message(error)
        self.assertIsInstance(formatted, str)
        self.assertIn("Test error", formatted)


class TestIntegrationBasic(unittest.TestCase):
    """Test basic integration functionality."""

    def test_end_to_end_mock_workflow(self):
        """Test end-to-end workflow with mock data."""
        import unittest.mock

        # Mock the logging setup
        with unittest.mock.patch("utils.error_handling.setup_logging"):
            from main import FinancialAnalysisApp

            app = FinancialAnalysisApp()

            # Mock company data
            mock_company_data = {
                "longName": "Apple Inc.",
                "sector": "Technology",
                "industry": "Consumer Electronics",
                "currentPrice": 150.25,
                "marketCap": 2400000000000,
                "trailingPE": 25.5,
                "profitMargins": 0.253,
            }

            # Test company profile analysis
            with unittest.mock.patch("sys.stdout"):  # Suppress output
                try:
                    app._handle_company_profile(mock_company_data)
                    app._handle_key_metrics(mock_company_data)
                    # If we get here, the workflow worked
                    self.assertTrue(True)
                except Exception as e:
                    self.fail(f"Mock workflow failed: {e}")


def run_simple_tests():
    """Run the simple test suite."""
    print("🧪 Running Simple Financial Analysis Bot Test Suite")
    print("=" * 60)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCoreModules))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationBasic))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}")

    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}")

    success = len(result.failures) == 0 and len(result.errors) == 0

    if success:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n❌ {len(result.failures) + len(result.errors)} tests failed")

    return success


if __name__ == "__main__":
    success = run_simple_tests()
    sys.exit(0 if success else 1)
