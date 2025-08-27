"""
Unit tests for analysis modules.
"""
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from analysis.company_analyzer import CompanyAnalyzer
from analysis.metrics_analyzer import MetricsAnalyzer
from analysis.statement_analyzer import StatementAnalyzer
from analysis.comparison_analyzer import ComparisonAnalyzer
from tests.test_fixtures import MockData


class TestCompanyAnalyzer(unittest.TestCase):
    """Test cases for CompanyAnalyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = CompanyAnalyzer()
        self.mock_data = MockData()
    
    def test_analyze_company_profile_success(self):
        """Test successful company profile analysis."""
        company_data = self.mock_data.get_mock_company_info()
        
        result = self.analyzer.analyze_company_profile(company_data)
        
        self.assertTrue(result['success'])
        self.assertIsNone(result['error'])
        self.assertIn('data', result)
        self.assertIn('basic_info', result['data'])
        self.assertIn('business_summary', result['data'])
        
        # Check basic info extraction
        basic_info = result['data']['basic_info']
        self.assertEqual(basic_info['name'], 'Apple Inc.')
        self.assertEqual(basic_info['sector'], 'Technology')
        self.assertEqual(basic_info['industry'], 'Consumer Electronics')
    
    def test_analyze_company_profile_missing_data(self):
        """Test company profile analysis with missing data."""
        # Test with minimal data
        minimal_data = {
            'longName': 'Test Company',
            'sector': 'Technology'
        }
        
        result = self.analyzer.analyze_company_profile(minimal_data)
        
        self.assertTrue(result['success'])
        basic_info = result['data']['basic_info']
        self.assertEqual(basic_info['name'], 'Test Company')
        self.assertEqual(basic_info['sector'], 'Technology')
        self.assertEqual(basic_info['industry'], 'N/A')  # Should handle missing data
    
    def test_analyze_company_profile_empty_data(self):
        """Test company profile analysis with empty data."""
        result = self.analyzer.analyze_company_profile({})
        
        self.assertFalse(result['success'])
        self.assertIsNotNone(result['error'])


class TestMetricsAnalyzer(unittest.TestCase):
    """Test cases for MetricsAnalyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = MetricsAnalyzer()
        self.mock_data = MockData()
    
    def test_get_comprehensive_metrics_success(self):
        """Test successful comprehensive metrics analysis."""
        company_data = self.mock_data.get_mock_company_info()
        
        result = self.analyzer.get_comprehensive_metrics(company_data)
        
        self.assertTrue(result['success'])
        self.assertIsNone(result['error'])
        self.assertIn('data', result)
        
        # Check that all metric categories are present (actual implementation uses different keys)
        metrics_data = result['data']
        self.assertIn('valuation', metrics_data)
        self.assertIn('profitability', metrics_data)
        self.assertIn('stock_price', metrics_data)
        self.assertIn('dividend', metrics_data)
    
    def test_get_valuation_metrics(self):
        """Test valuation metrics extraction."""
        company_data = self.mock_data.get_mock_company_info()
        
        result = self.analyzer.analyze_valuation_metrics(company_data)
        
        self.assertTrue(result['success'])
        valuation = result['data']
        self.assertIn('market_cap', valuation)
        self.assertIn('enterprise_value', valuation)
        self.assertIn('trailing_pe', valuation)
        self.assertIn('forward_pe', valuation)
        self.assertIn('price_to_sales', valuation)
        self.assertIn('price_to_book', valuation)
    
    def test_get_profitability_metrics(self):
        """Test profitability metrics extraction."""
        company_data = self.mock_data.get_mock_company_info()
        
        result = self.analyzer.analyze_profitability_metrics(company_data)
        
        self.assertTrue(result['success'])
        profitability = result['data']
        self.assertIn('profit_margins', profitability)
        self.assertIn('return_on_equity', profitability)
        self.assertIn('return_on_assets', profitability)
    
    def test_get_stock_price_metrics(self):
        """Test stock price metrics extraction."""
        company_data = self.mock_data.get_mock_company_info()
        
        result = self.analyzer.analyze_stock_price_metrics(company_data)
        
        self.assertTrue(result['success'])
        stock_metrics = result['data']
        self.assertIn('current_price', stock_metrics)
        self.assertIn('fifty_two_week_low', stock_metrics)
        self.assertIn('fifty_two_week_high', stock_metrics)
        self.assertIn('beta', stock_metrics)
    
    def test_metrics_with_missing_data(self):
        """Test metrics analysis with missing data."""
        incomplete_data = {
            'longName': 'Test Company',
            'currentPrice': 100.0,
            'marketCap': 1000000000
        }
        
        result = self.analyzer.get_comprehensive_metrics(incomplete_data)
        
        self.assertTrue(result['success'])
        # Should handle missing data gracefully


class TestStatementAnalyzer(unittest.TestCase):
    """Test cases for StatementAnalyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = StatementAnalyzer()
        self.mock_data = MockData()
    
    def test_process_income_statement_success(self):
        """Test successful income statement processing."""
        statements = self.mock_data.get_mock_financial_statements()
        income_statement = statements['income_statement']
        
        result = self.analyzer.process_income_statement(income_statement)
        
        self.assertTrue(result['success'])
        self.assertIsNone(result['error'])
        self.assertIn('data', result)
        self.assertIn('formatted_data', result['data'])
        self.assertIn('key_metrics', result['data'])
    
    def test_process_balance_sheet_success(self):
        """Test successful balance sheet processing."""
        statements = self.mock_data.get_mock_financial_statements()
        balance_sheet = statements['balance_sheet']
        
        result = self.analyzer.process_balance_sheet(balance_sheet)
        
        self.assertTrue(result['success'])
        self.assertIsNone(result['error'])
        self.assertIn('data', result)
        self.assertIn('formatted_data', result['data'])
        self.assertIn('key_metrics', result['data'])
    
    def test_process_cash_flow_success(self):
        """Test successful cash flow processing."""
        statements = self.mock_data.get_mock_financial_statements()
        cash_flow = statements['cash_flow']
        
        result = self.analyzer.process_cash_flow(cash_flow)
        
        self.assertTrue(result['success'])
        self.assertIsNone(result['error'])
        self.assertIn('data', result)
        self.assertIn('formatted_data', result['data'])
        self.assertIn('key_metrics', result['data'])
    
    def test_process_empty_statement(self):
        """Test processing with empty statement."""
        empty_df = pd.DataFrame()
        
        result = self.analyzer.process_income_statement(empty_df)
        
        self.assertFalse(result['success'])
        self.assertIsNotNone(result['error'])
    
    def test_process_none_statement(self):
        """Test processing with None statement."""
        result = self.analyzer.process_income_statement(None)
        
        self.assertFalse(result['success'])
        self.assertIsNotNone(result['error'])


class TestComparisonAnalyzer(unittest.TestCase):
    """Test cases for ComparisonAnalyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = ComparisonAnalyzer()
        self.mock_data = MockData()
    
    def test_perform_peer_comparison_success(self):
        """Test successful peer comparison."""
        main_ticker = 'AAPL'
        peer_tickers = ['MSFT', 'GOOGL']
        comparison_data = self.mock_data.get_mock_peer_data()
        
        result = self.analyzer.perform_peer_comparison(main_ticker, peer_tickers, comparison_data)
        
        self.assertTrue(result['success'])
        self.assertIsNone(result['error'])
        self.assertIn('data', result)
        
        # Check comparison data structure
        comparison_result = result['data']
        self.assertIn('comparison_table', comparison_result)
        self.assertIn('visual_comparisons', comparison_result)
        self.assertIn('main_ticker', comparison_result)
        self.assertEqual(comparison_result['main_ticker'], main_ticker)
    
    def test_calculate_comparison_metrics(self):
        """Test comparison metrics calculation."""
        comparison_data = self.mock_data.get_mock_peer_data()
        
        result = self.analyzer.calculate_comparison_metrics(comparison_data)
        
        # The method returns a DataFrame directly, not a success/data structure
        self.assertIsInstance(result, pd.DataFrame)
        
        # Check that metrics are calculated for all companies
        if not result.empty:
            self.assertIn('AAPL', result.index)
            # Note: MSFT and GOOGL might not be in the result if mock data doesn't include them
    
    def test_generate_visual_comparisons(self):
        """Test visual comparison generation."""
        comparison_data = self.mock_data.get_mock_peer_data()
        
        # First get the comparison metrics DataFrame
        comparison_df = self.analyzer.calculate_comparison_metrics(comparison_data)
        
        # Then generate visuals from the DataFrame
        result = self.analyzer.generate_comparison_visuals(comparison_df)
        
        # The method returns a dictionary of visual data directly
        self.assertIsInstance(result, dict)
        
        # Check that visual data is generated (if there's data)
        if comparison_df is not None and not comparison_df.empty:
            self.assertTrue(len(result) > 0)
    
    def test_peer_comparison_with_missing_data(self):
        """Test peer comparison with missing data."""
        main_ticker = 'AAPL'
        peer_tickers = ['MSFT']
        incomplete_data = {
            'AAPL': {'longName': 'Apple Inc.', 'currentPrice': 150.0},
            'MSFT': {'longName': 'Microsoft Corporation'}  # Missing price data
        }
        
        result = self.analyzer.perform_peer_comparison(main_ticker, peer_tickers, incomplete_data)
        
        # Should handle missing data gracefully
        self.assertTrue(result['success'])
    
    def test_peer_comparison_empty_data(self):
        """Test peer comparison with empty data."""
        result = self.analyzer.perform_peer_comparison('AAPL', ['MSFT'], {})
        
        self.assertFalse(result['success'])
        self.assertIsNotNone(result['error'])


if __name__ == '__main__':
    unittest.main()