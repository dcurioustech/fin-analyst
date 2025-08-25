"""
Financial data service for accessing external financial data APIs.
"""
import yfinance as yf
import pandas as pd
import logging
from typing import Dict, Any, Optional, Union
from datetime import datetime


class FinancialDataService:
    """Service class for accessing financial data from external APIs."""
    
    def __init__(self):
        """Initialize the financial data service."""
        self.logger = logging.getLogger(__name__)
    
    def validate_ticker(self, ticker: str) -> bool:
        """
        Validates if a ticker symbol exists and has data available.
        
        Args:
            ticker: The ticker symbol to validate
            
        Returns:
            True if ticker is valid, False otherwise
        """
        if not ticker or not isinstance(ticker, str):
            return False
        
        try:
            stock = yf.Ticker(ticker.upper())
            info = stock.info
            # Check if we got valid data back
            return info and info.get('regularMarketPrice') is not None
        except Exception as e:
            self.logger.warning(f"Ticker validation failed for {ticker}: {e}")
            return False
    
    def get_company_info(self, ticker: str) -> Dict[str, Any]:
        """
        Fetches comprehensive company information for a given ticker.
        
        Args:
            ticker: The ticker symbol
            
        Returns:
            Dictionary containing company info or error information
        """
        try:
            stock = yf.Ticker(ticker.upper())
            info = stock.info
            
            if not info or info.get('regularMarketPrice') is None:
                return {
                    'success': False,
                    'error': f"No data found for ticker '{ticker}'",
                    'data': None
                }
            
            return {
                'success': True,
                'error': None,
                'data': info,
                'ticker': ticker.upper(),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching company info for {ticker}: {e}")
            return {
                'success': False,
                'error': f"Failed to fetch data for {ticker}: {str(e)}",
                'data': None
            }
    
    def get_financial_statements(self, ticker: str) -> Dict[str, Any]:
        """
        Fetches financial statements (income statement, balance sheet, cash flow) for a ticker.
        
        Args:
            ticker: The ticker symbol
            
        Returns:
            Dictionary containing financial statements or error information
        """
        try:
            stock = yf.Ticker(ticker.upper())
            
            statements = {
                'income_statement': None,
                'balance_sheet': None,
                'cash_flow': None
            }
            
            # Fetch each statement with individual error handling
            try:
                statements['income_statement'] = stock.financials
            except Exception as e:
                self.logger.warning(f"Could not fetch income statement for {ticker}: {e}")
            
            try:
                statements['balance_sheet'] = stock.balance_sheet
            except Exception as e:
                self.logger.warning(f"Could not fetch balance sheet for {ticker}: {e}")
            
            try:
                statements['cash_flow'] = stock.cashflow
            except Exception as e:
                self.logger.warning(f"Could not fetch cash flow for {ticker}: {e}")
            
            return {
                'success': True,
                'error': None,
                'data': statements,
                'ticker': ticker.upper(),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching financial statements for {ticker}: {e}")
            return {
                'success': False,
                'error': f"Failed to fetch financial statements for {ticker}: {str(e)}",
                'data': None
            }
    
    def get_recommendations(self, ticker: str) -> Dict[str, Any]:
        """
        Fetches analyst recommendations for a ticker.
        
        Args:
            ticker: The ticker symbol
            
        Returns:
            Dictionary containing recommendations or error information
        """
        try:
            stock = yf.Ticker(ticker.upper())
            recommendations = stock.recommendations
            
            return {
                'success': True,
                'error': None,
                'data': recommendations,
                'ticker': ticker.upper(),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching recommendations for {ticker}: {e}")
            return {
                'success': False,
                'error': f"Failed to fetch recommendations for {ticker}: {str(e)}",
                'data': None
            }
    
    def get_multiple_company_info(self, tickers: list) -> Dict[str, Any]:
        """
        Fetches company information for multiple tickers efficiently.
        
        Args:
            tickers: List of ticker symbols
            
        Returns:
            Dictionary containing results for each ticker
        """
        results = {}
        successful_fetches = 0
        
        for ticker in tickers:
            if not ticker:
                continue
                
            ticker = ticker.upper().strip()
            self.logger.info(f"Fetching data for {ticker}...")
            
            result = self.get_company_info(ticker)
            results[ticker] = result
            
            if result['success']:
                successful_fetches += 1
        
        return {
            'success': successful_fetches > 0,
            'total_requested': len(tickers),
            'successful_fetches': successful_fetches,
            'results': results,
            'timestamp': datetime.now()
        }
    
    def get_peer_comparison_data(self, main_ticker: str, peer_tickers: list) -> Dict[str, Any]:
        """
        Fetches data for peer comparison analysis.
        
        Args:
            main_ticker: The primary ticker to compare
            peer_tickers: List of peer ticker symbols
            
        Returns:
            Dictionary containing comparison data for all tickers
        """
        all_tickers = [main_ticker.upper()] + [t.upper() for t in peer_tickers if t]
        comparison_data = {}
        
        self.logger.info("Fetching data for peer comparison...")
        
        for ticker in all_tickers:
            try:
                self.logger.info(f"  Fetching {ticker}...")
                result = self.get_company_info(ticker)
                
                if result['success']:
                    comparison_data[ticker] = result['data']
                else:
                    self.logger.warning(f"  Could not fetch data for {ticker}: {result['error']}")
                    comparison_data[ticker] = None
                    
            except Exception as e:
                self.logger.error(f"  Error fetching {ticker}: {e}")
                comparison_data[ticker] = None
        
        # Filter out failed fetches
        successful_data = {k: v for k, v in comparison_data.items() if v is not None}
        
        return {
            'success': len(successful_data) > 0,
            'main_ticker': main_ticker.upper(),
            'peer_tickers': [t.upper() for t in peer_tickers],
            'data': successful_data,
            'failed_tickers': [k for k, v in comparison_data.items() if v is None],
            'timestamp': datetime.now()
        }
    
    def get_batch_financial_statements(self, tickers: list) -> Dict[str, Any]:
        """
        Fetches financial statements for multiple tickers with partial failure handling.
        
        Args:
            tickers: List of ticker symbols
            
        Returns:
            Dictionary containing statements for each ticker
        """
        results = {}
        
        for ticker in tickers:
            if not ticker:
                continue
                
            ticker = ticker.upper().strip()
            result = self.get_financial_statements(ticker)
            results[ticker] = result
        
        successful_fetches = sum(1 for r in results.values() if r['success'])
        
        return {
            'success': successful_fetches > 0,
            'total_requested': len(tickers),
            'successful_fetches': successful_fetches,
            'results': results,
            'timestamp': datetime.now()
        }
    
    def get_stock_history(self, ticker: str, period: str = "1y") -> Dict[str, Any]:
        """
        Fetches historical stock price data.
        
        Args:
            ticker: The ticker symbol
            period: Time period for historical data (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            Dictionary containing historical data or error information
        """
        try:
            stock = yf.Ticker(ticker.upper())
            history = stock.history(period=period)
            
            if history.empty:
                return {
                    'success': False,
                    'error': f"No historical data found for {ticker}",
                    'data': None
                }
            
            return {
                'success': True,
                'error': None,
                'data': history,
                'ticker': ticker.upper(),
                'period': period,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Error fetching stock history for {ticker}: {e}")
            return {
                'success': False,
                'error': f"Failed to fetch stock history for {ticker}: {str(e)}",
                'data': None
            }
    
    def suggest_peers_from_recommendations(self, ticker: str, max_peers: int = 4) -> list:
        """
        Attempts to suggest peer companies from Yahoo Finance recommendations.
        
        Args:
            ticker: The ticker symbol to find peers for
            max_peers: Maximum number of peers to suggest
            
        Returns:
            List of suggested peer ticker symbols
        """
        try:
            stock = yf.Ticker(ticker.upper())
            recommendations = stock.recommendations_summary
            
            if recommendations is not None and 'recommended_tickers' in recommendations:
                suggested_peers = [item['symbol'] for item in recommendations['recommended_tickers']][:max_peers]
                return suggested_peers
            
        except Exception as e:
            self.logger.warning(f"Could not fetch peer suggestions for {ticker}: {e}")
        
        return []