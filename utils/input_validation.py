"""
Input validation utilities for user inputs.
"""
import re
from typing import List, Optional, Dict, Any
import logging


class InputValidator:
    """Handles validation of various user inputs."""
    
    def __init__(self):
        """Initialize the input validator."""
        self.logger = logging.getLogger(__name__)
    
    def validate_ticker_list(self, tickers: List[str], max_count: int = 10) -> Dict[str, Any]:
        """
        Validates a list of ticker symbols.
        
        Args:
            tickers: List of ticker symbols to validate
            max_count: Maximum number of tickers allowed
            
        Returns:
            Dictionary with validation results
        """
        if not tickers:
            return {
                'valid': False,
                'error': 'No tickers provided',
                'valid_tickers': [],
                'invalid_tickers': []
            }
        
        valid_tickers = []
        invalid_tickers = []
        
        for ticker in tickers:
            if self.is_valid_ticker_format(ticker):
                valid_tickers.append(ticker.upper().strip())
            else:
                invalid_tickers.append(ticker)
        
        # Check count limit
        if len(valid_tickers) > max_count:
            excess_tickers = valid_tickers[max_count:]
            valid_tickers = valid_tickers[:max_count]
            self.logger.warning(f"Ticker count exceeded limit. Keeping first {max_count} tickers.")
        
        return {
            'valid': len(valid_tickers) > 0,
            'error': None if len(valid_tickers) > 0 else 'No valid tickers found',
            'valid_tickers': valid_tickers,
            'invalid_tickers': invalid_tickers,
            'excess_count': len(tickers) - max_count if len(tickers) > max_count else 0
        }
    
    def is_valid_ticker_format(self, ticker: str) -> bool:
        """
        Validates ticker symbol format.
        
        Args:
            ticker: Ticker symbol to validate
            
        Returns:
            True if valid format, False otherwise
        """
        if not ticker or not isinstance(ticker, str):
            return False
        
        ticker = ticker.strip().upper()
        
        # Basic format validation
        if len(ticker) < 1 or len(ticker) > 10:
            return False
        
        # Should contain only letters
        if not re.match(r'^[A-Z]+$', ticker):
            return False
        
        return True
    
    def validate_menu_input(self, choice: str, valid_range: tuple = (1, 9)) -> Dict[str, Any]:
        """
        Validates menu choice input.
        
        Args:
            choice: User's menu choice
            valid_range: Tuple of (min, max) valid choices
            
        Returns:
            Dictionary with validation results
        """
        if not choice:
            return {
                'valid': False,
                'error': 'No choice provided',
                'normalized_choice': None
            }
        
        choice = choice.strip()
        
        # Check if it's a number
        try:
            choice_num = int(choice)
            if valid_range[0] <= choice_num <= valid_range[1]:
                return {
                    'valid': True,
                    'error': None,
                    'normalized_choice': str(choice_num)
                }
            else:
                return {
                    'valid': False,
                    'error': f'Choice must be between {valid_range[0]} and {valid_range[1]}',
                    'normalized_choice': None
                }
        except ValueError:
            return {
                'valid': False,
                'error': 'Choice must be a number',
                'normalized_choice': None
            }
    
    def sanitize_string_input(self, input_str: str, max_length: int = 100) -> str:
        """
        Sanitizes string input by removing dangerous characters and limiting length.
        
        Args:
            input_str: Input string to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not input_str:
            return ""
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\';\\]', '', input_str)
        
        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
            self.logger.warning(f"Input truncated to {max_length} characters")
        
        return sanitized.strip()
    
    def validate_numeric_input(self, input_str: str, min_val: float = None, 
                             max_val: float = None) -> Dict[str, Any]:
        """
        Validates numeric input.
        
        Args:
            input_str: Input string to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            
        Returns:
            Dictionary with validation results
        """
        if not input_str or not input_str.strip():
            return {
                'valid': False,
                'error': 'No input provided',
                'value': None
            }
        
        try:
            value = float(input_str.strip())
            
            if min_val is not None and value < min_val:
                return {
                    'valid': False,
                    'error': f'Value must be at least {min_val}',
                    'value': None
                }
            
            if max_val is not None and value > max_val:
                return {
                    'valid': False,
                    'error': f'Value must be at most {max_val}',
                    'value': None
                }
            
            return {
                'valid': True,
                'error': None,
                'value': value
            }
            
        except ValueError:
            return {
                'valid': False,
                'error': 'Input must be a valid number',
                'value': None
            }
    
    def validate_yes_no_input(self, input_str: str) -> Dict[str, Any]:
        """
        Validates yes/no input.
        
        Args:
            input_str: Input string to validate
            
        Returns:
            Dictionary with validation results
        """
        if not input_str:
            return {
                'valid': False,
                'error': 'No input provided',
                'value': None
            }
        
        normalized = input_str.strip().lower()
        
        yes_values = ['y', 'yes', '1', 'true', 't']
        no_values = ['n', 'no', '0', 'false', 'f']
        
        if normalized in yes_values:
            return {
                'valid': True,
                'error': None,
                'value': True
            }
        elif normalized in no_values:
            return {
                'valid': True,
                'error': None,
                'value': False
            }
        else:
            return {
                'valid': False,
                'error': 'Please enter yes/no (y/n)',
                'value': None
            }


def create_input_validator() -> InputValidator:
    """
    Factory function to create an InputValidator instance.
    
    Returns:
        InputValidator instance
    """
    return InputValidator()