"""
Error handling utilities and logging configuration.
"""
import logging
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from functools import wraps


class ErrorResponse:
    """Standardized error response format."""
    
    def __init__(self, error_type: str, message: str, details: Dict[str, Any] = None):
        """
        Initialize error response.
        
        Args:
            error_type: Type of error (e.g., 'DATA_ACCESS', 'VALIDATION', 'NETWORK')
            message: Human-readable error message
            details: Optional additional error details
        """
        self.error_type = error_type
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error response to dictionary format."""
        return {
            'success': False,
            'error_type': self.error_type,
            'error': self.message,
            'details': self.details,
            'timestamp': self.timestamp.isoformat(),
            'data': None
        }


def setup_logging(log_level: str = 'INFO') -> None:
    """
    Set up logging configuration for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    root_logger.addHandler(console_handler)
    
    # Suppress yfinance debug messages
    logging.getLogger('yfinance').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)


def handle_api_error(func):
    """
    Decorator for handling API-related errors.
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function with error handling
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError as e:
            logger = logging.getLogger(func.__module__)
            logger.error(f"Network connection error in {func.__name__}: {e}")
            return ErrorResponse(
                'NETWORK_ERROR',
                'Network connection failed. Please check your internet connection.',
                {'original_error': str(e)}
            ).to_dict()
        except TimeoutError as e:
            logger = logging.getLogger(func.__module__)
            logger.error(f"Timeout error in {func.__name__}: {e}")
            return ErrorResponse(
                'TIMEOUT_ERROR',
                'Request timed out. Please try again later.',
                {'original_error': str(e)}
            ).to_dict()
        except Exception as e:
            logger = logging.getLogger(func.__module__)
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            return ErrorResponse(
                'UNEXPECTED_ERROR',
                f'An unexpected error occurred: {str(e)}',
                {'original_error': str(e)}
            ).to_dict()
    
    return wrapper


def handle_data_validation_error(func):
    """
    Decorator for handling data validation errors.
    
    Args:
        func: Function to wrap
        
    Returns:
        Wrapped function with validation error handling
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger = logging.getLogger(func.__module__)
            logger.warning(f"Data validation error in {func.__name__}: {e}")
            return ErrorResponse(
                'VALIDATION_ERROR',
                f'Invalid data provided: {str(e)}',
                {'original_error': str(e)}
            ).to_dict()
        except KeyError as e:
            logger = logging.getLogger(func.__module__)
            logger.warning(f"Missing required data in {func.__name__}: {e}")
            return ErrorResponse(
                'MISSING_DATA_ERROR',
                f'Required data is missing: {str(e)}',
                {'original_error': str(e)}
            ).to_dict()
        except Exception as e:
            logger = logging.getLogger(func.__module__)
            logger.error(f"Unexpected error in {func.__name__}: {e}")
            return ErrorResponse(
                'UNEXPECTED_ERROR',
                f'An unexpected error occurred: {str(e)}',
                {'original_error': str(e)}
            ).to_dict()
    
    return wrapper


def safe_execute(func, default_return=None, error_message="Operation failed"):
    """
    Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        default_return: Default value to return on error
        error_message: Custom error message
        
    Returns:
        Function result or default_return on error
    """
    try:
        return func()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"{error_message}: {e}")
        return default_return


def validate_ticker_symbol(ticker: str) -> bool:
    """
    Validates ticker symbol format.
    
    Args:
        ticker: Ticker symbol to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not ticker or not isinstance(ticker, str):
        return False
    
    ticker = ticker.strip().upper()
    
    # Basic validation rules
    if len(ticker) < 1 or len(ticker) > 10:
        return False
    
    if not ticker.isalpha():
        return False
    
    return True


def create_success_response(data: Any, message: str = None) -> Dict[str, Any]:
    """
    Creates a standardized success response.
    
    Args:
        data: Response data
        message: Optional success message
        
    Returns:
        Standardized success response dictionary
    """
    response = {
        'success': True,
        'data': data,
        'error': None,
        'timestamp': datetime.now().isoformat()
    }
    
    if message:
        response['message'] = message
    
    return response


def log_operation_start(operation: str, **kwargs) -> None:
    """
    Logs the start of an operation.
    
    Args:
        operation: Name of the operation
        **kwargs: Additional context to log
    """
    logger = logging.getLogger(__name__)
    context = ', '.join([f"{k}={v}" for k, v in kwargs.items()])
    logger.info(f"Starting {operation}" + (f" with {context}" if context else ""))


def log_operation_end(operation: str, success: bool, **kwargs) -> None:
    """
    Logs the end of an operation.
    
    Args:
        operation: Name of the operation
        success: Whether the operation was successful
        **kwargs: Additional context to log
    """
    logger = logging.getLogger(__name__)
    status = "successfully" if success else "with errors"
    context = ', '.join([f"{k}={v}" for k, v in kwargs.items()])
    logger.info(f"Completed {operation} {status}" + (f" - {context}" if context else ""))


class RetryHandler:
    """Handles retry logic for operations that may fail temporarily."""
    
    def __init__(self, max_retries: int = 3, delay: float = 1.0):
        """
        Initialize retry handler.
        
        Args:
            max_retries: Maximum number of retry attempts
            delay: Delay between retries in seconds
        """
        self.max_retries = max_retries
        self.delay = delay
        self.logger = logging.getLogger(__name__)
    
    def execute_with_retry(self, func, *args, **kwargs):
        """
        Execute function with retry logic.
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result or raises last exception
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    self.logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {self.delay}s...")
                    import time
                    time.sleep(self.delay)
                else:
                    self.logger.error(f"All {self.max_retries + 1} attempts failed. Last error: {e}")
        
        raise last_exception