"""
Test fixtures and mock data for consistent testing.
"""
from typing import Dict, Any
import pandas as pd


class MockData:
    """Mock data fixtures for testing."""
    
    @staticmethod
    def get_mock_company_info() -> Dict[str, Any]:
        """Returns mock company information data."""
        return {
            'longName': 'Apple Inc.',
            'shortName': 'Apple',
            'symbol': 'AAPL',
            'sector': 'Technology',
            'industry': 'Consumer Electronics',
            'country': 'United States',
            'website': 'https://www.apple.com',
            'longBusinessSummary': 'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide.',
            'fullTimeEmployees': 164000,
            'currentPrice': 150.25,
            'marketCap': 2400000000000,
            'enterpriseValue': 2450000000000,
            'trailingPE': 25.5,
            'forwardPE': 22.8,
            'priceToSalesTrailing12Months': 7.2,
            'priceToBook': 39.4,
            'profitMargins': 0.253,
            'returnOnEquity': 1.479,
            'returnOnAssets': 0.202,
            'fiftyTwoWeekLow': 124.17,
            'fiftyTwoWeekHigh': 199.62,
            'beta': 1.286,
            'dividendYield': 0.0044,
            'payoutRatio': 0.1534,
            'regularMarketPrice': 150.25
        }
    
    @staticmethod
    def get_mock_financial_statements() -> Dict[str, Any]:
        """Returns mock financial statements data."""
        # Create mock dataframes for financial statements
        dates = pd.to_datetime(['2023-12-31', '2022-12-31', '2021-12-31', '2020-12-31'])
        
        income_statement = pd.DataFrame({
            '2023-12-31': [383285000000, 214137000000, 169148000000, 95041000000, 74100000000],
            '2022-12-31': [394328000000, 223546000000, 170782000000, 99803000000, 73351000000],
            '2021-12-31': [365817000000, 212981000000, 152836000000, 94680000000, 57411000000],
            '2020-12-31': [274515000000, 169559000000, 104956000000, 66288000000, 38016000000]
        }, index=['Total Revenue', 'Cost Of Revenue', 'Gross Profit', 'Operating Income', 'Net Income'])
        
        balance_sheet = pd.DataFrame({
            '2023-12-31': [352755000000, 143566000000, 209189000000, 123930000000, 85274000000],
            '2022-12-31': [352583000000, 135405000000, 217178000000, 109106000000, 108150000000],
            '2021-12-31': [381191000000, 125481000000, 255710000000, 174406000000, 81293000000],
            '2020-12-31': [323888000000, 105392000000, 218499000000, 153982000000, 64849000000]
        }, index=['Total Assets', 'Total Liabilities Net Minority Interest', 'Total Equity Gross Minority Interest', 'Stockholders Equity', 'Total Debt'])
        
        cash_flow = pd.DataFrame({
            '2023-12-31': [110543000000, -10959000000, -108488000000, -8945000000],
            '2022-12-31': [122151000000, -22354000000, -89402000000, 10448000000],
            '2021-12-31': [104038000000, -14545000000, -85971000000, 3522000000],
            '2020-12-31': [80674000000, -4289000000, -86820000000, -10435000000]
        }, index=['Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow', 'Free Cash Flow'])
        
        return {
            'income_statement': income_statement,
            'balance_sheet': balance_sheet,
            'cash_flow': cash_flow
        }
    
    @staticmethod
    def get_mock_recommendations() -> pd.DataFrame:
        """Returns mock analyst recommendations data."""
        return pd.DataFrame({
            'period': ['0m', '-1m', '-2m', '-3m'],
            'strongBuy': [12, 11, 10, 9],
            'buy': [18, 19, 20, 21],
            'hold': [8, 9, 10, 11],
            'sell': [1, 1, 0, 0],
            'strongSell': [0, 0, 0, 0]
        })
    
    @staticmethod
    def get_mock_peer_data() -> Dict[str, Dict[str, Any]]:
        """Returns mock peer comparison data."""
        return {
            'AAPL': MockData.get_mock_company_info(),
            'MSFT': {
                'longName': 'Microsoft Corporation',
                'symbol': 'MSFT',
                'sector': 'Technology',
                'industry': 'Software—Infrastructure',
                'currentPrice': 420.55,
                'marketCap': 3120000000000,
                'trailingPE': 35.2,
                'priceToSalesTrailing12Months': 12.8,
                'priceToBook': 13.1,
                'profitMargins': 0.362,
                'returnOnEquity': 0.384
            },
            'GOOGL': {
                'longName': 'Alphabet Inc.',
                'symbol': 'GOOGL',
                'sector': 'Communication Services',
                'industry': 'Internet Content & Information',
                'currentPrice': 138.21,
                'marketCap': 1750000000000,
                'trailingPE': 26.1,
                'priceToSalesTrailing12Months': 5.9,
                'priceToBook': 5.8,
                'profitMargins': 0.205,
                'returnOnEquity': 0.275
            }
        }
    
    @staticmethod
    def get_mock_service_response(success: bool = True, data: Any = None, error: str = None) -> Dict[str, Any]:
        """Returns a mock service response structure."""
        return {
            'success': success,
            'data': data,
            'error': error,
            'timestamp': pd.Timestamp.now()
        }


class MockYFinance:
    """Mock yfinance module for testing."""
    
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self._mock_data = MockData()
    
    @property
    def info(self) -> Dict[str, Any]:
        """Mock info property."""
        if self.ticker == 'AAPL':
            return self._mock_data.get_mock_company_info()
        elif self.ticker == 'INVALID':
            return {}
        else:
            # Return basic mock data for other tickers
            return {
                'longName': f'{self.ticker} Corporation',
                'symbol': self.ticker,
                'regularMarketPrice': 100.0,
                'marketCap': 1000000000
            }
    
    @property
    def financials(self) -> pd.DataFrame:
        """Mock financials property."""
        return self._mock_data.get_mock_financial_statements()['income_statement']
    
    @property
    def balance_sheet(self) -> pd.DataFrame:
        """Mock balance_sheet property."""
        return self._mock_data.get_mock_financial_statements()['balance_sheet']
    
    @property
    def cashflow(self) -> pd.DataFrame:
        """Mock cashflow property."""
        return self._mock_data.get_mock_financial_statements()['cash_flow']
    
    @property
    def recommendations(self) -> pd.DataFrame:
        """Mock recommendations property."""
        return self._mock_data.get_mock_recommendations()