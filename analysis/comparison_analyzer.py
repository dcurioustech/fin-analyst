"""
Peer comparison analysis functionality.
"""
from typing import Dict, Any, List, Optional
import pandas as pd
import logging
from config.settings import COMPARISON_METRICS
from utils.visualizations import create_comparison_chart, plot_text_bar


class ComparisonAnalyzer:
    """Analyzer for peer comparison and competitive analysis."""
    
    def __init__(self):
        """Initialize the comparison analyzer."""
        self.logger = logging.getLogger(__name__)
    
    def perform_peer_comparison(self, main_ticker: str, peer_tickers: List[str], 
                              companies_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Performs comprehensive peer comparison analysis.
        
        Args:
            main_ticker: The primary ticker to compare
            peer_tickers: List of peer ticker symbols
            companies_data: Dictionary containing company data for all tickers
            
        Returns:
            Dictionary with comparison analysis results
        """
        try:
            if not companies_data:
                return {
                    'success': False,
                    'error': 'No company data provided for comparison',
                    'data': None
                }
            
            # Calculate comparison metrics
            comparison_metrics = self.calculate_comparison_metrics(companies_data)
            
            # Generate visual comparisons
            visual_data = self.generate_comparison_visuals(comparison_metrics)
            
            # Analyze competitive positioning
            competitive_analysis = self.analyze_competitive_positioning(
                main_ticker, comparison_metrics
            )
            
            comparison_results = {
                'main_ticker': main_ticker,
                'peer_tickers': peer_tickers,
                'comparison_table': comparison_metrics,
                'visual_comparisons': visual_data,
                'competitive_analysis': competitive_analysis,
                'summary': self._generate_comparison_summary(main_ticker, comparison_metrics)
            }
            
            return {
                'success': True,
                'data': comparison_results,
                'error': None
            }
            
        except Exception as e:
            self.logger.error(f"Error performing peer comparison: {e}")
            return {
                'success': False,
                'data': None,
                'error': f"Failed to perform peer comparison: {str(e)}"
            }
    
    def suggest_peers(self, company_info: Dict[str, Any]) -> List[str]:
        """
        Suggests peer companies based on sector and industry.
        
        Args:
            company_info: Company information dictionary
            
        Returns:
            List of suggested peer ticker symbols
        """
        # This is a placeholder implementation
        # In a real system, this would use sector/industry data to suggest peers
        suggested_peers = []
        
        try:
            # Try to extract sector and industry for peer suggestion logic
            sector = company_info.get('sector', '')
            industry = company_info.get('industry', '')
            
            # For now, return empty list as we don't have a peer database
            # In production, this would query a database of companies by sector/industry
            self.logger.info(f"Would suggest peers for sector: {sector}, industry: {industry}")
            
        except Exception as e:
            self.logger.warning(f"Error suggesting peers: {e}")
        
        return suggested_peers
    
    def calculate_comparison_metrics(self, companies_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Calculates comparison metrics for all companies.
        
        Args:
            companies_data: Dictionary containing company data for all tickers
            
        Returns:
            DataFrame with comparison metrics
        """
        try:
            comparison_data = []
            
            for ticker, company_info in companies_data.items():
                if not company_info:
                    continue
                
                data_point = {'Ticker': ticker}
                
                # Extract metrics defined in settings
                for key, display_name in COMPARISON_METRICS.items():
                    value = company_info.get(key)
                    
                    # Convert percentage metrics to percentage values
                    if '%' in display_name and value is not None:
                        value *= 100
                    
                    data_point[display_name] = value if value is not None else 'N/A'
                
                comparison_data.append(data_point)
            
            if not comparison_data:
                return pd.DataFrame()
            
            # Create DataFrame and set ticker as index
            df = pd.DataFrame(comparison_data)
            df.set_index('Ticker', inplace=True)
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error calculating comparison metrics: {e}")
            return pd.DataFrame()
    
    def generate_comparison_visuals(self, comparison_data: pd.DataFrame) -> Dict[str, str]:
        """
        Generates visual comparisons for the metrics.
        
        Args:
            comparison_data: DataFrame with comparison metrics
            
        Returns:
            Dictionary with visual representations for each metric
        """
        visual_data = {}
        
        try:
            if comparison_data.empty:
                return {'error': 'No data available for visualization'}
            
            # Convert to numeric for plotting, handling 'N/A' values
            df_numeric = comparison_data.apply(pd.to_numeric, errors='coerce').fillna(0)
            
            # Generate visual for each metric column
            for column in df_numeric.columns:
                visual_lines = [f"\n-- {column} --"]
                
                # Use the max of the absolute values for scaling
                max_val = df_numeric[column].abs().max()
                if pd.isna(max_val) or max_val == 0:
                    max_val = 1  # Avoid division by zero
                
                # Create bar chart for each ticker
                for ticker, value in df_numeric[column].items():
                    visual_lines.append(plot_text_bar(ticker, value, max_val))
                
                visual_lines.append("-" * 25)
                visual_data[column] = "\n".join(visual_lines)
            
            return visual_data
            
        except Exception as e:
            self.logger.error(f"Error generating comparison visuals: {e}")
            return {'error': f'Error generating visuals: {str(e)}'}
    
    def analyze_competitive_positioning(self, main_ticker: str, 
                                      comparison_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyzes the competitive positioning of the main ticker.
        
        Args:
            main_ticker: The primary ticker being analyzed
            comparison_data: DataFrame with comparison metrics
            
        Returns:
            Dictionary with competitive positioning analysis
        """
        try:
            if comparison_data.empty or main_ticker not in comparison_data.index:
                return {
                    'success': False,
                    'error': 'Insufficient data for competitive analysis'
                }
            
            positioning = {
                'strengths': [],
                'weaknesses': [],
                'rankings': {},
                'percentile_rankings': {}
            }
            
            # Convert to numeric for analysis
            df_numeric = comparison_data.apply(pd.to_numeric, errors='coerce')
            
            # Analyze each metric
            for column in df_numeric.columns:
                if main_ticker not in df_numeric.index:
                    continue
                
                main_value = df_numeric.loc[main_ticker, column]
                if pd.isna(main_value):
                    continue
                
                # Calculate ranking (1 = best)
                column_values = df_numeric[column].dropna()
                if len(column_values) <= 1:
                    continue
                
                # Determine if higher is better based on metric type
                higher_is_better = self._is_higher_better(column)
                
                if higher_is_better:
                    # For higher-is-better metrics: rank 1 = highest value
                    rank = (column_values > main_value).sum() + 1
                    # Percentile: what % of values are <= this value
                    percentile = ((column_values < main_value).sum() / len(column_values)) * 100
                else:
                    # For lower-is-better metrics: rank 1 = lowest value  
                    rank = (column_values < main_value).sum() + 1
                    # Percentile: what % of values are >= this value (inverted for lower-is-better)
                    percentile = ((column_values > main_value).sum() / len(column_values)) * 100
                
                positioning['rankings'][column] = f"{rank} of {len(column_values)}"
                positioning['percentile_rankings'][column] = f"{percentile:.0f}th percentile"
                
                # Identify strengths and weaknesses based on percentile ranking
                # For 2-company comparisons, use 50% threshold; for larger groups use 75%/25%
                if len(column_values) == 2:
                    # For head-to-head comparisons, use 50% threshold
                    strength_threshold = 50
                    weakness_threshold = 50
                else:
                    # For larger groups, use quartile thresholds
                    strength_threshold = 75
                    weakness_threshold = 25
                
                if percentile > strength_threshold:
                    # Better performance
                    if higher_is_better:
                        positioning['strengths'].append(f"Strong {column.lower()}")
                    else:
                        positioning['strengths'].append(f"Strong {column.lower()} (attractive valuation)")
                elif percentile < weakness_threshold:
                    # Worse performance
                    if higher_is_better:
                        positioning['weaknesses'].append(f"Weak {column.lower()}")
                    else:
                        positioning['weaknesses'].append(f"Weak {column.lower()} (expensive valuation)")
            
            return {
                'success': True,
                'data': positioning,
                'error': None
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing competitive positioning: {e}")
            return {
                'success': False,
                'data': None,
                'error': f"Failed to analyze competitive positioning: {str(e)}"
            }
    
    def format_comparison_for_display(self, comparison_results: Dict[str, Any]) -> str:
        """
        Formats comparison results for console display.
        
        Args:
            comparison_results: Results from peer comparison analysis
            
        Returns:
            Formatted string for display
        """
        try:
            output_lines = []
            
            # Display comparison table
            if 'comparison_table' in comparison_results:
                output_lines.append("\n--- Comparison Table ---")
                df = comparison_results['comparison_table']
                if not df.empty:
                    output_lines.append(df.round(2).to_string())
                else:
                    output_lines.append("No comparison data available.")
            
            # Display competitive analysis
            if 'competitive_analysis' in comparison_results:
                comp_analysis = comparison_results['competitive_analysis']
                if comp_analysis.get('success') and comp_analysis.get('data'):
                    data = comp_analysis['data']
                    
                    output_lines.append(f"\n--- Competitive Position for {comparison_results['main_ticker']} ---")
                    
                    if data.get('strengths'):
                        output_lines.append("Strengths:")
                        for strength in data['strengths']:
                            output_lines.append(f"  • {strength}")
                    
                    if data.get('weaknesses'):
                        output_lines.append("Areas for Improvement:")
                        for weakness in data['weaknesses']:
                            output_lines.append(f"  • {weakness}")
                    
                    if data.get('rankings'):
                        output_lines.append("Rankings:")
                        for metric, ranking in data['rankings'].items():
                            output_lines.append(f"  {metric}: {ranking}")
            
            # Display summary
            if 'summary' in comparison_results:
                output_lines.append(f"\n--- Summary ---")
                output_lines.append(comparison_results['summary'])
            
            return "\n".join(output_lines)
            
        except Exception as e:
            self.logger.error(f"Error formatting comparison for display: {e}")
            return "Error formatting comparison results"
    
    def _is_higher_better(self, metric_name: str) -> bool:
        """
        Determines if higher values are better for a given metric.
        
        Args:
            metric_name: Name of the metric
            
        Returns:
            True if higher is better, False otherwise
        """
        # Metrics where higher is better
        higher_better = [
            'market cap', 'profit margin', 'roe', 'return on equity', 'return on assets',
            'revenue growth', 'earnings growth', 'gross margin', 'operating margin',
            'free cash flow', 'current ratio', 'quick ratio'
        ]
        
        # Metrics where lower is better (valuation ratios, debt ratios, etc.)
        lower_better = [
            'p/e', 'p/s', 'p/b', 'price to earnings', 'price to sales', 'price to book',
            'pe ratio', 'ps ratio', 'pb ratio', 'debt to equity', 'debt/equity',
            'debt ratio', 'beta', 'peg ratio'
        ]
        
        metric_lower = metric_name.lower()
        
        # Check lower_better first since these are more specific
        for term in lower_better:
            if term in metric_lower:
                return False
        
        for term in higher_better:
            if term in metric_lower:
                return True
        
        # Default to higher is better for unknown metrics
        return True
    
    def _generate_comparison_summary(self, main_ticker: str, 
                                   comparison_data: pd.DataFrame) -> str:
        """
        Generates a summary of the comparison analysis.
        
        Args:
            main_ticker: The primary ticker
            comparison_data: DataFrame with comparison metrics
            
        Returns:
            Summary string
        """
        try:
            if comparison_data.empty:
                return "No data available for summary."
            
            total_companies = len(comparison_data)
            
            summary_parts = [
                f"{main_ticker} compared against {total_companies - 1} peer companies.",
                f"Analysis includes {len(comparison_data.columns)} key financial metrics.",
            ]
            
            # Add basic insights if data is available
            if main_ticker in comparison_data.index:
                df_numeric = comparison_data.apply(pd.to_numeric, errors='coerce')
                
                # Count how many metrics the company leads in
                leading_count = 0
                for column in df_numeric.columns:
                    if main_ticker not in df_numeric.index:
                        continue
                    
                    main_value = df_numeric.loc[main_ticker, column]
                    if pd.isna(main_value):
                        continue
                    
                    column_values = df_numeric[column].dropna()
                    if len(column_values) <= 1:
                        continue
                    
                    higher_is_better = self._is_higher_better(column)
                    
                    if higher_is_better and main_value == column_values.max():
                        leading_count += 1
                    elif not higher_is_better and main_value == column_values.min():
                        leading_count += 1
                
                if leading_count > 0:
                    summary_parts.append(f"{main_ticker} leads in {leading_count} metric(s).")
            
            return " ".join(summary_parts)
            
        except Exception as e:
            self.logger.error(f"Error generating comparison summary: {e}")
            return "Error generating summary."