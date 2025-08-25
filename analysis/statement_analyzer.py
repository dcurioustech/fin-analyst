"""
Financial statement analysis functionality.
"""
from typing import Dict, Any, Optional
import pandas as pd
import logging
from utils.formatters import format_large_number


class StatementAnalyzer:
    """Analyzer for financial statements processing and formatting."""
    
    def __init__(self):
        """Initialize the statement analyzer."""
        self.logger = logging.getLogger(__name__)
    
    def process_income_statement(self, statement_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Processes income statement data for analysis.
        
        Args:
            statement_data: Raw income statement DataFrame
            
        Returns:
            Dictionary with processed income statement data
        """
        try:
            if statement_data is None or statement_data.empty:
                return {
                    'success': False,
                    'error': 'No income statement data available',
                    'data': None
                }
            
            # Extract key income statement items
            processed_data = {
                'raw_data': statement_data,
                'key_metrics': self._extract_income_statement_metrics(statement_data),
                'formatted_data': self._format_statement_data(statement_data)
            }
            
            return {
                'success': True,
                'data': processed_data,
                'error': None
            }
            
        except Exception as e:
            self.logger.error(f"Error processing income statement: {e}")
            return {
                'success': False,
                'data': None,
                'error': f"Failed to process income statement: {str(e)}"
            }
    
    def process_balance_sheet(self, statement_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Processes balance sheet data for analysis.
        
        Args:
            statement_data: Raw balance sheet DataFrame
            
        Returns:
            Dictionary with processed balance sheet data
        """
        try:
            if statement_data is None or statement_data.empty:
                return {
                    'success': False,
                    'error': 'No balance sheet data available',
                    'data': None
                }
            
            # Extract key balance sheet items
            processed_data = {
                'raw_data': statement_data,
                'key_metrics': self._extract_balance_sheet_metrics(statement_data),
                'formatted_data': self._format_statement_data(statement_data)
            }
            
            return {
                'success': True,
                'data': processed_data,
                'error': None
            }
            
        except Exception as e:
            self.logger.error(f"Error processing balance sheet: {e}")
            return {
                'success': False,
                'data': None,
                'error': f"Failed to process balance sheet: {str(e)}"
            }
    
    def process_cash_flow(self, statement_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Processes cash flow statement data for analysis.
        
        Args:
            statement_data: Raw cash flow DataFrame
            
        Returns:
            Dictionary with processed cash flow data
        """
        try:
            if statement_data is None or statement_data.empty:
                return {
                    'success': False,
                    'error': 'No cash flow data available',
                    'data': None
                }
            
            # Extract key cash flow items
            processed_data = {
                'raw_data': statement_data,
                'key_metrics': self._extract_cash_flow_metrics(statement_data),
                'formatted_data': self._format_statement_data(statement_data)
            }
            
            return {
                'success': True,
                'data': processed_data,
                'error': None
            }
            
        except Exception as e:
            self.logger.error(f"Error processing cash flow statement: {e}")
            return {
                'success': False,
                'data': None,
                'error': f"Failed to process cash flow statement: {str(e)}"
            }
    
    def format_statement_for_display(self, statement: pd.DataFrame, statement_name: str) -> str:
        """
        Formats a financial statement for console display.
        
        Args:
            statement: The financial statement DataFrame
            statement_name: Name of the statement for display
            
        Returns:
            Formatted string representation of the statement
        """
        try:
            if statement is None or statement.empty:
                return f"No {statement_name} data available."
            
            # Format all numeric columns to be more readable
            formatted_statement = statement.applymap(
                lambda x: format_large_number(x) if isinstance(x, (int, float)) else x
            )
            
            output_lines = [
                f"\n--- {statement_name} (Annual) ---",
                str(formatted_statement),
                "-" * (len(statement_name) + 12)
            ]
            
            return "\n".join(output_lines)
            
        except Exception as e:
            self.logger.error(f"Error formatting {statement_name} for display: {e}")
            return f"Could not format {statement_name}: {e}"
    
    def get_all_statements_analysis(self, statements_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """
        Analyzes all financial statements together.
        
        Args:
            statements_data: Dictionary containing all statement DataFrames
            
        Returns:
            Dictionary with comprehensive statement analysis
        """
        try:
            analysis_results = {}
            
            # Process each statement type
            if 'income_statement' in statements_data:
                analysis_results['income_statement'] = self.process_income_statement(
                    statements_data['income_statement']
                )
            
            if 'balance_sheet' in statements_data:
                analysis_results['balance_sheet'] = self.process_balance_sheet(
                    statements_data['balance_sheet']
                )
            
            if 'cash_flow' in statements_data:
                analysis_results['cash_flow'] = self.process_cash_flow(
                    statements_data['cash_flow']
                )
            
            # Calculate cross-statement metrics if data is available
            cross_metrics = self._calculate_cross_statement_metrics(analysis_results)
            
            return {
                'success': True,
                'data': {
                    'individual_statements': analysis_results,
                    'cross_statement_metrics': cross_metrics
                },
                'error': None
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing all statements: {e}")
            return {
                'success': False,
                'data': None,
                'error': f"Failed to analyze statements: {str(e)}"
            }
    
    def _extract_income_statement_metrics(self, income_statement: pd.DataFrame) -> Dict[str, Any]:
        """
        Extracts key metrics from income statement.
        
        Args:
            income_statement: Income statement DataFrame
            
        Returns:
            Dictionary with key income statement metrics
        """
        metrics = {}
        
        try:
            # Common income statement line items (case-insensitive search)
            line_items = {
                'total_revenue': ['Total Revenue', 'Revenue', 'Net Sales'],
                'gross_profit': ['Gross Profit'],
                'operating_income': ['Operating Income', 'Operating Profit'],
                'net_income': ['Net Income', 'Net Earnings'],
                'ebitda': ['EBITDA', 'Normalized EBITDA']
            }
            
            for metric_name, possible_names in line_items.items():
                for name in possible_names:
                    matching_rows = income_statement.index[
                        income_statement.index.str.contains(name, case=False, na=False)
                    ]
                    if not matching_rows.empty:
                        # Get the most recent year (first column)
                        metrics[metric_name] = income_statement.loc[matching_rows[0]].iloc[0]
                        break
        
        except Exception as e:
            self.logger.warning(f"Error extracting income statement metrics: {e}")
        
        return metrics
    
    def _extract_balance_sheet_metrics(self, balance_sheet: pd.DataFrame) -> Dict[str, Any]:
        """
        Extracts key metrics from balance sheet.
        
        Args:
            balance_sheet: Balance sheet DataFrame
            
        Returns:
            Dictionary with key balance sheet metrics
        """
        metrics = {}
        
        try:
            # Common balance sheet line items
            line_items = {
                'total_assets': ['Total Assets'],
                'total_liabilities': ['Total Liabilities', 'Total Liab'],
                'total_equity': ['Total Stockholder Equity', 'Total Equity', 'Stockholder Equity'],
                'cash_and_equivalents': ['Cash And Cash Equivalents', 'Cash'],
                'total_debt': ['Total Debt', 'Long Term Debt']
            }
            
            for metric_name, possible_names in line_items.items():
                for name in possible_names:
                    matching_rows = balance_sheet.index[
                        balance_sheet.index.str.contains(name, case=False, na=False)
                    ]
                    if not matching_rows.empty:
                        # Get the most recent year (first column)
                        metrics[metric_name] = balance_sheet.loc[matching_rows[0]].iloc[0]
                        break
        
        except Exception as e:
            self.logger.warning(f"Error extracting balance sheet metrics: {e}")
        
        return metrics
    
    def _extract_cash_flow_metrics(self, cash_flow: pd.DataFrame) -> Dict[str, Any]:
        """
        Extracts key metrics from cash flow statement.
        
        Args:
            cash_flow: Cash flow DataFrame
            
        Returns:
            Dictionary with key cash flow metrics
        """
        metrics = {}
        
        try:
            # Common cash flow line items
            line_items = {
                'operating_cash_flow': ['Total Cash From Operating Activities', 'Operating Cash Flow'],
                'investing_cash_flow': ['Total Cash From Investing Activities', 'Investing Cash Flow'],
                'financing_cash_flow': ['Total Cash From Financing Activities', 'Financing Cash Flow'],
                'free_cash_flow': ['Free Cash Flow'],
                'capital_expenditures': ['Capital Expenditures', 'Capex']
            }
            
            for metric_name, possible_names in line_items.items():
                for name in possible_names:
                    matching_rows = cash_flow.index[
                        cash_flow.index.str.contains(name, case=False, na=False)
                    ]
                    if not matching_rows.empty:
                        # Get the most recent year (first column)
                        metrics[metric_name] = cash_flow.loc[matching_rows[0]].iloc[0]
                        break
        
        except Exception as e:
            self.logger.warning(f"Error extracting cash flow metrics: {e}")
        
        return metrics
    
    def _format_statement_data(self, statement: pd.DataFrame) -> pd.DataFrame:
        """
        Formats statement data for better readability.
        
        Args:
            statement: Raw statement DataFrame
            
        Returns:
            Formatted DataFrame
        """
        try:
            # Create a copy to avoid modifying original
            formatted = statement.copy()
            
            # Format numeric values
            for col in formatted.columns:
                formatted[col] = formatted[col].apply(
                    lambda x: format_large_number(x) if isinstance(x, (int, float)) else x
                )
            
            return formatted
            
        except Exception as e:
            self.logger.warning(f"Error formatting statement data: {e}")
            return statement
    
    def _calculate_cross_statement_metrics(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates metrics that require data from multiple statements.
        
        Args:
            analysis_results: Results from individual statement analyses
            
        Returns:
            Dictionary with cross-statement metrics
        """
        cross_metrics = {}
        
        try:
            # Extract metrics from each statement if available
            income_metrics = {}
            balance_metrics = {}
            cash_flow_metrics = {}
            
            if ('income_statement' in analysis_results and 
                analysis_results['income_statement']['success']):
                income_metrics = analysis_results['income_statement']['data']['key_metrics']
            
            if ('balance_sheet' in analysis_results and 
                analysis_results['balance_sheet']['success']):
                balance_metrics = analysis_results['balance_sheet']['data']['key_metrics']
            
            if ('cash_flow' in analysis_results and 
                analysis_results['cash_flow']['success']):
                cash_flow_metrics = analysis_results['cash_flow']['data']['key_metrics']
            
            # Calculate cross-statement ratios
            # ROA = Net Income / Total Assets
            if 'net_income' in income_metrics and 'total_assets' in balance_metrics:
                net_income = income_metrics['net_income']
                total_assets = balance_metrics['total_assets']
                if net_income and total_assets and total_assets != 0:
                    cross_metrics['return_on_assets'] = net_income / total_assets
            
            # ROE = Net Income / Total Equity
            if 'net_income' in income_metrics and 'total_equity' in balance_metrics:
                net_income = income_metrics['net_income']
                total_equity = balance_metrics['total_equity']
                if net_income and total_equity and total_equity != 0:
                    cross_metrics['return_on_equity'] = net_income / total_equity
            
            # Debt to Equity Ratio
            if 'total_debt' in balance_metrics and 'total_equity' in balance_metrics:
                total_debt = balance_metrics['total_debt']
                total_equity = balance_metrics['total_equity']
                if total_debt and total_equity and total_equity != 0:
                    cross_metrics['debt_to_equity'] = total_debt / total_equity
        
        except Exception as e:
            self.logger.warning(f"Error calculating cross-statement metrics: {e}")
        
        return cross_metrics