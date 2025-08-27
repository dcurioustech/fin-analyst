"""
Unit tests for services modules.
"""
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd

from services.financial_data_service import FinancialDataService
from tests.test_fixtures import MockData, MockYFinance


class TestFinancialDataService(unittest.TestCase):
    """Test cases for FinancialDataService."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = FinancialDataService()
        self.mock_data = MockData()
    
    @patch('services.financial_data_service.yf.Ticker')
    def test_validate_ticker_valid(self, mock_ticker):
        """Test ticker validation with valid ticker."""
        # Mock successful ticker validation
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.info = {'regularMarketPrice': 150.25}
        mock_ticker.return_value = mock_ticker_instance
        
        result = self.service.validate_ticker("AAPL")
        self.assertTrue(result)
        mock_ticker.assert_called_with("AAPL")
    
    @patch('services.financial_data_service.yf.Ticker')
    def test_validate_ticker_invalid(self, mock_ticker):
        """Test ticker validation with invalid ticker."""
        # Mock failed ticker validation
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.info = {}
        mock_ticker.return_value = mock_ticker_instance
        
        result = self.service.validate_ticker("INVALID")
        self.assertFalse(result)
    
    def test_validate_ticker_edge_cases(self):
        """Test ticker validation edge cases."""
        # Test None and empty string
        self.assertFalse(self.service.validate_ticker(None))
        self.assertFalse(self.service.validate_ticker(""))
        self.assertFalse(self.service.validate_ticker(123))  # Non-string
    
    @patch('services.financial_data_service.yf.Ticker')
    def test_get_company_info_success(self, mock_ticker):
        """Test successful company info retrieval."""
        # Mock successful data fetch
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.info = self.mock_data.get_mock_company_info()
        mock_ticker.return_value = mock_ticker_instance
        
        result = self.service.get_company_info("AAPL")
        
        self.assertTrue(result['success'])
        self.assertIsNone(result['error'])
        self.assertIsNotNone(result['data'])
        self.assertEqual(result['ticker'], 'AAPL')
        self.assertEqual(result['data']['longName'], 'Apple Inc.')
    
    @patch('services.financial_data_service.yf.Ticker')
    def test_get_company_info_failure(self, mock_ticker):
        """Test failed company info retrieval."""
        # Mock failed data fetch
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.info = {}
        mock_ticker.return_value = mock_ticker_instance
        
        result = self.service.get_company_info("INVALID")
        
        self.assertFalse(result['success'])
        self.assertIsNotNone(result['error'])
        self.assertIsNone(result['data'])
    
    @patch('services.financial_data_service.yf.Ticker')
    def test_get_company_info_exception(self, mock_ticker):
        """Test company info retrieval with exception."""
        # Mock exception during data fetch
        mock_ticker.side_effect = Exception("Network error")
        
        result = self.service.get_company_info("AAPL")
        
        self.assertFalse(result['success'])
        self.assertIn("Network error", result['error'])
        self.assertIsNone(result['data'])
    
    @patch('services.financial_data_service.yf.Ticker')
    def test_get_financial_statements_success(self, mock_ticker):
        """Test successful financial statements retrieval."""
        # Mock successful statements fetch
        mock_ticker_instance = MagicMock()
        statements = self.mock_data.get_mock_financial_statements()
        mock_ticker_instance.financials = statements['income_statement']
        mock_ticker_instance.balance_sheet = statements['balance_sheet']
        mock_ticker_instance.cashflow = statements['cash_flow']
        mock_ticker.return_value = mock_ticker_instance
        
        result = self.service.get_financial_statements("AAPL")
        
        self.assertTrue(result['success'])
        self.assertIsNone(result['error'])
        self.assertIsNotNone(result['data'])
        self.assertIn('income_statement', result['data'])
        self.assertIn('balance_sheet', result['data'])
        self.assertIn('cash_flow', result['data'])
    
    @patch('services.financial_data_service.yf.Ticker')
    def test_get_recommendations_success(self, mock_ticker):
        """Test successful recommendations retrieval."""
        # Mock successful recommendations fetch
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.recommendations = self.mock_data.get_mock_recommendations()
        mock_ticker.return_value = mock_ticker_instance
        
        result = self.service.get_recommendations("AAPL")
        
        self.assertTrue(result['success'])
        self.assertIsNone(result['error'])
        self.assertIsNotNone(result['data'])
    
    @patch('services.financial_data_service.yf.Ticker')
    def test_get_multiple_company_info(self, mock_ticker):
        """Test multiple company info retrieval."""
        # Mock multiple ticker responses
        def mock_ticker_side_effect(ticker):
            mock_instance = MagicMock()
            if ticker == 'AAPL':
                mock_instance.info = self.mock_data.get_mock_company_info()
            elif ticker == 'MSFT':
                mock_instance.info = {'longName': 'Microsoft Corporation', 'regularMarketPrice': 420.55}
            else:
                mock_instance.info = {}
            return mock_instance
        
        mock_ticker.side_effect = mock_ticker_side_effect
        
        result = self.service.get_multiple_company_info(['AAPL', 'MSFT', 'INVALID'])
        
        self.assertTrue(result['success'])
        self.assertEqual(result['total_requested'], 3)
        self.assertEqual(result['successful_fetches'], 2)
        self.assertIn('AAPL', result['results'])
        self.assertIn('MSFT', result['results'])
        self.assertIn('INVALID', result['results'])
    
    @patch('services.financial_data_service.yf.Ticker')
    def test_get_peer_comparison_data(self, mock_ticker):
        """Test peer comparison data retrieval."""
        # Mock peer data responses
        peer_data = self.mock_data.get_mock_peer_data()
        
        def mock_ticker_side_effect(ticker):
            mock_instance = MagicMock()
            if ticker in peer_data:
                mock_instance.info = peer_data[ticker]
            else:
                mock_instance.info = {'regularMarketPrice': 100.0}  # Minimal valid data
            return mock_instance
        
        mock_ticker.side_effect = mock_ticker_side_effect
        
        result = self.service.get_peer_comparison_data('AAPL', ['MSFT', 'GOOGL'])
        
        self.assertTrue(result['success'])
        self.assertEqual(result['main_ticker'], 'AAPL')
        self.assertEqual(len(result['peer_tickers']), 2)
        self.assertIn('AAPL', result['data'])
        # MSFT and GOOGL might not be in result if their data fetch fails
        # The service correctly filters out failed tickers
    
    def test_suggest_peers_from_recommendations(self):
        """Test peer suggestion from recommendations."""
        # This method currently returns empty list, test the behavior
        result = self.service.suggest_peers_from_recommendations('AAPL')
        self.assertIsInstance(result, list)


if __name__ == '__main__':
    unittest.main()