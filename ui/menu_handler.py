"""
Menu handling and user interaction functionality.
"""

import logging
import sys
from typing import Any, Dict, List, Optional

from config.settings import MENU_OPTIONS
from utils.error_handling import RetryHandler, validate_ticker_symbol


class MenuHandler:
    """Handles user interface interactions and menu navigation."""

    def __init__(self):
        """Initialize the menu handler."""
        self.logger = logging.getLogger(__name__)

    def display_main_menu(self) -> None:
        """Displays the main analysis menu options."""
        print("\nWhat analysis would you like to see?")
        for option in MENU_OPTIONS["main_menu"]:
            print(option)

    def display_analysis_menu(self) -> None:
        """Displays the analysis menu with all available options."""
        self.display_main_menu()

    def get_user_choice(
        self, options: List[str], prompt: str = "Please enter your choice: "
    ) -> str:
        """
        Gets user choice from a list of options.

        Args:
            options: List of available options
            prompt: Prompt message to display

        Returns:
            User's choice as string
        """
        try:
            choice = input(prompt).strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            return "exit"
        except Exception as e:
            self.logger.error(f"Error getting user choice: {e}")
            return ""

    def get_ticker_input(
        self,
        prompt: str = "Enter a stock ticker (e.g., AAPL, GOOGL) or type 'exit' to quit: ",
    ) -> str:
        """
        Gets ticker symbol input from user with validation.

        Args:
            prompt: Prompt message to display

        Returns:
            Validated ticker symbol in uppercase, or 'EXIT' to quit
        """
        max_attempts = 3
        attempt = 0

        while attempt < max_attempts:
            try:
                ticker = input(prompt).strip().upper()

                if ticker == "EXIT":
                    return "EXIT"

                # Enhanced ticker validation
                if not ticker:
                    print("Please enter a valid ticker symbol.")
                    attempt += 1
                    continue

                if not validate_ticker_symbol(ticker):
                    print(
                        "Invalid ticker format. Ticker should be 1-10 letters only (e.g., AAPL, MSFT)."
                    )
                    attempt += 1
                    continue

                return ticker

            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                return "EXIT"
            except Exception as e:
                self.logger.error(f"Error getting ticker input: {e}")
                print("An error occurred while processing input. Please try again.")
                attempt += 1

        print(f"Maximum attempts ({max_attempts}) reached. Please try again later.")
        return ""

    def get_peer_tickers_input(self, suggested_peers: List[str] = None) -> List[str]:
        """
        Gets peer ticker symbols from user input with validation.

        Args:
            suggested_peers: Optional list of suggested peer tickers

        Returns:
            List of validated peer ticker symbols
        """
        try:
            if suggested_peers:
                print(
                    f"Suggested peers from Yahoo Finance: {', '.join(suggested_peers)}"
                )

            peer_input = input(
                "Enter peer tickers separated by spaces (or press Enter to use suggestions): "
            ).strip()

            if peer_input:
                # Parse and validate user input
                raw_peers = [
                    ticker.strip().upper()
                    for ticker in peer_input.split()
                    if ticker.strip()
                ]
                valid_peers = []
                invalid_peers = []

                for ticker in raw_peers:
                    if validate_ticker_symbol(ticker):
                        valid_peers.append(ticker)
                    else:
                        invalid_peers.append(ticker)

                if invalid_peers:
                    print(
                        f"Warning: Invalid ticker symbols ignored: {', '.join(invalid_peers)}"
                    )

                if not valid_peers:
                    print("No valid peer tickers provided.")
                    return []

                if len(valid_peers) > 10:
                    print(
                        f"Too many peers provided. Using first 10: {', '.join(valid_peers[:10])}"
                    )
                    return valid_peers[:10]

                return valid_peers

            elif suggested_peers:
                # Validate suggested peers as well
                valid_suggested = [
                    p for p in suggested_peers if validate_ticker_symbol(p)
                ]
                if len(valid_suggested) != len(suggested_peers):
                    print("Some suggested peers were invalid and filtered out.")
                return valid_suggested
            else:
                print("No peers provided.")
                return []

        except (EOFError, KeyboardInterrupt):
            print("\nExiting peer selection...")
            return []
        except Exception as e:
            self.logger.error(f"Error getting peer tickers input: {e}")
            print("An error occurred while processing peer input. Please try again.")
            return []

    def handle_menu_navigation(self, ticker_symbol: str) -> str:
        """
        Handles the main menu navigation for a given ticker.

        Args:
            ticker_symbol: The ticker symbol being analyzed

        Returns:
            User's menu choice
        """
        try:
            self.display_analysis_menu()
            choice = self.get_user_choice(
                MENU_OPTIONS["main_menu"], "Please enter your choice (1-9): "
            )

            return choice

        except Exception as e:
            self.logger.error(f"Error handling menu navigation: {e}")
            return ""

    def validate_menu_choice(
        self, choice: str, valid_choices: List[str] = None
    ) -> bool:
        """
        Validates if a menu choice is valid.

        Args:
            choice: User's choice
            valid_choices: List of valid choices (defaults to 1-9)

        Returns:
            True if choice is valid, False otherwise
        """
        if valid_choices is None:
            valid_choices = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        return choice.strip() in valid_choices

    def get_validated_menu_choice(self, max_attempts: int = 3) -> str:
        """
        Gets a validated menu choice from user with retry logic.

        Args:
            max_attempts: Maximum number of attempts

        Returns:
            Valid menu choice or empty string if max attempts reached
        """
        valid_choices = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        attempt = 0

        while attempt < max_attempts:
            choice = self.get_user_choice(
                valid_choices, "Please enter your choice (1-9): "
            )

            if choice.upper() == "EXIT":
                return "9"  # Map exit to menu option 9

            if self.validate_menu_choice(choice, valid_choices):
                return choice

            self.handle_invalid_choice(choice)
            attempt += 1

        print(f"Maximum attempts ({max_attempts}) reached. Returning to main menu.")
        return ""

    def display_error_message(self, message: str) -> None:
        """
        Displays an error message to the user.

        Args:
            message: Error message to display
        """
        print(f"Error: {message}")

    def display_success_message(self, message: str) -> None:
        """
        Displays a success message to the user.

        Args:
            message: Success message to display
        """
        print(f"✓ {message}")

    def display_info_message(self, message: str) -> None:
        """
        Displays an informational message to the user.

        Args:
            message: Info message to display
        """
        print(f"ℹ {message}")

    def confirm_action(self, message: str) -> bool:
        """
        Asks user for confirmation of an action.

        Args:
            message: Confirmation message

        Returns:
            True if user confirms, False otherwise
        """
        try:
            response = input(f"{message} (y/n): ").strip().lower()
            return response in ["y", "yes", "1", "true"]
        except (EOFError, KeyboardInterrupt):
            return False
        except Exception as e:
            self.logger.error(f"Error getting confirmation: {e}")
            return False

    def display_loading_message(self, message: str) -> None:
        """
        Displays a loading message and flushes output.

        Args:
            message: Loading message to display
        """
        print(message)
        sys.stdout.flush()  # Ensure print appears immediately

    def get_analysis_choice_handler(self) -> Dict[str, str]:
        """
        Returns a mapping of menu choices to their corresponding actions.

        Returns:
            Dictionary mapping choice numbers to action names
        """
        return {
            "1": "company_profile",
            "2": "key_metrics",
            "3": "income_statement",
            "4": "balance_sheet",
            "5": "cash_flow",
            "6": "recommendations",
            "7": "peer_comparison",
            "8": "new_ticker",
            "9": "exit",
        }

    def handle_invalid_choice(self, choice: str) -> None:
        """
        Handles invalid menu choices.

        Args:
            choice: The invalid choice entered by user
        """
        print(f"Invalid choice '{choice}'. Please enter a number between 1 and 9.")

    def display_ticker_info(self, ticker: str, company_name: str) -> None:
        """
        Displays ticker information after successful data fetch.

        Args:
            ticker: Ticker symbol
            company_name: Company name
        """
        print(f"\nSuccessfully fetched data for {company_name} ({ticker}).")

    def handle_ticker_validation_error(self, ticker: str) -> None:
        """
        Handles ticker validation errors.

        Args:
            ticker: The invalid ticker symbol
        """
        print(
            f"Error: Could not find data for ticker '{ticker}'. Please check the symbol and try again."
        )

    def display_exit_message(self) -> None:
        """Displays exit message when user quits the application."""
        print("Exiting analysis bot. Goodbye!")

    def get_retry_choice(self, error_message: str) -> bool:
        """
        Asks user if they want to retry after an error.

        Args:
            error_message: The error that occurred

        Returns:
            True if user wants to retry, False otherwise
        """
        print(f"An error occurred: {error_message}")
        return self.confirm_action("Would you like to try again?")

    def display_section_header(self, title: str) -> None:
        """
        Displays a formatted section header.

        Args:
            title: Title of the section
        """
        print(f"\n--- {title} ---")

    def display_section_footer(self, title: str) -> None:
        """
        Displays a formatted section footer.

        Args:
            title: Title of the section
        """
        print("-" * (len(title) + 8))
