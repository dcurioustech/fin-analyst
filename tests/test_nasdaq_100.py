"""Tests for NASDAQ-100 universe validation."""

from unittest.mock import patch

from agents.interpreter import RuleBasedInterpreter
from services.financial_data_service import FinancialDataService
from utils.nasdaq_100 import (
    NASDAQ_100_SNAPSHOT_DATE,
    filter_nasdaq_100_tickers,
    is_nasdaq_100_ticker,
)


def test_nasdaq_100_snapshot_accepts_constituents_and_rejects_other_companies():
    """The local universe should allow constituents but exclude non-members."""
    assert NASDAQ_100_SNAPSHOT_DATE == "2026-06-22"
    assert is_nasdaq_100_ticker("aapl")
    assert is_nasdaq_100_ticker("RKLB")
    assert not is_nasdaq_100_ticker("F")
    assert not is_nasdaq_100_ticker("JPM")


def test_filter_nasdaq_100_tickers_normalizes_and_preserves_order():
    """Filtering should retain only supported tickers without duplicates."""
    assert filter_nasdaq_100_tickers(["msft", "F", "AAPL", "MSFT"]) == [
        "MSFT",
        "AAPL",
    ]


@patch("services.financial_data_service.yf.Ticker")
def test_data_service_rejects_out_of_universe_ticker_before_yahoo_lookup(mock_ticker):
    """Out-of-scope requests must not trigger an external data request."""
    result = FinancialDataService().get_company_info("F")

    assert not result["success"]
    assert "outside the supported NASDAQ-100 universe" in result["error"]
    mock_ticker.assert_not_called()


def test_interpreter_explains_out_of_universe_company_request():
    """Natural-language requests should get an explicit scope response."""
    result = RuleBasedInterpreter().interpret_request("Analyze Ford")

    assert result.companies == []
    assert result.out_of_universe_tickers == ["F"]
    assert result.needs_clarification
    assert "outside the supported NASDAQ-100 universe" in result.clarification_message
