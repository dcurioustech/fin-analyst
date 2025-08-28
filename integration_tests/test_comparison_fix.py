#!/usr/bin/env python3
"""
Test script to verify the comparison analyzer fix.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from analysis.comparison_analyzer import ComparisonAnalyzer


def test_comparison_fix():
    """Test the comparison analyzer with sample SMCI vs NVDA data."""

    # Sample data that mimics the issue you described
    # NVDA should have better (lower) P/E, P/S, P/B ratios
    sample_data = {
        "SMCI": {
            "marketCap": 15000000000,  # 15B
            "trailingPE": 25.5,  # Higher P/E (worse)
            "priceToSalesTrailing12Months": 3.2,  # Higher P/S (worse)
            "priceToBook": 4.1,  # Higher P/B (worse)
            "profitMargins": 0.08,  # 8% profit margin
            "returnOnEquity": 0.15,  # 15% ROE
        },
        "NVDA": {
            "marketCap": 800000000000,  # 800B
            "trailingPE": 22.1,  # Lower P/E (better)
            "priceToSalesTrailing12Months": 2.8,  # Lower P/S (better)
            "priceToBook": 3.5,  # Lower P/B (better)
            "profitMargins": 0.12,  # 12% profit margin (better)
            "returnOnEquity": 0.18,  # 18% ROE (better)
        },
    }

    analyzer = ComparisonAnalyzer()

    # Test the comparison
    result = analyzer.perform_peer_comparison("SMCI", ["NVDA"], sample_data)

    if result["success"]:
        comparison_data = result["data"]
        competitive_analysis = comparison_data["competitive_analysis"]

        print("=== COMPARISON TEST RESULTS ===")
        print(f"Main ticker: {comparison_data['main_ticker']}")
        print(f"Peer tickers: {comparison_data['peer_tickers']}")

        print("\n--- Comparison Table ---")
        print(comparison_data["comparison_table"])

        if competitive_analysis["success"]:
            positioning = competitive_analysis["data"]

            print(f"\n--- Competitive Position for SMCI ---")

            if positioning.get("strengths"):
                print("Strengths:")
                for strength in positioning["strengths"]:
                    print(f"  • {strength}")
            else:
                print("No significant strengths identified")

            if positioning.get("weaknesses"):
                print("Areas for Improvement:")
                for weakness in positioning["weaknesses"]:
                    print(f"  • {weakness}")
            else:
                print("No significant weaknesses identified")

            print("\nRankings:")
            for metric, ranking in positioning.get("rankings", {}).items():
                percentile = positioning.get("percentile_rankings", {}).get(
                    metric, "N/A"
                )
                print(f"  {metric}: {ranking} ({percentile})")

            # Debug the percentile calculation
            print("\n=== DEBUG PERCENTILE CALCULATION ===")
            comparison_table = comparison_data["comparison_table"]
            df_numeric = comparison_table.apply(pd.to_numeric, errors="coerce")

            for column in df_numeric.columns:
                if "SMCI" in df_numeric.index:
                    smci_value = df_numeric.loc["SMCI", column]
                    nvda_value = df_numeric.loc["NVDA", column]
                    column_values = df_numeric[column].dropna()

                    # Check if higher is better
                    higher_is_better = analyzer._is_higher_better(column)

                    print(f"\n{column}:")
                    print(f"  SMCI: {smci_value}, NVDA: {nvda_value}")
                    print(f"  Higher is better: {higher_is_better}")

                    if higher_is_better:
                        rank = (column_values > smci_value).sum() + 1
                        percentile = (
                            (column_values <= smci_value).sum() / len(column_values)
                        ) * 100
                    else:
                        rank = (column_values < smci_value).sum() + 1
                        percentile = (
                            (column_values >= smci_value).sum() / len(column_values)
                        ) * 100

                    print(f"  SMCI rank: {rank} of {len(column_values)}")
                    print(f"  SMCI percentile: {percentile}%")

                    if higher_is_better:
                        better_performer = "NVDA" if nvda_value > smci_value else "SMCI"
                    else:
                        better_performer = "NVDA" if nvda_value < smci_value else "SMCI"
                    print(f"  Better performer: {better_performer}")

        print(f"\n--- Summary ---")
        print(comparison_data["summary"])

        # Verify the fix
        print("\n=== VERIFICATION ===")
        positioning = competitive_analysis["data"]

        # Check if SMCI is correctly identified as having weak ratios
        pe_weak = any(
            "p/e" in weakness.lower() for weakness in positioning.get("weaknesses", [])
        )
        ps_weak = any(
            "p/s" in weakness.lower() for weakness in positioning.get("weaknesses", [])
        )
        pb_weak = any(
            "p/b" in weakness.lower() for weakness in positioning.get("weaknesses", [])
        )

        print(f"P/E identified as weakness: {pe_weak}")
        print(f"P/S identified as weakness: {ps_weak}")
        print(f"P/B identified as weakness: {pb_weak}")

        if pe_weak and ps_weak and pb_weak:
            print(
                "✅ FIX VERIFIED: SMCI correctly identified as having weak valuation ratios"
            )
        else:
            print(
                "❌ FIX NOT WORKING: SMCI should have weak valuation ratios compared to NVDA"
            )

    else:
        print(f"❌ Test failed: {result['error']}")


if __name__ == "__main__":
    test_comparison_fix()
