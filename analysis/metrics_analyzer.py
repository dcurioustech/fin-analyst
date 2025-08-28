"""
Financial metrics analysis functionality.
"""

import logging
from typing import Any, Dict, Optional

from utils.formatters import (format_large_number, format_percentage,
                              format_ratio)


class MetricsAnalyzer:
    """Analyzer for financial metrics and ratios."""

    def __init__(self):
        """Initialize the metrics analyzer."""
        self.logger = logging.getLogger(__name__)

    def analyze_valuation_metrics(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes valuation metrics for a company.

        Args:
            company_info: Raw company information

        Returns:
            Dictionary with valuation metrics
        """
        try:
            valuation_metrics = {
                "market_cap": company_info.get("marketCap"),
                "enterprise_value": company_info.get("enterpriseValue"),
                "trailing_pe": company_info.get("trailingPE"),
                "forward_pe": company_info.get("forwardPE"),
                "price_to_sales": company_info.get("priceToSalesTrailing12Months"),
                "price_to_book": company_info.get("priceToBook"),
                "peg_ratio": company_info.get("pegRatio"),
                "ev_to_revenue": company_info.get("enterpriseToRevenue"),
                "ev_to_ebitda": company_info.get("enterpriseToEbitda"),
            }

            return {"success": True, "data": valuation_metrics, "error": None}

        except Exception as e:
            self.logger.error(f"Error analyzing valuation metrics: {e}")
            return {
                "success": False,
                "data": None,
                "error": f"Failed to analyze valuation metrics: {str(e)}",
            }

    def analyze_profitability_metrics(
        self, company_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyzes profitability metrics for a company.

        Args:
            company_info: Raw company information

        Returns:
            Dictionary with profitability metrics
        """
        try:
            profitability_metrics = {
                "profit_margins": company_info.get("profitMargins"),
                "operating_margins": company_info.get("operatingMargins"),
                "gross_margins": company_info.get("grossMargins"),
                "return_on_equity": company_info.get("returnOnEquity"),
                "return_on_assets": company_info.get("returnOnAssets"),
                "return_on_investment": company_info.get("returnOnInvestment"),
                "revenue_growth": company_info.get("revenueGrowth"),
                "earnings_growth": company_info.get("earningsGrowth"),
            }

            return {"success": True, "data": profitability_metrics, "error": None}

        except Exception as e:
            self.logger.error(f"Error analyzing profitability metrics: {e}")
            return {
                "success": False,
                "data": None,
                "error": f"Failed to analyze profitability metrics: {str(e)}",
            }

    def analyze_stock_price_metrics(
        self, company_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyzes stock price related metrics.

        Args:
            company_info: Raw company information

        Returns:
            Dictionary with stock price metrics
        """
        try:
            price_metrics = {
                "current_price": company_info.get("currentPrice"),
                "previous_close": company_info.get("previousClose"),
                "open_price": company_info.get("open"),
                "day_low": company_info.get("dayLow"),
                "day_high": company_info.get("dayHigh"),
                "fifty_two_week_low": company_info.get("fiftyTwoWeekLow"),
                "fifty_two_week_high": company_info.get("fiftyTwoWeekHigh"),
                "fifty_day_average": company_info.get("fiftyDayAverage"),
                "two_hundred_day_average": company_info.get("twoHundredDayAverage"),
                "beta": company_info.get("beta"),
                "volume": company_info.get("volume"),
                "average_volume": company_info.get("averageVolume"),
            }

            # Calculate some derived metrics
            current_price = price_metrics["current_price"]
            fifty_two_week_low = price_metrics["fifty_two_week_low"]
            fifty_two_week_high = price_metrics["fifty_two_week_high"]

            if all([current_price, fifty_two_week_low, fifty_two_week_high]):
                # Calculate position in 52-week range
                range_position = (
                    (current_price - fifty_two_week_low)
                    / (fifty_two_week_high - fifty_two_week_low)
                ) * 100
                price_metrics["fifty_two_week_position_pct"] = range_position

            return {"success": True, "data": price_metrics, "error": None}

        except Exception as e:
            self.logger.error(f"Error analyzing stock price metrics: {e}")
            return {
                "success": False,
                "data": None,
                "error": f"Failed to analyze stock price metrics: {str(e)}",
            }

    def analyze_dividend_metrics(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes dividend related metrics.

        Args:
            company_info: Raw company information

        Returns:
            Dictionary with dividend metrics
        """
        try:
            dividend_metrics = {
                "dividend_yield": company_info.get("dividendYield"),
                "dividend_rate": company_info.get("dividendRate"),
                "payout_ratio": company_info.get("payoutRatio"),
                "ex_dividend_date": company_info.get("exDividendDate"),
                "last_dividend_value": company_info.get("lastDividendValue"),
                "last_dividend_date": company_info.get("lastDividendDate"),
                "five_year_avg_dividend_yield": company_info.get(
                    "fiveYearAvgDividendYield"
                ),
            }

            return {"success": True, "data": dividend_metrics, "error": None}

        except Exception as e:
            self.logger.error(f"Error analyzing dividend metrics: {e}")
            return {
                "success": False,
                "data": None,
                "error": f"Failed to analyze dividend metrics: {str(e)}",
            }

    def get_comprehensive_metrics(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gets comprehensive financial metrics analysis.

        Args:
            company_info: Raw company information

        Returns:
            Dictionary with all metrics categories
        """
        try:
            valuation = self.analyze_valuation_metrics(company_info)
            profitability = self.analyze_profitability_metrics(company_info)
            stock_price = self.analyze_stock_price_metrics(company_info)
            dividend = self.analyze_dividend_metrics(company_info)

            comprehensive_metrics = {
                "valuation": valuation["data"] if valuation["success"] else {},
                "profitability": (
                    profitability["data"] if profitability["success"] else {}
                ),
                "stock_price": stock_price["data"] if stock_price["success"] else {},
                "dividend": dividend["data"] if dividend["success"] else {},
            }

            return {"success": True, "data": comprehensive_metrics, "error": None}

        except Exception as e:
            self.logger.error(f"Error getting comprehensive metrics: {e}")
            return {
                "success": False,
                "data": None,
                "error": f"Failed to get comprehensive metrics: {str(e)}",
            }

    def format_metrics_for_display(self, metrics: Dict[str, Any]) -> str:
        """
        Formats metrics data for console display.

        Args:
            metrics: Metrics data from comprehensive analysis

        Returns:
            Formatted string for display
        """
        try:
            output_lines = []

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
                if prof_metrics.get("gross_margins"):
                    output_lines.append(
                        f"  Gross Margins: {format_percentage(prof_metrics['gross_margins'])}"
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

            return "\n".join(output_lines)

        except Exception as e:
            self.logger.error(f"Error formatting metrics for display: {e}")
            return "Error formatting metrics data"

    def calculate_financial_strength_score(
        self, metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculates a simple financial strength score based on key metrics.

        Args:
            metrics: Comprehensive metrics data

        Returns:
            Dictionary with financial strength analysis
        """
        try:
            score = 0
            max_score = 0
            factors = []

            # Check profitability metrics
            if "profitability" in metrics:
                prof = metrics["profitability"]

                # ROE > 15% is good
                if prof.get("return_on_equity"):
                    max_score += 20
                    if prof["return_on_equity"] > 0.15:
                        score += 20
                        factors.append("Strong ROE (>15%)")
                    elif prof["return_on_equity"] > 0.10:
                        score += 10
                        factors.append("Decent ROE (>10%)")

                # Profit margin > 10% is good
                if prof.get("profit_margins"):
                    max_score += 20
                    if prof["profit_margins"] > 0.10:
                        score += 20
                        factors.append("Strong profit margins (>10%)")
                    elif prof["profit_margins"] > 0.05:
                        score += 10
                        factors.append("Decent profit margins (>5%)")

            # Check valuation metrics
            if "valuation" in metrics:
                val = metrics["valuation"]

                # P/E ratio between 10-25 is reasonable
                if val.get("trailing_pe"):
                    max_score += 15
                    pe = val["trailing_pe"]
                    if 10 <= pe <= 25:
                        score += 15
                        factors.append("Reasonable P/E ratio (10-25)")
                    elif 5 <= pe <= 35:
                        score += 8
                        factors.append("Acceptable P/E ratio")

            # Check dividend metrics
            if "dividend" in metrics:
                div = metrics["dividend"]

                # Dividend yield > 2% is good for income
                if div.get("dividend_yield"):
                    max_score += 10
                    if div["dividend_yield"] > 0.02:
                        score += 10
                        factors.append("Pays dividends (>2% yield)")

            # Calculate final score
            if max_score > 0:
                final_score = int((score / max_score) * 100)
            else:
                final_score = 0

            return {
                "success": True,
                "data": {
                    "score": final_score,
                    "max_possible": 100,
                    "positive_factors": factors,
                    "interpretation": self._interpret_strength_score(final_score),
                },
                "error": None,
            }

        except Exception as e:
            self.logger.error(f"Error calculating financial strength score: {e}")
            return {
                "success": False,
                "data": None,
                "error": f"Failed to calculate financial strength score: {str(e)}",
            }

    def _interpret_strength_score(self, score: int) -> str:
        """
        Interprets the financial strength score.

        Args:
            score: The calculated score (0-100)

        Returns:
            String interpretation of the score
        """
        if score >= 80:
            return "Excellent financial strength"
        elif score >= 60:
            return "Good financial strength"
        elif score >= 40:
            return "Moderate financial strength"
        elif score >= 20:
            return "Below average financial strength"
        else:
            return "Poor financial strength"
