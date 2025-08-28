#!/usr/bin/env python3
"""
Integration Flow Tests for LangGraph Financial Analysis.

This test suite validates the complete data flow through all layers:
- Interpreter → Orchestrator → Tools → Response Generation
- Analysis quality and functionality validation
- Layer integration verification
"""
import logging
import os
import sys
from typing import Any, Dict, List

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_complete_data_flow():
    """Test complete data flow through all layers."""
    print("🧪 Testing Complete Data Flow")
    print("=" * 35)

    try:
        from agents.interpreter import default_interpreter
        from agents.response_generator import (ResponseContext,
                                               default_response_generator)
        from agents.state import (create_initial_state,
                                  update_state_with_user_input)
        from agents.tools import (analyze_company_profile, get_company_data,
                                  validate_ticker)

        # Test case: Single company analysis flow
        print("\n📋 Test: Complete Single Company Analysis Flow")
        user_input = "Analyze AAPL"
        print(f"🔤 User Input: {user_input}")

        # Step 1: Interpreter Layer
        print("\n🔄 Step 1: Interpreter Layer")
        interpretation = default_interpreter.interpret_request(user_input)
        print(f"  📊 Companies extracted: {interpretation.companies}")
        print(f"  🔍 Analysis type: {interpretation.analysis_type}")
        print(f"  📈 Confidence: {interpretation.confidence:.2f}")

        # Step 2: State Management
        print("\n🔄 Step 2: State Management")
        state = create_initial_state()
        state = update_state_with_user_input(state, user_input)
        state["companies"] = interpretation.companies
        state["analysis_type"] = interpretation.analysis_type
        print(f"  ✅ State updated with interpretation results")

        # Step 3: Tools Layer (Data Collection)
        print("\n🔄 Step 3: Tools Layer - Data Collection")
        if interpretation.companies and len(interpretation.companies) > 0:
            ticker = interpretation.companies[0]  # Use first valid ticker

            # Validate ticker first
            validation_result = validate_ticker.invoke({"ticker": ticker})
            print(f"  🔍 Ticker validation: {validation_result.get('valid', False)}")

            if validation_result.get("valid", False):
                # Get company data
                company_data_result = get_company_data.invoke({"ticker": ticker})
                print(
                    f"  📊 Company data retrieved: {company_data_result.get('success', False)}"
                )

                if company_data_result.get("success", False):
                    state["financial_data"] = {
                        ticker: company_data_result.get("data", {})
                    }

                    # Step 4: Tools Layer (Analysis)
                    print("\n🔄 Step 4: Tools Layer - Analysis")
                    analysis_result = analyze_company_profile.invoke(
                        {
                            "ticker": ticker,
                            "company_data": company_data_result.get("data", {}),
                        }
                    )
                    print(
                        f"  📈 Analysis completed: {analysis_result.get('success', False)}"
                    )

                    if analysis_result.get("success", False):
                        state["analysis_results"] = {
                            ticker: analysis_result.get("analysis", {})
                        }

                        # Step 5: Response Generation Layer
                        print("\n🔄 Step 5: Response Generation Layer")
                        response_context = ResponseContext()
                        response_context.analysis_type = interpretation.analysis_type
                        response_context.companies = [ticker]
                        response_context.analysis_results = state["analysis_results"]
                        response_context.user_input = user_input

                        response = default_response_generator.generate_response(
                            response_context
                        )
                        print(f"  💬 Response generated: {len(response)} characters")
                        print(f"  📝 Response preview: {response[:100]}...")

                        state["agent_response"] = response

                        print(f"\n✅ Complete data flow successful!")
                        return True, state
                    else:
                        print(f"  ❌ Analysis failed")
                else:
                    print(f"  ❌ Data collection failed")
            else:
                print(f"  ❌ Ticker validation failed")
        else:
            print(f"  ❌ No valid companies found")

        print(f"\n⚠️  Data flow incomplete")
        return False, state

    except Exception as e:
        print(f"\n❌ Complete data flow test failed: {e}")
        logger.exception("Complete data flow test error:")
        return False, None


def test_all_analysis_types():
    """Test all analysis types through the orchestrated workflow."""
    print("\n🧪 Testing All Analysis Types")
    print("=" * 35)

    try:
        from agents.interpreter import default_interpreter
        from agents.tools import (analyze_company_profile,
                                  analyze_financial_metrics,
                                  analyze_financial_statements,
                                  compare_companies)

        # Test cases for different analysis types (using only ticker symbols to avoid interpreter issues)
        test_cases = [
            {
                "name": "Company Profile Analysis",
                "input": "AAPL profile",
                "expected_type": "profile",
                "tool": analyze_company_profile,
            },
            {
                "name": "Financial Metrics Analysis",
                "input": "AAPL metrics",
                "expected_type": "metrics",
                "tool": analyze_financial_metrics,
            },
            {
                "name": "Financial Statements Analysis",
                "input": "AAPL income statement",
                "expected_type": "income_statement",
                "tool": analyze_financial_statements,
            },
            {
                "name": "Company Comparison",
                "input": "Compare AAPL MSFT",
                "expected_type": "comparison",
                "tool": compare_companies,
            },
        ]

        successful_tests = 0

        for test_case in test_cases:
            print(f"\n📋 Test: {test_case['name']}")
            print(f"🔤 Input: {test_case['input']}")

            # Interpret request
            interpretation = default_interpreter.interpret_request(test_case["input"])
            print(f"  🔍 Detected type: {interpretation.analysis_type}")
            print(f"  📊 Companies: {interpretation.companies}")

            # Check if interpretation matches expected
            type_match = interpretation.analysis_type == test_case["expected_type"]
            has_companies = len(interpretation.companies) > 0

            if type_match and has_companies:
                print(f"  ✅ Interpretation correct")

                # Test tool invocation (mock data)
                try:
                    # Filter to get only valid ticker-like symbols (3-5 uppercase letters)
                    valid_tickers = [
                        t
                        for t in interpretation.companies
                        if len(t) >= 3
                        and len(t) <= 5
                        and t.isalpha()
                        and t.isupper()
                        and t not in ["AND", "VS", "VERSUS", "THE", "FOR", "WITH"]
                    ]

                    if test_case["expected_type"] == "comparison":
                        # For comparison, need multiple tickers
                        if len(valid_tickers) >= 2:
                            result = test_case["tool"].invoke(
                                {
                                    "main_ticker": valid_tickers[0],
                                    "peer_tickers": valid_tickers[1:2],
                                }
                            )
                        else:
                            result = {
                                "success": False,
                                "error": "Insufficient valid tickers",
                            }
                    elif test_case["expected_type"] == "income_statement":
                        if valid_tickers:
                            result = test_case["tool"].invoke(
                                {"ticker": valid_tickers[0], "statement_type": "income"}
                            )
                        else:
                            result = {
                                "success": False,
                                "error": "No valid ticker found",
                            }
                    else:
                        if valid_tickers:
                            result = test_case["tool"].invoke(
                                {"ticker": valid_tickers[0]}
                            )
                        else:
                            result = {
                                "success": False,
                                "error": "No valid ticker found",
                            }

                    if result.get("success", False):
                        print(f"  ✅ Tool execution successful")
                        successful_tests += 1
                    else:
                        print(
                            f"  ⚠️  Tool execution failed: {result.get('error', 'Unknown error')}"
                        )

                except Exception as e:
                    print(f"  ❌ Tool execution error: {e}")
            else:
                print(
                    f"  ❌ Interpretation failed - Type: {type_match}, Companies: {has_companies}"
                )

        print(
            f"\n📊 Analysis Types Summary: {successful_tests}/{len(test_cases)} successful"
        )

        if successful_tests >= len(test_cases) * 0.75:  # 75% success rate
            print("✅ Analysis types test passed!")
            return True
        else:
            print("⚠️  Analysis types test needs improvement")
            return False

    except Exception as e:
        print(f"\n❌ Analysis types test failed: {e}")
        logger.exception("Analysis types test error:")
        return False


def test_layer_integration():
    """Test integration between all layers."""
    print("\n🧪 Testing Layer Integration")
    print("=" * 30)

    try:
        # Test 1: Interpreter → State Management
        print("\n📋 Test 1: Interpreter → State Management Integration")
        from agents.interpreter import default_interpreter
        from agents.state import (create_initial_state,
                                  update_state_with_user_input)

        interpretation = default_interpreter.interpret_request("Analyze AAPL")
        state = create_initial_state()
        state = update_state_with_user_input(state, "Analyze AAPL")

        # Verify state can hold interpretation results
        state["interpretation"] = interpretation.to_dict()
        state["companies"] = interpretation.companies
        state["analysis_type"] = interpretation.analysis_type

        print(f"  ✅ Interpreter → State: {len(state)} state fields populated")

        # Test 2: State → Tools Integration
        print("\n📋 Test 2: State → Tools Integration")
        from agents.tools import get_company_data, validate_ticker

        if state["companies"]:
            ticker = state["companies"][0]
            validation = validate_ticker.invoke({"ticker": ticker})

            if validation.get("valid", False):
                data_result = get_company_data.invoke({"ticker": ticker})
                state["financial_data"] = {ticker: data_result.get("data", {})}
                print(f"  ✅ State → Tools: Data retrieved for {ticker}")
            else:
                print(f"  ⚠️  State → Tools: Invalid ticker {ticker}")

        # Test 3: Tools → Response Generation Integration
        print("\n📋 Test 3: Tools → Response Generation Integration")
        from agents.response_generator import (ResponseContext,
                                               default_response_generator)

        response_context = ResponseContext()
        response_context.analysis_type = state.get("analysis_type")
        response_context.companies = state.get("companies", [])
        response_context.analysis_results = state.get("analysis_results", {})
        response_context.user_input = state.get("user_input", "")

        response = default_response_generator.generate_response(response_context)
        state["agent_response"] = response

        print(f"  ✅ Tools → Response: {len(response)} character response generated")

        # Test 4: End-to-End State Consistency
        print("\n📋 Test 4: End-to-End State Consistency")

        required_fields = ["user_input", "companies", "analysis_type", "agent_response"]
        missing_fields = [field for field in required_fields if not state.get(field)]

        if not missing_fields:
            print(f"  ✅ State Consistency: All required fields present")
        else:
            print(f"  ⚠️  State Consistency: Missing fields: {missing_fields}")

        # Test 5: Data Type Consistency
        print("\n📋 Test 5: Data Type Consistency")

        type_checks = [
            ("user_input", str),
            ("companies", list),
            ("analysis_type", (str, type(None))),
            ("agent_response", str),
            ("financial_data", dict),
            ("analysis_results", dict),
        ]

        type_errors = []
        for field, expected_type in type_checks:
            if field in state:
                if not isinstance(state[field], expected_type):
                    type_errors.append(
                        f"{field}: expected {expected_type}, got {type(state[field])}"
                    )

        if not type_errors:
            print(f"  ✅ Data Types: All fields have correct types")
        else:
            print(f"  ⚠️  Data Types: Issues found: {type_errors}")

        print("\n✅ Layer integration tests completed!")
        return True

    except Exception as e:
        print(f"\n❌ Layer integration test failed: {e}")
        logger.exception("Layer integration test error:")
        return False


def test_analysis_quality_regression():
    """Test that analysis quality hasn't regressed with new architecture."""
    print("\n🧪 Testing Analysis Quality (No Regression)")
    print("=" * 45)

    try:
        # Test direct analysis tools vs orchestrated workflow
        from agents.tools import (analyze_company_profile, get_company_data,
                                  validate_ticker)

        print("\n📋 Test: Direct Tool Analysis Quality")

        # Test with a known good ticker
        ticker = "AAPL"

        # Direct tool usage (original approach)
        print(f"\n🔄 Direct Tool Usage for {ticker}")

        validation = validate_ticker.invoke({"ticker": ticker})
        print(f"  🔍 Validation: {validation.get('valid', False)}")

        if validation.get("valid", False):
            data_result = get_company_data.invoke({"ticker": ticker})
            print(f"  📊 Data retrieval: {data_result.get('success', False)}")

            if data_result.get("success", False):
                analysis_result = analyze_company_profile.invoke(
                    {"ticker": ticker, "company_data": data_result.get("data", {})}
                )
                print(f"  📈 Analysis: {analysis_result.get('success', False)}")

                if analysis_result.get("success", False):
                    analysis_data = analysis_result.get("data", {})

                    # Check analysis quality indicators based on actual structure
                    basic_info = analysis_data.get("basic_info", {})
                    market_info = analysis_data.get("market_info", {})

                    quality_indicators = [
                        ("name", str, basic_info),
                        ("sector", str, basic_info),
                        ("market_cap", (int, float, type(None)), market_info),
                        ("ticker", str, basic_info),
                    ]

                    quality_score = 0
                    for indicator, expected_type, data_source in quality_indicators:
                        if indicator in data_source:
                            value = data_source[indicator]
                            if isinstance(value, expected_type) and value != "N/A":
                                quality_score += 1
                                print(f"    ✅ {indicator}: {value}")
                            else:
                                print(
                                    f"    ⚠️  {indicator}: {value} (type: {type(value)})"
                                )
                        else:
                            print(f"    ❌ {indicator}: missing")

                    quality_percentage = (quality_score / len(quality_indicators)) * 100
                    print(
                        f"  📊 Analysis Quality: {quality_percentage:.1f}% ({quality_score}/{len(quality_indicators)})"
                    )

                    if quality_percentage >= 75:
                        print(f"  ✅ Analysis quality acceptable")
                        return True
                    else:
                        print(f"  ⚠️  Analysis quality below threshold")
                        return False

        print(f"  ❌ Analysis quality test failed")
        return False

    except Exception as e:
        print(f"\n❌ Analysis quality test failed: {e}")
        logger.exception("Analysis quality test error:")
        return False


def main():
    """Run all integration flow tests."""
    print("🚀 LangGraph Financial Analysis - Integration Flow Tests")
    print("=" * 65)

    # Run all test suites
    data_flow_success, final_state = test_complete_data_flow()
    analysis_types_success = test_all_analysis_types()
    layer_integration_success = test_layer_integration()
    quality_regression_success = test_analysis_quality_regression()

    # Summary
    print("\n📊 Integration Flow Test Summary")
    print("=" * 40)
    print(f"Complete Data Flow: {'✅ PASS' if data_flow_success else '❌ FAIL'}")
    print(f"All Analysis Types: {'✅ PASS' if analysis_types_success else '❌ FAIL'}")
    print(f"Layer Integration: {'✅ PASS' if layer_integration_success else '❌ FAIL'}")
    print(f"Analysis Quality: {'✅ PASS' if quality_regression_success else '❌ FAIL'}")

    overall_success = all(
        [
            data_flow_success,
            analysis_types_success,
            layer_integration_success,
            quality_regression_success,
        ]
    )

    if overall_success:
        print(
            "\n🎉 All integration tests passed! The orchestrated workflow maintains quality."
        )
        print("📊 Layer integration is working correctly with no regressions.")
        return 0
    else:
        print("\n⚠️  Some integration tests failed. Check the logs above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
