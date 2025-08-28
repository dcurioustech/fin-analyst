"""
Display formatting functionality for analysis results.
"""

import logging
from typing import Any, Dict, Optional

import pandas as pd

from utils.formatters import format_large_number, format_percentage, format_ratio


class DisplayFormatter:
    """Handles output formatting and display logic for analysis results."""

    def __init__(self):
        """Initialize the display formatter."""
        self.logger = logging.getLogger(__name__)

    def format_company_profile(self, profile_data: Dict[str, Any]) -> str:
        """
        Formats company profile data for display.

        Args:
            profile_data: Company profile data from analyzer

        Returns:
            Formatted string for display
        """
        try:
            if not profile_data or not profile_data.get("success"):
                return f"Error: {profile_data.get('error', 'Unknown error')}"

            data = profile_data["data"]
            basic_info = data["basic_info"]

            output_lines = [
                "\n--- Company Profile ---",
                f"Name: {basic_info['name']}",
                f"Sector: {basic_info['sector']}",
                f"Industry: {basic_info['industry']}",
                f"Country: {basic_info['country']}",
            ]

            if basic_info["website"] != "N/A":
                output_lines.append(f"Website: {basic_info['website']}")

            if basic_info["employees"] != "N/A":
                try:
                    employees = int(basic_info["employees"])
                    output_lines.append(f"Employees: {employees:,}")
                except (ValueError, TypeError):
                    output_lines.append(f"Employees: {basic_info['employees']}")

            output_lines.extend(
                ["\nBusiness Summary:", data["business_summary"], "-" * 25]
            )

            return "\n".join(output_lines)

        except Exception as e:
            self.logger.error(f"Error formatting company profile: {e}")
            return "Error formatting company profile data"

    def format_metrics_display(self, metrics_data: Dict[str, Any]) -> str:
        """
        Formats financial metrics data for display.

        Args:
            metrics_data: Metrics data from analyzer

        Returns:
            Formatted string for display
        """
        try:
            if not metrics_data or not metrics_data.get("success"):
                return f"Error: {metrics_data.get('error', 'Unknown error')}"

            metrics = metrics_data["data"]
            output_lines = ["\n--- Key Financial Metrics ---"]

            # Valuation Metrics
            if "valuation" in metrics and metrics["valuation"]:
                output_lines.append("Valuation:")
                val_metrics = metrics["valuation"]

                if val_metrics.get("market_cap"):
                    output_lines.append(
                        f"  Market Cap: {format_large_number(val_metrics['market_cap'])}"
                    )
                if val_metrics.get("enterprise_value"):
                    output_lines.append(
                        f"  Enterprise Value: {format_large_number(val_metrics['enterprise_value'])}"
                    )
                if val_metrics.get("trailing_pe"):
                    output_lines.append(
                        f"  Trailing P/E: {format_ratio(val_metrics['trailing_pe'])}"
                    )
                if val_metrics.get("forward_pe"):
                    output_lines.append(
                        f"  Forward P/E: {format_ratio(val_metrics['forward_pe'])}"
                    )
                if val_metrics.get("price_to_sales"):
                    output_lines.append(
                        f"  Price to Sales (TTM): {format_ratio(val_metrics['price_to_sales'])}"
                    )
                if val_metrics.get("price_to_book"):
                    output_lines.append(
                        f"  Price to Book: {format_ratio(val_metrics['price_to_book'])}"
                    )

            # Profitability Metrics
            if "profitability" in metrics and metrics["profitability"]:
                output_lines.append("\nProfitability & Management:")
                prof_metrics = metrics["profitability"]

                if prof_metrics.get("profit_margins"):
                    output_lines.append(
                        f"  Profit Margins: {format_percentage(prof_metrics['profit_margins'])}"
                    )
                if prof_metrics.get("return_on_equity"):
                    output_lines.append(
                        f"  Return on Equity (ROE): {format_percentage(prof_metrics['return_on_equity'])}"
                    )
                if prof_metrics.get("return_on_assets"):
                    output_lines.append(
                        f"  Return on Assets (ROA): {format_percentage(prof_metrics['return_on_assets'])}"
                    )

            # Stock Price Info
            if "stock_price" in metrics and metrics["stock_price"]:
                output_lines.append("\nStock Price Info:")
                price_metrics = metrics["stock_price"]

                if price_metrics.get("current_price"):
                    output_lines.append(
                        f"  Current Price: {price_metrics['current_price']}"
                    )

                fifty_two_low = price_metrics.get("fifty_two_week_low")
                fifty_two_high = price_metrics.get("fifty_two_week_high")
                if fifty_two_low and fifty_two_high:
                    output_lines.append(
                        f"  52-Week Range: {fifty_two_low} - {fifty_two_high}"
                    )

                if price_metrics.get("beta"):
                    output_lines.append(
                        f"  Beta: {format_ratio(price_metrics['beta'])}"
                    )

            # Dividend Info
            if "dividend" in metrics and metrics["dividend"]:
                output_lines.append("\nDividends:")
                div_metrics = metrics["dividend"]

                if div_metrics.get("dividend_yield"):
                    output_lines.append(
                        f"  Dividend Yield: {format_percentage(div_metrics['dividend_yield'])}"
                    )
                if div_metrics.get("payout_ratio"):
                    output_lines.append(
                        f"  Payout Ratio: {format_percentage(div_metrics['payout_ratio'])}"
                    )

            output_lines.append("-" * 25)
            return "\n".join(output_lines)

        except Exception as e:
            self.logger.error(f"Error formatting metrics display: {e}")
            return "Error formatting metrics data"

    def format_statement_display(
        self, statement_data: Dict[str, Any], statement_name: str
    ) -> str:
        """
        Formats financial statement data for display.

        Args:
            statement_data: Statement data from analyzer
            statement_name: Name of the statement

        Returns:
            Formatted string for display
        """
        try:
            if not statement_data or not statement_data.get("success"):
                return f"Error: {statement_data.get('error', f'No {statement_name} data available.')}"

            data = statement_data["data"]
            formatted_data = data.get("formatted_data")

            if formatted_data is None or formatted_data.empty:
                return f"No {statement_name} data available."

            output_lines = [
                f"\n--- {statement_name} (Annual) ---",
                str(formatted_data),
                "-" * (len(statement_name) + 12),
            ]

            return "\n".join(output_lines)

        except Exception as e:
            self.logger.error(f"Error formatting {statement_name} display: {e}")
            return f"Could not retrieve {statement_name}: {e}"

    def format_comparison_display(self, comparison_data: Dict[str, Any]) -> str:
        """
        Formats peer comparison data for display.

        Args:
            comparison_data: Comparison data from analyzer

        Returns:
            Formatted string for display
        """
        try:
            if not comparison_data or not comparison_data.get("success"):
                return (
                    f"Error: {comparison_data.get('error', 'Unknown comparison error')}"
                )

            data = comparison_data["data"]
            output_lines = ["\n--- Peer Comparison ---"]

            # Display comparison table
            if "comparison_table" in data and not data["comparison_table"].empty:
                output_lines.append("\n--- Comparison Table ---")
                df = data["comparison_table"]
                output_lines.append(df.round(2).to_string())

            # Display visual comparisons
            if "visual_comparisons" in data:
                output_lines.append("\n--- Visual Comparison ---")
                visuals = data["visual_comparisons"]

                for metric_name, visual_chart in visuals.items():
                    if metric_name != "error":
                        output_lines.append(visual_chart)

            # Display competitive analysis
            if "competitive_analysis" in data:
                comp_analysis = data["competitive_analysis"]
                if comp_analysis.get("success") and comp_analysis.get("data"):
                    analysis_data = comp_analysis["data"]
                    main_ticker = data.get("main_ticker", "Company")

                    output_lines.append(
                        f"\n--- Competitive Position for {main_ticker} ---"
                    )

                    if analysis_data.get("strengths"):
                        output_lines.append("Strengths:")
                        for strength in analysis_data["strengths"]:
                            output_lines.append(f"  • {strength}")

                    if analysis_data.get("weaknesses"):
                        output_lines.append("Areas for Improvement:")
                        for weakness in analysis_data["weaknesses"]:
                            output_lines.append(f"  • {weakness}")

            # Display summary
            if "summary" in data:
                output_lines.append(f"\n--- Summary ---")
                output_lines.append(data["summary"])

            return "\n".join(output_lines)

        except Exception as e:
            self.logger.error(f"Error formatting comparison display: {e}")
            return "Error formatting comparison data"

    def format_recommendations_display(
        self, recommendations_data: Dict[str, Any]
    ) -> str:
        """
        Formats analyst recommendations data for display.

        Args:
            recommendations_data: Recommendations data from service

        Returns:
            Formatted string for display
        """
        try:
            if not recommendations_data or not recommendations_data.get("success"):
                return f"Error: {recommendations_data.get('error', 'No recommendations available.')}"

            recommendations = recommendations_data["data"]

            if recommendations is None or recommendations.empty:
                return "No analyst recommendations available."

            output_lines = [
                "\n--- Analyst Recommendations (Last 30) ---",
                str(recommendations.tail(30)),
                "-" * 35,
            ]

            return "\n".join(output_lines)

        except Exception as e:
            self.logger.error(f"Error formatting recommendations display: {e}")
            return f"Error displaying recommendations: {e}"

    def format_error_message(self, error: Exception) -> str:
        """
        Formats error messages for user display.

        Args:
            error: Exception object

        Returns:
            Formatted error message string
        """
        try:
            error_message = str(error)

            # Make error messages more user-friendly
            if "ticker" in error_message.lower():
                return "Invalid ticker symbol or no data available. Please check the symbol and try again."
            elif (
                "network" in error_message.lower()
                or "connection" in error_message.lower()
            ):
                return "Network error. Please check your internet connection and try again."
            elif "timeout" in error_message.lower():
                return "Request timed out. Please try again later."
            else:
                return f"An error occurred: {error_message}"

        except Exception:
            return "An unexpected error occurred. Please try again."

    def format_loading_message(self, operation: str, ticker: str = None) -> str:
        """
        Formats loading messages for operations.

        Args:
            operation: Description of the operation
            ticker: Optional ticker symbol

        Returns:
            Formatted loading message
        """
        if ticker:
            return f"  Fetching {operation} for {ticker}..."
        else:
            return f"  {operation}..."

    def format_success_message(self, operation: str, ticker: str = None) -> str:
        """
        Formats success messages for completed operations.

        Args:
            operation: Description of the operation
            ticker: Optional ticker symbol

        Returns:
            Formatted success message
        """
        if ticker:
            return f"✓ Successfully {operation} for {ticker}"
        else:
            return f"✓ {operation} completed successfully"

    def format_data_table(self, data: pd.DataFrame, title: str = None) -> str:
        """
        Formats a pandas DataFrame for display with optional title.

        Args:
            data: DataFrame to format
            title: Optional title for the table

        Returns:
            Formatted table string
        """
        try:
            if data.empty:
                return "No data available."

            output_lines = []

            if title:
                output_lines.append(f"\n--- {title} ---")

            # Format numeric columns
            formatted_data = data.copy()
            for col in formatted_data.columns:
                if formatted_data[col].dtype in ["float64", "int64"]:
                    formatted_data[col] = formatted_data[col].apply(
                        lambda x: format_large_number(x) if pd.notna(x) else "N/A"
                    )

            output_lines.append(str(formatted_data))

            if title:
                output_lines.append("-" * (len(title) + 8))

            return "\n".join(output_lines)

        except Exception as e:
            self.logger.error(f"Error formatting data table: {e}")
            return "Error formatting table data"
