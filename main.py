"""
Main application entry point for the Financial Analysis Bot.
"""

import logging
from typing import Optional

# Import analyzers
from analysis.company_analyzer import CompanyAnalyzer
from analysis.comparison_analyzer import ComparisonAnalyzer
from analysis.metrics_analyzer import MetricsAnalyzer
from analysis.statement_analyzer import StatementAnalyzer

# Import configuration
from config.settings import configure_pandas

# Import services
from services.financial_data_service import FinancialDataService
from ui.display_formatter import DisplayFormatter

# Import UI components
from ui.menu_handler import MenuHandler

# Import utilities
from utils.error_handling import log_operation_end, log_operation_start, setup_logging


class FinancialAnalysisApp:
    """Main application class that orchestrates all modules."""

    def __init__(self):
        """Initialize the financial analysis application."""
        # Set up logging
        setup_logging("INFO")
        self.logger = logging.getLogger(__name__)

        # Configure pandas
        configure_pandas()

        # Initialize services
        self.data_service = FinancialDataService()

        # Initialize analyzers
        self.company_analyzer = CompanyAnalyzer()
        self.metrics_analyzer = MetricsAnalyzer()
        self.statement_analyzer = StatementAnalyzer()
        self.comparison_analyzer = ComparisonAnalyzer()

        # Initialize UI components
        self.menu_handler = MenuHandler()
        self.display_formatter = DisplayFormatter()

        self.logger.info("Financial Analysis Application initialized successfully")

    def run(self) -> None:
        """Main application loop."""
        self.logger.info("Starting Financial Analysis Bot")
        print("Welcome to the Financial Analysis Bot!")

        try:
            self._main_loop()
        except KeyboardInterrupt:
            print("\nApplication interrupted by user.")
        except Exception as e:
            self.logger.error(f"Unexpected error in main loop: {e}")
            print(f"An unexpected error occurred: {e}")
        finally:
            self.logger.info("Financial Analysis Bot shutting down")
            self.menu_handler.display_exit_message()

    def _main_loop(self) -> None:
        """Main application loop for ticker selection and analysis."""
        while True:
            # Get ticker input from user
            ticker_symbol = self.menu_handler.get_ticker_input()

            if ticker_symbol == "EXIT":
                break

            if not ticker_symbol:
                continue

            # Validate and fetch company data
            company_data = self._fetch_company_data(ticker_symbol)
            if not company_data:
                continue

            # Display company info and start analysis loop
            company_name = company_data.get("longName", "Unknown Company")
            self.menu_handler.display_ticker_info(ticker_symbol, company_name)

            # Analysis menu loop for this ticker
            self._analysis_loop(ticker_symbol, company_data)

    def _fetch_company_data(self, ticker: str) -> Optional[dict]:
        """
        Fetches and validates company data.

        Args:
            ticker: Ticker symbol

        Returns:
            Company data dictionary or None if failed
        """
        log_operation_start("fetch_company_data", ticker=ticker)

        try:
            # Validate ticker first
            if not self.data_service.validate_ticker(ticker):
                self.menu_handler.handle_ticker_validation_error(ticker)
                return None

            # Fetch company info
            result = self.data_service.get_company_info(ticker)

            if result["success"]:
                log_operation_end("fetch_company_data", True, ticker=ticker)
                return result["data"]
            else:
                self.menu_handler.display_error_message(result["error"])
                log_operation_end(
                    "fetch_company_data", False, ticker=ticker, error=result["error"]
                )
                return None

        except Exception as e:
            error_msg = f"Failed to fetch data for {ticker}: {str(e)}"
            self.logger.error(error_msg)
            self.menu_handler.display_error_message(error_msg)
            return None

    def _analysis_loop(self, ticker: str, company_data: dict) -> None:
        """
        Analysis menu loop for a specific ticker.

        Args:
            ticker: Ticker symbol
            company_data: Company data dictionary
        """
        while True:
            # Display menu and get user choice
            choice = self.menu_handler.handle_menu_navigation(ticker)

            if not choice:
                continue

            # Handle menu choice
            if choice == "1":
                self._handle_company_profile(company_data)
            elif choice == "2":
                self._handle_key_metrics(company_data)
            elif choice == "3":
                self._handle_income_statement(ticker)
            elif choice == "4":
                self._handle_balance_sheet(ticker)
            elif choice == "5":
                self._handle_cash_flow(ticker)
            elif choice == "6":
                self._handle_recommendations(ticker)
            elif choice == "7":
                self._handle_peer_comparison(ticker)
            elif choice == "8":
                break  # New ticker
            elif choice == "9":
                return  # Exit application
            else:
                self.menu_handler.handle_invalid_choice(choice)

    def _handle_company_profile(self, company_data: dict) -> None:
        """Handle company profile analysis."""
        log_operation_start("company_profile_analysis")

        try:
            # Analyze company profile
            profile_result = self.company_analyzer.analyze_company_profile(company_data)

            # Format and display results
            formatted_output = self.display_formatter.format_company_profile(
                profile_result
            )
            print(formatted_output)

            log_operation_end(
                "company_profile_analysis", profile_result.get("success", False)
            )

        except Exception as e:
            error_msg = self.display_formatter.format_error_message(e)
            print(error_msg)
            self.logger.error(f"Error in company profile analysis: {e}")

    def _handle_key_metrics(self, company_data: dict) -> None:
        """Handle key metrics analysis."""
        log_operation_start("key_metrics_analysis")

        try:
            # Analyze comprehensive metrics
            metrics_result = self.metrics_analyzer.get_comprehensive_metrics(
                company_data
            )

            # Format and display results
            formatted_output = self.display_formatter.format_metrics_display(
                metrics_result
            )
            print(formatted_output)

            log_operation_end(
                "key_metrics_analysis", metrics_result.get("success", False)
            )

        except Exception as e:
            error_msg = self.display_formatter.format_error_message(e)
            print(error_msg)
            self.logger.error(f"Error in key metrics analysis: {e}")

    def _handle_income_statement(self, ticker: str) -> None:
        """Handle income statement analysis."""
        self._handle_financial_statement(ticker, "income_statement", "Income Statement")

    def _handle_balance_sheet(self, ticker: str) -> None:
        """Handle balance sheet analysis."""
        self._handle_financial_statement(ticker, "balance_sheet", "Balance Sheet")

    def _handle_cash_flow(self, ticker: str) -> None:
        """Handle cash flow statement analysis."""
        self._handle_financial_statement(ticker, "cash_flow", "Cash Flow Statement")

    def _handle_financial_statement(
        self, ticker: str, statement_type: str, statement_name: str
    ) -> None:
        """
        Handle financial statement analysis.

        Args:
            ticker: Ticker symbol
            statement_type: Type of statement (income_statement, balance_sheet, cash_flow)
            statement_name: Display name of the statement
        """
        log_operation_start(f"{statement_type}_analysis", ticker=ticker)

        try:
            # Fetch financial statements
            statements_result = self.data_service.get_financial_statements(ticker)

            if not statements_result["success"]:
                print(f"Error: {statements_result['error']}")
                return

            # Get specific statement
            statement_data = statements_result["data"].get(statement_type)

            # Analyze statement
            if statement_type == "income_statement":
                analysis_result = self.statement_analyzer.process_income_statement(
                    statement_data
                )
            elif statement_type == "balance_sheet":
                analysis_result = self.statement_analyzer.process_balance_sheet(
                    statement_data
                )
            elif statement_type == "cash_flow":
                analysis_result = self.statement_analyzer.process_cash_flow(
                    statement_data
                )
            else:
                print(f"Unknown statement type: {statement_type}")
                return

            # Format and display results
            formatted_output = self.display_formatter.format_statement_display(
                analysis_result, statement_name
            )
            print(formatted_output)

            log_operation_end(
                f"{statement_type}_analysis",
                analysis_result.get("success", False),
                ticker=ticker,
            )

        except Exception as e:
            error_msg = self.display_formatter.format_error_message(e)
            print(error_msg)
            self.logger.error(f"Error in {statement_name} analysis: {e}")

    def _handle_recommendations(self, ticker: str) -> None:
        """Handle analyst recommendations."""
        log_operation_start("recommendations_analysis", ticker=ticker)

        try:
            # Fetch recommendations
            recommendations_result = self.data_service.get_recommendations(ticker)

            # Format and display results
            formatted_output = self.display_formatter.format_recommendations_display(
                recommendations_result
            )
            print(formatted_output)

            log_operation_end(
                "recommendations_analysis",
                recommendations_result.get("success", False),
                ticker=ticker,
            )

        except Exception as e:
            error_msg = self.display_formatter.format_error_message(e)
            print(error_msg)
            self.logger.error(f"Error in recommendations analysis: {e}")

    def _handle_peer_comparison(self, ticker: str) -> None:
        """Handle peer comparison analysis."""
        log_operation_start("peer_comparison_analysis", ticker=ticker)

        try:
            # Get suggested peers
            suggested_peers = self.data_service.suggest_peers_from_recommendations(
                ticker
            )

            # Get peer tickers from user
            peer_tickers = self.menu_handler.get_peer_tickers_input(suggested_peers)

            if not peer_tickers:
                print("No peers provided. Returning to main menu.")
                return

            # Fetch comparison data
            self.menu_handler.display_loading_message("Fetching data for comparison...")
            comparison_data_result = self.data_service.get_peer_comparison_data(
                ticker, peer_tickers
            )

            if not comparison_data_result["success"]:
                print(
                    f"Error: {comparison_data_result.get('error', 'Failed to fetch comparison data')}"
                )
                return

            # Perform comparison analysis
            comparison_result = self.comparison_analyzer.perform_peer_comparison(
                ticker, peer_tickers, comparison_data_result["data"]
            )

            # Format and display results
            formatted_output = self.display_formatter.format_comparison_display(
                comparison_result
            )
            print(formatted_output)

            log_operation_end(
                "peer_comparison_analysis",
                comparison_result.get("success", False),
                ticker=ticker,
            )

        except Exception as e:
            error_msg = self.display_formatter.format_error_message(e)
            print(error_msg)
            self.logger.error(f"Error in peer comparison analysis: {e}")


def main():
    """Main entry point for the application."""
    app = FinancialAnalysisApp()
    app.run()


if __name__ == "__main__":
    main()
