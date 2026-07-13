"""NASDAQ-100 constituent universe used to scope supported analysis."""

from typing import Iterable, List

# Snapshot source: Nasdaq's constituent page (2025-05-19), adjusted for the
# official June 2026 quarterly rebalance effective 2026-06-22. The index can
# hold more than 100 securities because a constituent may have multiple share
# classes (for example, Alphabet's GOOG and GOOGL).
NASDAQ_100_CONSTITUENTS_SOURCE = (
    "https://www.nasdaq.com/solutions/global-indexes/nasdaq-100/companies"
)
NASDAQ_100_REBALANCE_SOURCE = (
    "https://www.nasdaq.com/press-release/"
    "nasdaq-100-indexr-june-2026-quarterly-changes-2026-06-12"
)
NASDAQ_100_SNAPSHOT_DATE = "2026-06-22"
NASDAQ_100_TICKERS = frozenset(
    {
        "AAPL", "ABNB", "ADBE", "ADI", "ADP", "ADSK", "AEP", "ALAB", "ALNY",
        "AMAT", "AMD", "AMGN", "AMZN", "APP", "ARM", "ASML", "AVGO", "AXON",
        "BKNG", "BKR", "CCEP", "CDNS", "CEG", "CMCSA", "COST", "CPRT", "CRWD",
        "CRWV", "CSCO", "CSGP", "CSX", "CTAS", "DASH", "DDOG", "DXCM", "EA",
        "EXC", "FANG", "FAST", "FER", "FTNT", "GEHC", "GILD", "GOOG", "GOOGL",
        "HON", "IDXX", "INTC", "INTU", "ISRG", "KDP", "KHC", "KLAC", "LIN",
        "LRCX", "MAR", "MCHP", "MDLZ", "MELI", "META", "MNST", "MPWR", "MRVL",
        "MSFT", "MSTR", "MU", "NBIS", "NFLX", "NVDA", "NXPI", "ODFL", "ORLY",
        "PANW", "PAYX", "PCAR", "PDD", "PEP", "PLTR", "PYPL", "QCOM", "REGN",
        "RKLB", "ROP", "ROST", "SBUX", "SHOP", "SNPS", "STX", "TEAM", "TER",
        "TMUS", "TRI", "TSLA", "TTWO", "TXN", "VRTX", "WBD", "WDAY", "WDC",
        "WMT", "XEL",
    }
)


def normalize_ticker(ticker: str) -> str:
    """Return a normalized ticker, or an empty string for invalid input."""
    return ticker.strip().upper() if isinstance(ticker, str) else ""


def is_nasdaq_100_ticker(ticker: str) -> bool:
    """Return whether ``ticker`` is in the maintained NASDAQ-100 snapshot."""
    return normalize_ticker(ticker) in NASDAQ_100_TICKERS


def filter_nasdaq_100_tickers(tickers: Iterable[str]) -> List[str]:
    """Return normalized, de-duplicated NASDAQ-100 tickers in input order."""
    filtered = []
    for ticker in tickers:
        normalized = normalize_ticker(ticker)
        if normalized in NASDAQ_100_TICKERS and normalized not in filtered:
            filtered.append(normalized)
    return filtered


def unsupported_ticker_message(ticker: str) -> str:
    """Return the standard user-facing response for an out-of-universe ticker."""
    return (
        f"{normalize_ticker(ticker) or 'That ticker'} is outside the supported "
        "NASDAQ-100 universe. Please choose a current NASDAQ-100 constituent."
    )
