"""
Company profile analysis functionality.
"""

import logging
from typing import Any, Dict, Optional


class CompanyAnalyzer:
    """Analyzer for company profile and basic information."""

    def __init__(self):
        """Initialize the company analyzer."""
        self.logger = logging.getLogger(__name__)

    def analyze_company_profile(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes and structures company profile information.

        Args:
            company_info: Raw company information from data service

        Returns:
            Structured company profile data
        """
        if not company_info:
            return {
                "success": False,
                "error": "No company information provided",
                "data": None,
            }

        try:
            profile_data = self.extract_key_company_details(company_info)

            return {"success": True, "error": None, "data": profile_data}

        except Exception as e:
            self.logger.error(f"Error analyzing company profile: {e}")
            return {
                "success": False,
                "error": f"Failed to analyze company profile: {str(e)}",
                "data": None,
            }

    def extract_key_company_details(
        self, company_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extracts key company details from raw company information.

        Args:
            company_info: Raw company information

        Returns:
            Dictionary with structured company details
        """
        return {
            "basic_info": {
                "name": company_info.get("longName", "N/A"),
                "ticker": company_info.get("symbol", "N/A"),
                "sector": company_info.get("sector", "N/A"),
                "industry": company_info.get("industry", "N/A"),
                "country": company_info.get("country", "N/A"),
                "website": company_info.get("website", "N/A"),
                "employees": company_info.get("fullTimeEmployees", "N/A"),
            },
            "business_summary": company_info.get(
                "longBusinessSummary", "No summary available."
            ),
            "market_info": {
                "market_cap": company_info.get("marketCap"),
                "enterprise_value": company_info.get("enterpriseValue"),
                "shares_outstanding": company_info.get("sharesOutstanding"),
                "float_shares": company_info.get("floatShares"),
            },
            "exchange_info": {
                "exchange": company_info.get("exchange", "N/A"),
                "currency": company_info.get("currency", "N/A"),
                "timezone": company_info.get("timeZoneFullName", "N/A"),
            },
        }

    def format_company_summary(self, company_info: Dict[str, Any]) -> str:
        """
        Formats company information into a readable summary string.

        Args:
            company_info: Raw company information

        Returns:
            Formatted company summary string
        """
        try:
            profile_data = self.extract_key_company_details(company_info)
            basic_info = profile_data["basic_info"]

            summary_lines = [
                f"Company: {basic_info['name']} ({basic_info['ticker']})",
                f"Sector: {basic_info['sector']}",
                f"Industry: {basic_info['industry']}",
                f"Country: {basic_info['country']}",
            ]

            if basic_info["employees"] != "N/A":
                summary_lines.append(f"Employees: {basic_info['employees']:,}")

            if basic_info["website"] != "N/A":
                summary_lines.append(f"Website: {basic_info['website']}")

            return "\n".join(summary_lines)

        except Exception as e:
            self.logger.error(f"Error formatting company summary: {e}")
            return "Error formatting company summary"

    def get_company_overview(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gets a comprehensive company overview including key highlights.

        Args:
            company_info: Raw company information

        Returns:
            Dictionary with company overview data
        """
        try:
            profile_data = self.extract_key_company_details(company_info)

            # Calculate some basic metrics for overview
            market_cap = profile_data["market_info"]["market_cap"]
            current_price = company_info.get("currentPrice")

            overview = {
                "company_profile": profile_data,
                "key_highlights": {
                    "current_price": current_price,
                    "market_cap": market_cap,
                    "pe_ratio": company_info.get("trailingPE"),
                    "dividend_yield": company_info.get("dividendYield"),
                    "beta": company_info.get("beta"),
                },
                "business_description": profile_data["business_summary"],
            }

            return {"success": True, "data": overview, "error": None}

        except Exception as e:
            self.logger.error(f"Error creating company overview: {e}")
            return {
                "success": False,
                "data": None,
                "error": f"Failed to create company overview: {str(e)}",
            }

    def validate_company_data(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates company data completeness and quality.

        Args:
            company_info: Raw company information

        Returns:
            Dictionary with validation results
        """
        validation_results = {
            "is_valid": True,
            "missing_fields": [],
            "warnings": [],
            "data_quality_score": 0,
        }

        # Check for essential fields
        essential_fields = [
            "longName",
            "sector",
            "industry",
            "currentPrice",
            "marketCap",
        ]
        missing_essential = []

        for field in essential_fields:
            if not company_info.get(field):
                missing_essential.append(field)

        if missing_essential:
            validation_results["is_valid"] = False
            validation_results["missing_fields"] = missing_essential

        # Check for optional but important fields
        important_fields = [
            "longBusinessSummary",
            "website",
            "fullTimeEmployees",
            "trailingPE",
        ]
        missing_important = []

        for field in important_fields:
            if not company_info.get(field):
                missing_important.append(field)

        if missing_important:
            validation_results["warnings"].append(
                f"Missing optional fields: {', '.join(missing_important)}"
            )

        # Calculate data quality score (0-100)
        total_fields = len(essential_fields) + len(important_fields)
        available_fields = (
            total_fields - len(missing_essential) - len(missing_important)
        )
        validation_results["data_quality_score"] = int(
            (available_fields / total_fields) * 100
        )

        return validation_results
