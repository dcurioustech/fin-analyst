"""
Analysis/Functional Tools Layer for Financial Analysis.

This module provides tools that wrap existing analysis functions for use
by the LangGraph orchestrator. Tools are organized by functionality and
provide structured data for the orchestrator to consume.
"""

import logging
from typing import Any, Dict, List, Optional

from langchain.tools import tool

from analysis.company_analyzer import CompanyAnalyzer
from analysis.comparison_analyzer import ComparisonAnalyzer
from analysis.metrics_analyzer import MetricsAnalyzer
from analysis.statement_analyzer import StatementAnalyzer

# Import our existing services and analyzers
from services.financial_data_service import FinancialDataService

# Initialize services and analyzers
data_service = FinancialDataService()
company_analyzer = CompanyAnalyzer()
metrics_analyzer = MetricsAnalyzer()
statement_analyzer = StatementAnalyzer()
comparison_analyzer = ComparisonAnalyzer()

logger = logging.getLogger(__name__)


# =============================================================================
# DATA SERVICE INTERFACE TOOLS
# =============================================================================


@tool
def get_company_data(ticker: str) -> Dict[str, Any]:
    """
    Fetch comprehensive company data for analysis.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')

    Returns:
        Dictionary containing company data or error details
    """
    try:
        logger.info(f"Fetching company data for {ticker}")
        result = data_service.get_company_info(ticker)
        return result
    except Exception as e:
        logger.error(f"Error fetching company data for {ticker}: {e}")
        return {"success": False, "error": str(e), "tool": "get_company_data"}


# =============================================================================
# ANALYSIS FUNCTION TOOLS
# =============================================================================


@tool
def analyze_company_profile(
    ticker: str, company_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Analyze company profile and basic information.

    Args:
        ticker: Stock ticker symbol
        company_data: Optional pre-fetched company data

    Returns:
        Dictionary containing company profile analysis
    """
    try:
        logger.info(f"Analyzing company profile for {ticker}")

        # Use provided data or fetch if not available
        if company_data is None:
            company_data_result = data_service.get_company_info(ticker)
            if not company_data_result["success"]:
                return company_data_result
            company_data = company_data_result["data"]

        # Analyze profile
        profile_result = company_analyzer.analyze_company_profile(company_data)
        profile_result["tool"] = "analyze_company_profile"
        return profile_result

    except Exception as e:
        logger.error(f"Error analyzing company profile for {ticker}: {e}")
        return {"success": False, "error": str(e), "tool": "analyze_company_profile"}


@tool
def analyze_financial_metrics(
    ticker: str, company_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Analyze comprehensive financial metrics for a company.

    Args:
        ticker: Stock ticker symbol
        company_data: Optional pre-fetched company data

    Returns:
        Dictionary containing financial metrics analysis
    """
    try:
        logger.info(f"Analyzing financial metrics for {ticker}")

        # Use provided data or fetch if not available
        if company_data is None:
            company_data_result = data_service.get_company_info(ticker)
            if not company_data_result["success"]:
                return company_data_result
            company_data = company_data_result["data"]

        # Analyze metrics
        metrics_result = metrics_analyzer.get_comprehensive_metrics(company_data)
        metrics_result["tool"] = "analyze_financial_metrics"
        return metrics_result

    except Exception as e:
        logger.error(f"Error analyzing financial metrics for {ticker}: {e}")
        return {"success": False, "error": str(e), "tool": "analyze_financial_metrics"}


@tool
def analyze_financial_statements(
    ticker: str, statement_type: str, statements_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Analyze a specific financial statement for a company.

    Args:
        ticker: Stock ticker symbol
        statement_type: Type of statement ('income_statement', 'balance_sheet', 'cash_flow')
        statements_data: Optional pre-fetched statements data

    Returns:
        Dictionary containing financial statement analysis
    """
    try:
        logger.info(f"Analyzing {statement_type} for {ticker}")

        # Use provided data or fetch if not available
        if statements_data is None:
            statements_result = data_service.get_financial_statements(ticker)
            if not statements_result["success"]:
                return statements_result
            statements_data = statements_result["data"]

        # Get specific statement
        statement_data = statements_data.get(statement_type)
        if statement_data is None:
            return {
                "success": False,
                "error": f"No {statement_type} data available",
                "tool": "analyze_financial_statements",
            }

        # Analyze statement
        if statement_type == "income_statement":
            analysis_result = statement_analyzer.process_income_statement(
                statement_data
            )
        elif statement_type == "balance_sheet":
            analysis_result = statement_analyzer.process_balance_sheet(statement_data)
        elif statement_type == "cash_flow":
            analysis_result = statement_analyzer.process_cash_flow(statement_data)
        else:
            return {
                "success": False,
                "error": f"Unknown statement type: {statement_type}",
                "tool": "analyze_financial_statements",
            }

        analysis_result["tool"] = "analyze_financial_statements"
        return analysis_result

    except Exception as e:
        logger.error(f"Error analyzing {statement_type} for {ticker}: {e}")
        return {
            "success": False,
            "error": str(e),
            "tool": "analyze_financial_statements",
        }


@tool
def compare_companies(
    main_ticker: str, peer_tickers: List[str], comparison_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Compare a main company with peer companies.

    Args:
        main_ticker: Main company ticker symbol
        peer_tickers: List of peer company ticker symbols
        comparison_data: Optional pre-fetched comparison data

    Returns:
        Dictionary containing comparison analysis
    """
    try:
        logger.info(f"Comparing {main_ticker} with peers: {peer_tickers}")

        # Use provided data or fetch if not available
        if comparison_data is None:
            comparison_data_result = data_service.get_peer_comparison_data(
                main_ticker, peer_tickers
            )
            if not comparison_data_result["success"]:
                return comparison_data_result
            comparison_data = comparison_data_result["data"]

        # Perform comparison analysis
        comparison_result = comparison_analyzer.perform_peer_comparison(
            main_ticker, peer_tickers, comparison_data
        )

        comparison_result["tool"] = "compare_companies"
        return comparison_result

    except Exception as e:
        logger.error(f"Error comparing companies: {e}")
        return {"success": False, "error": str(e), "tool": "compare_companies"}


# =============================================================================
# SPECIALIZED ANALYSIS TOOLS
# =============================================================================


@tool
def get_analyst_recommendations(ticker: str) -> Dict[str, Any]:
    """
    Get analyst recommendations for a company.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Dictionary containing analyst recommendations
    """
    try:
        logger.info(f"Getting analyst recommendations for {ticker}")
        result = data_service.get_recommendations(ticker)
        result["tool"] = "get_analyst_recommendations"
        return result

    except Exception as e:
        logger.error(f"Error getting recommendations for {ticker}: {e}")
        return {
            "success": False,
            "error": str(e),
            "tool": "get_analyst_recommendations",
        }


@tool
def analyze_income_statement(
    ticker: str, statements_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Analyze income statement specifically.

    Args:
        ticker: Stock ticker symbol
        statements_data: Optional pre-fetched statements data

    Returns:
        Dictionary containing income statement analysis
    """
    return analyze_financial_statements(ticker, "income_statement", statements_data)


@tool
def analyze_balance_sheet(
    ticker: str, statements_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Analyze balance sheet specifically.

    Args:
        ticker: Stock ticker symbol
        statements_data: Optional pre-fetched statements data

    Returns:
        Dictionary containing balance sheet analysis
    """
    return analyze_financial_statements(ticker, "balance_sheet", statements_data)


@tool
def analyze_cash_flow(
    ticker: str, statements_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Analyze cash flow statement specifically.

    Args:
        ticker: Stock ticker symbol
        statements_data: Optional pre-fetched statements data

    Returns:
        Dictionary containing cash flow analysis
    """
    return analyze_financial_statements(ticker, "cash_flow", statements_data)


@tool
def validate_ticker(ticker: str) -> Dict[str, Any]:
    """
    Validate if a ticker symbol is valid and accessible.

    Args:
        ticker: Stock ticker symbol to validate

    Returns:
        Dictionary with validation result
    """
    try:
        logger.info(f"Validating ticker: {ticker}")
        is_valid = data_service.validate_ticker(ticker)
        return {
            "success": True,
            "valid": is_valid,
            "ticker": ticker.upper(),
            "tool": "validate_ticker",
        }

    except Exception as e:
        logger.error(f"Error validating ticker {ticker}: {e}")
        return {"success": False, "error": str(e), "tool": "validate_ticker"}


@tool
def get_peer_suggestions(ticker: str) -> Dict[str, Any]:
    """
    Get suggested peer companies for comparison analysis.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Dictionary containing suggested peer companies
    """
    try:
        logger.info(f"Getting peer suggestions for {ticker}")
        suggested_peers = data_service.suggest_peers_from_recommendations(ticker)
        return {
            "success": True,
            "ticker": ticker,
            "suggested_peers": suggested_peers,
            "tool": "get_peer_suggestions",
        }

    except Exception as e:
        logger.error(f"Error getting peer suggestions for {ticker}: {e}")
        return {"success": False, "error": str(e), "tool": "get_peer_suggestions"}


@tool
def get_financial_statements_data(ticker: str) -> Dict[str, Any]:
    """
    Fetch financial statements data for a company.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Dictionary containing financial statements data
    """
    try:
        logger.info(f"Fetching financial statements for {ticker}")
        result = data_service.get_financial_statements(ticker)
        return result

    except Exception as e:
        logger.error(f"Error fetching financial statements for {ticker}: {e}")
        return {
            "success": False,
            "error": str(e),
            "tool": "get_financial_statements_data",
        }


@tool
def get_peer_comparison_data(
    main_ticker: str, peer_tickers: List[str]
) -> Dict[str, Any]:
    """
    Fetch data for peer comparison analysis.

    Args:
        main_ticker: Main company ticker symbol
        peer_tickers: List of peer company ticker symbols

    Returns:
        Dictionary containing comparison data
    """
    try:
        logger.info(f"Fetching peer comparison data: {main_ticker} vs {peer_tickers}")
        result = data_service.get_peer_comparison_data(main_ticker, peer_tickers)
        return result

    except Exception as e:
        logger.error(f"Error fetching peer comparison data: {e}")
        return {"success": False, "error": str(e), "tool": "get_peer_comparison_data"}


# =============================================================================
# TOOL COLLECTIONS FOR ORCHESTRATOR
# =============================================================================

# Data service interface tools
DATA_SERVICE_TOOLS = [
    get_company_data,
    validate_ticker,
    get_peer_suggestions,
    get_financial_statements_data,
    get_peer_comparison_data,
]

# Analysis function tools
ANALYSIS_TOOLS = [
    analyze_company_profile,
    analyze_financial_metrics,
    analyze_financial_statements,
    compare_companies,
]

# Specialized analysis tools
SPECIALIZED_TOOLS = [
    get_analyst_recommendations,
    analyze_income_statement,
    analyze_balance_sheet,
    analyze_cash_flow,
]

# All available tools for the orchestrator
ALL_FINANCIAL_TOOLS = DATA_SERVICE_TOOLS + ANALYSIS_TOOLS + SPECIALIZED_TOOLS

# Tool mapping for easy access by name
TOOL_MAP = {
    # Data service tools
    "get_company_data": get_company_data,
    "validate_ticker": validate_ticker,
    "get_peer_suggestions": get_peer_suggestions,
    "get_financial_statements_data": get_financial_statements_data,
    "get_peer_comparison_data": get_peer_comparison_data,
    # Analysis tools
    "analyze_company_profile": analyze_company_profile,
    "analyze_financial_metrics": analyze_financial_metrics,
    "analyze_financial_statements": analyze_financial_statements,
    "compare_companies": compare_companies,
    # Specialized tools
    "get_analyst_recommendations": get_analyst_recommendations,
    "analyze_income_statement": analyze_income_statement,
    "analyze_balance_sheet": analyze_balance_sheet,
    "analyze_cash_flow": analyze_cash_flow,
}
