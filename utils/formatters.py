"""
Utility functions for number and text formatting.
"""

from typing import Any, Union


def format_large_number(num: Union[int, float, None]) -> str:
    """
    Formats a large number into a more readable string (e.g., 1.25 T, 350.50 B, 15.75 M).

    Args:
        num: The number to format

    Returns:
        Formatted string representation of the number
    """
    if num is None or not isinstance(num, (int, float)):
        return "N/A"
    if abs(num) > 1e12:
        return f"{num / 1e12:.2f} T"
    elif abs(num) > 1e9:
        return f"{num / 1e9:.2f} B"
    elif abs(num) > 1e6:
        return f"{num / 1e6:.2f} M"
    else:
        return f"{num:,.2f}"


def format_percentage(num: Union[int, float, None]) -> str:
    """
    Formats a number as a percentage.

    Args:
        num: The number to format as percentage (should be in decimal form, e.g., 0.15 for 15%)

    Returns:
        Formatted percentage string
    """
    if num is None or not isinstance(num, (int, float)):
        return "N/A"
    return f"{num * 100:.2f}%"


def format_currency(num: Union[int, float, None], currency_symbol: str = "$") -> str:
    """
    Formats a number as currency.

    Args:
        num: The number to format as currency
        currency_symbol: The currency symbol to use

    Returns:
        Formatted currency string
    """
    if num is None or not isinstance(num, (int, float)):
        return "N/A"
    return f"{currency_symbol}{num:,.2f}"


def safe_format_number(num: Any, decimal_places: int = 2) -> str:
    """
    Safely formats any value as a number, handling None and non-numeric values gracefully.

    Args:
        num: The value to format
        decimal_places: Number of decimal places to show

    Returns:
        Formatted number string or "N/A" if not a valid number
    """
    if num is None:
        return "N/A"

    try:
        if isinstance(num, (int, float)):
            if decimal_places == 0:
                return f"{num:,.0f}"
            else:
                return f"{num:,.{decimal_places}f}"
        else:
            # Try to convert to float
            float_val = float(num)
            if decimal_places == 0:
                return f"{float_val:,.0f}"
            else:
                return f"{float_val:,.{decimal_places}f}"
    except (ValueError, TypeError):
        return "N/A"


def format_ratio(num: Union[int, float, None], suffix: str = "") -> str:
    """
    Formats a financial ratio with appropriate decimal places.

    Args:
        num: The ratio to format
        suffix: Optional suffix to append

    Returns:
        Formatted ratio string
    """
    if num is None or not isinstance(num, (int, float)):
        return "N/A"

    formatted = f"{num:.2f}"
    if suffix:
        formatted += f" {suffix}"
    return formatted
