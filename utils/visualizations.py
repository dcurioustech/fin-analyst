"""
Text-based visualization utilities.
"""

from typing import Any, Dict, Union

import pandas as pd


def plot_text_bar(
    label: str, value: Union[int, float, None], max_value: Union[int, float, None]
) -> str:
    """
    Creates a simple text-based horizontal bar chart.

    Args:
        label: The label for the bar
        value: The value to plot
        max_value: The maximum value for scaling

    Returns:
        Formatted string representing the bar chart
    """
    if value is None or max_value is None or max_value == 0:
        return f"{label:<15} | N/A"

    bar_length = 40  # Max length of the bar in characters

    # Handle negative values by plotting on a scale from min to max
    scaled_value = float(value)

    # Calculate the length of the bar
    try:
        bar_fill_length = int((scaled_value / max_value) * bar_length)
    except (ValueError, TypeError):
        bar_fill_length = 0

    # Create the bar string
    bar = "█" * bar_fill_length

    # Format the value for display
    if isinstance(value, float):
        value_str = f"{value:.2f}"
    else:
        value_str = str(value)

    return f"{label:<15} | {bar} {value_str}"


def create_comparison_chart(data: Dict[str, Union[int, float]], title: str = "") -> str:
    """
    Creates a text-based comparison chart for multiple values.

    Args:
        data: Dictionary with labels as keys and values as values
        title: Optional title for the chart

    Returns:
        Formatted string representing the comparison chart
    """
    if not data:
        return "No data available for comparison."

    # Filter out None values and convert to numeric
    numeric_data = {}
    for label, value in data.items():
        if value is not None:
            try:
                numeric_data[label] = float(value)
            except (ValueError, TypeError):
                continue

    if not numeric_data:
        return "No valid numeric data available for comparison."

    # Find the maximum absolute value for scaling
    max_val = max(abs(v) for v in numeric_data.values())

    # Build the chart
    chart_lines = []
    if title:
        chart_lines.append(f"-- {title} --")

    for label, value in numeric_data.items():
        chart_lines.append(plot_text_bar(label, value, max_val))

    chart_lines.append("-" * 25)

    return "\n".join(chart_lines)


def create_metrics_visualization(metrics: Dict[str, Any]) -> str:
    """
    Creates a visualization for financial metrics.

    Args:
        metrics: Dictionary of metric names and values

    Returns:
        Formatted string representing the metrics visualization
    """
    if not metrics:
        return "No metrics available for visualization."

    # Group metrics by type for better visualization
    valuation_metrics = {}
    performance_metrics = {}

    for key, value in metrics.items():
        if any(
            term in key.lower()
            for term in ["pe", "pb", "ps", "price", "market", "enterprise"]
        ):
            valuation_metrics[key] = value
        elif any(
            term in key.lower() for term in ["margin", "return", "roe", "roa", "profit"]
        ):
            performance_metrics[key] = value

    result = []

    if valuation_metrics:
        result.append(create_comparison_chart(valuation_metrics, "Valuation Metrics"))
        result.append("")

    if performance_metrics:
        result.append(
            create_comparison_chart(performance_metrics, "Performance Metrics")
        )

    return "\n".join(result) if result else "No visualizable metrics found."


def format_dataframe_for_display(df: pd.DataFrame, max_width: int = 100) -> str:
    """
    Formats a pandas DataFrame for clean console display.

    Args:
        df: The DataFrame to format
        max_width: Maximum width for display

    Returns:
        Formatted string representation of the DataFrame
    """
    if df.empty:
        return "No data available."

    # Create a copy to avoid modifying the original
    display_df = df.copy()

    # Format numeric columns
    for col in display_df.columns:
        if display_df[col].dtype in ["float64", "int64"]:
            display_df[col] = display_df[col].apply(
                lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A"
            )

    return str(display_df)


def create_trend_visualization(
    values: list, labels: list = None, title: str = ""
) -> str:
    """
    Creates a simple trend visualization using text characters.

    Args:
        values: List of numeric values to plot
        labels: Optional list of labels for each value
        title: Optional title for the trend

    Returns:
        Formatted string representing the trend
    """
    if not values:
        return "No data available for trend visualization."

    # Filter out None values
    clean_values = [v for v in values if v is not None]
    if not clean_values:
        return "No valid data for trend visualization."

    result = []
    if title:
        result.append(f"-- {title} --")

    # Simple trend indicators
    if len(clean_values) >= 2:
        trend = (
            "↗"
            if clean_values[-1] > clean_values[0]
            else "↘" if clean_values[-1] < clean_values[0] else "→"
        )
        result.append(f"Trend: {trend}")

    # Show min, max, and latest values
    result.append(f"Min: {min(clean_values):.2f}")
    result.append(f"Max: {max(clean_values):.2f}")
    result.append(f"Latest: {clean_values[-1]:.2f}")

    return "\n".join(result)
