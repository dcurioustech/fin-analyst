"""
Application configuration and settings.
"""
import pandas as pd
import logging
from typing import Dict, Any, Optional
import os


# Application metadata
APP_NAME = "Financial Analysis Bot"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Modular financial analysis application"

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'suppress_external': ['yfinance', 'urllib3', 'requests']
}

# Pandas display options
PANDAS_DISPLAY_OPTIONS = {
    'display.max_rows': 500,
    'display.max_columns': 500,
    'display.width': 1000,
    'display.float_format': '{:.2f}'.format
}

# Analysis configuration
COMPARISON_METRICS = {
    'marketCap': 'Market Cap',
    'trailingPE': 'P/E Ratio',
    'priceToSalesTrailing12Months': 'P/S Ratio',
    'priceToBook': 'P/B Ratio',
    'profitMargins': 'Profit Margin (%)',
    'returnOnEquity': 'ROE (%)'
}

# Data service configuration
DATA_SERVICE_CONFIG = {
    'default_timeout': 30,
    'max_retries': 3,
    'retry_delay': 1.0,
    'validate_tickers': True,
    'cache_enabled': False  # Future enhancement
}

# UI configuration
MENU_OPTIONS = {
    'main_menu': [
        "1: Company Profile & Summary",
        "2: Key Financial Metrics & Ratios", 
        "3: Income Statement (Annual)",
        "4: Balance Sheet (Annual)",
        "5: Cash Flow Statement (Annual)",
        "6: Analyst Recommendations",
        "7: Peer Comparison with Visuals",
        "8: Search for a new ticker",
        "9: Exit"
    ],
    'analysis_menu': [
        "What analysis would you like to see?",
        "Please enter your choice (1-9): "
    ]
}

# Input validation configuration
VALIDATION_CONFIG = {
    'max_ticker_length': 10,
    'min_ticker_length': 1,
    'max_peer_count': 10,
    'max_input_attempts': 3,
    'ticker_pattern': r'^[A-Z]+$'
}

# Error handling configuration
ERROR_CONFIG = {
    'show_detailed_errors': False,  # Set to True for debugging
    'log_errors': True,
    'retry_on_network_error': True,
    'graceful_degradation': True
}


class ConfigurationManager:
    """Manages application configuration and settings."""
    
    def __init__(self):
        """Initialize configuration manager."""
        self.logger = logging.getLogger(__name__)
        self._config_loaded = False
    
    def load_configuration(self) -> Dict[str, Any]:
        """
        Load and validate all configuration settings.
        
        Returns:
            Dictionary containing all configuration settings
        """
        try:
            config = {
                'app': {
                    'name': APP_NAME,
                    'version': APP_VERSION,
                    'description': APP_DESCRIPTION
                },
                'logging': LOGGING_CONFIG,
                'pandas': PANDAS_DISPLAY_OPTIONS,
                'comparison_metrics': COMPARISON_METRICS,
                'data_service': DATA_SERVICE_CONFIG,
                'ui': MENU_OPTIONS,
                'validation': VALIDATION_CONFIG,
                'error_handling': ERROR_CONFIG
            }
            
            # Validate configuration
            self._validate_configuration(config)
            
            self._config_loaded = True
            self.logger.info("Configuration loaded and validated successfully")
            
            return config
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            raise
    
    def _validate_configuration(self, config: Dict[str, Any]) -> None:
        """
        Validate configuration settings.
        
        Args:
            config: Configuration dictionary to validate
        """
        # Validate required sections
        required_sections = ['app', 'logging', 'pandas', 'ui']
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required configuration section: {section}")
        
        # Validate specific settings
        if config['validation']['max_ticker_length'] < config['validation']['min_ticker_length']:
            raise ValueError("max_ticker_length must be >= min_ticker_length")
        
        if config['validation']['max_peer_count'] < 1:
            raise ValueError("max_peer_count must be at least 1")
        
        if config['data_service']['max_retries'] < 0:
            raise ValueError("max_retries must be non-negative")
    
    def get_setting(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a specific configuration setting.
        
        Args:
            section: Configuration section name
            key: Setting key
            default: Default value if setting not found
            
        Returns:
            Configuration value or default
        """
        if not self._config_loaded:
            config = self.load_configuration()
        else:
            config = self.load_configuration()  # Reload for consistency
        
        return config.get(section, {}).get(key, default)
    
    def update_setting(self, section: str, key: str, value: Any) -> None:
        """
        Update a configuration setting (runtime only).
        
        Args:
            section: Configuration section name
            key: Setting key
            value: New value
        """
        # This would update runtime configuration
        # In a full implementation, this might also persist changes
        self.logger.info(f"Updated setting {section}.{key} = {value}")


def configure_pandas() -> None:
    """Configure pandas display options."""
    try:
        for option, value in PANDAS_DISPLAY_OPTIONS.items():
            pd.set_option(option, value)
        logging.getLogger(__name__).info("Pandas configuration applied successfully")
    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to configure pandas: {e}")


def get_app_info() -> Dict[str, str]:
    """
    Get application information.
    
    Returns:
        Dictionary with app name, version, and description
    """
    return {
        'name': APP_NAME,
        'version': APP_VERSION,
        'description': APP_DESCRIPTION
    }


def load_environment_overrides() -> Dict[str, Any]:
    """
    Load configuration overrides from environment variables.
    
    Returns:
        Dictionary with environment-based configuration overrides
    """
    overrides = {}
    
    # Check for common environment variables
    if os.getenv('FIN_ANALYST_LOG_LEVEL'):
        overrides['logging_level'] = os.getenv('FIN_ANALYST_LOG_LEVEL')
    
    if os.getenv('FIN_ANALYST_TIMEOUT'):
        try:
            overrides['timeout'] = int(os.getenv('FIN_ANALYST_TIMEOUT'))
        except ValueError:
            logging.getLogger(__name__).warning("Invalid timeout value in environment")
    
    if os.getenv('FIN_ANALYST_DEBUG'):
        overrides['debug_mode'] = os.getenv('FIN_ANALYST_DEBUG').lower() in ['true', '1', 'yes']
    
    return overrides


# Global configuration manager instance
config_manager = ConfigurationManager()