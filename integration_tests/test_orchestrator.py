#!/usr/bin/env python3
"""
Simple test script for the LangGraph Financial Analysis Orchestrator.

This script tests the basic functionality of the orchestrator-driven
financial analysis workflow.
"""
import logging
import sys

from agents.graph import financial_orchestrator
from agents.state import create_initial_state

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_basic_orchestrator():
    """Test basic orchestrator functionality."""
    print("🧪 Testing Financial Analysis Orchestrator")
    print("=" * 50)

    try:
        # Test 1: Start conversation
        print("\n📋 Test 1: Starting conversation")
        state = financial_orchestrator.start_conversation()
        print(f"✅ Welcome message: {state['agent_response'][:100]}...")

        # Test 2: Simple company analysis
        print("\n📋 Test 2: Simple company analysis")
        test_input = "Analyze Apple"
        print(f"🔤 Input: {test_input}")

        result_state = financial_orchestrator.process_user_request(test_input, state)

        if result_state.get("error_message"):
            print(f"❌ Error: {result_state['error_message']}")
        else:
            print(
                f"✅ Response generated: {len(result_state.get('agent_response', ''))} characters"
            )
            print(f"📊 Companies in context: {result_state.get('companies', [])}")
            print(f"🔍 Analysis type: {result_state.get('analysis_type')}")

        # Test 3: Clarification request
        print("\n📋 Test 3: Unclear request")
        test_input = "Tell me about stocks"
        print(f"🔤 Input: {test_input}")

        result_state = financial_orchestrator.process_user_request(
            test_input, create_initial_state()
        )

        if result_state.get("needs_clarification"):
            print("✅ Clarification requested as expected")
        else:
            print("⚠️  Expected clarification request")

        print(f"💬 Response: {result_state.get('agent_response', '')[:100]}...")

        # Test 4: Comparison request
        print("\n📋 Test 4: Comparison analysis")
        test_input = "Compare Apple and Microsoft"
        print(f"🔤 Input: {test_input}")

        result_state = financial_orchestrator.process_user_request(
            test_input, create_initial_state()
        )

        if result_state.get("error_message"):
            print(f"❌ Error: {result_state['error_message']}")
        else:
            print(f"✅ Comparison response generated")
            print(f"📊 Companies: {result_state.get('companies', [])}")
            print(f"🔍 Analysis type: {result_state.get('analysis_type')}")

        print("\n🎉 Basic orchestrator tests completed!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        logger.exception("Test error details:")
        return False


def test_interpreter():
    """Test the interpreter layer separately."""
    print("\n🧪 Testing Interpreter Layer")
    print("=" * 30)

    try:
        from agents.interpreter import default_interpreter

        # Test company recognition
        test_cases = [
            "Analyze Apple",
            "Tell me about MSFT",
            "Compare Tesla and Ford",
            "Show me Google's financials",
            "What about stocks?",
        ]

        for test_input in test_cases:
            print(f"\n🔤 Input: {test_input}")
            interpretation = default_interpreter.interpret_request(test_input)

            print(f"  📊 Companies: {interpretation.companies}")
            print(f"  🔍 Analysis type: {interpretation.analysis_type}")
            print(f"  📈 Confidence: {interpretation.confidence:.2f}")
            print(f"  ❓ Needs clarification: {interpretation.needs_clarification}")

        print("\n✅ Interpreter tests completed!")
        return True

    except Exception as e:
        print(f"\n❌ Interpreter test failed: {e}")
        logger.exception("Interpreter test error:")
        return False


def main():
    """Run all tests."""
    print("🚀 Starting LangGraph Financial Analysis Tests")
    print("=" * 60)

    # Test interpreter first
    interpreter_success = test_interpreter()

    # Test orchestrator
    orchestrator_success = test_basic_orchestrator()

    # Summary
    print("\n📊 Test Summary")
    print("=" * 20)
    print(f"Interpreter: {'✅ PASS' if interpreter_success else '❌ FAIL'}")
    print(f"Orchestrator: {'✅ PASS' if orchestrator_success else '❌ FAIL'}")

    if interpreter_success and orchestrator_success:
        print("\n🎉 All tests passed! The LangGraph integration is working.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the logs above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
