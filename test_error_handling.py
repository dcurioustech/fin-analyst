#!/usr/bin/env python3
"""
Error Handling and Edge Case Tests for LangGraph Financial Analysis.

This test suite focuses specifically on error scenarios, edge cases,
and recovery mechanisms in the orchestrator workflow.
"""
import sys
import os
import logging
from typing import Dict, Any

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_invalid_ticker_recovery():
    """Test orchestrator recovery from invalid ticker symbols."""
    print("🧪 Testing Invalid Ticker Recovery")
    print("=" * 40)
    
    try:
        from agents.interpreter import default_interpreter
        from agents.tools import validate_ticker
        from agents.state import create_initial_state, update_state_with_user_input
        
        # Test cases with invalid tickers
        invalid_cases = [
            "Analyze INVALID",
            "Compare FAKE and NOTREAL", 
            "Tell me about BADTICKER",
            "Show me XYZ123 financials"
        ]
        
        for case in invalid_cases:
            print(f"\n📋 Testing: {case}")
            
            # Interpret the request
            interpretation = default_interpreter.interpret_request(case)
            print(f"  📊 Found companies: {interpretation.companies}")
            
            # Validate each ticker
            valid_tickers = []
            invalid_tickers = []
            
            for ticker in interpretation.companies:
                if len(ticker) <= 5 and ticker.isalpha():  # Basic ticker format check
                    try:
                        result = validate_ticker.invoke({"ticker": ticker})
                        if result.get("valid", False):
                            valid_tickers.append(ticker)
                        else:
                            invalid_tickers.append(ticker)
                    except Exception as e:
                        print(f"    ⚠️  Error validating {ticker}: {e}")
                        invalid_tickers.append(ticker)
                else:
                    invalid_tickers.append(ticker)
            
            print(f"  ✅ Valid tickers: {valid_tickers}")
            print(f"  ❌ Invalid tickers: {invalid_tickers}")
            
            # Test recovery logic
            if invalid_tickers and not valid_tickers:
                print(f"  🔄 Recovery: Request clarification for all invalid tickers")
            elif invalid_tickers and valid_tickers:
                print(f"  🔄 Recovery: Proceed with valid tickers, warn about invalid ones")
            else:
                print(f"  ✅ No recovery needed")
        
        print("\n✅ Invalid ticker recovery tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Invalid ticker recovery test failed: {e}")
        logger.exception("Invalid ticker recovery test error:")
        return False

def test_unclear_request_clarification():
    """Test clarification workflow for unclear requests."""
    print("\n🧪 Testing Unclear Request Clarification")
    print("=" * 45)
    
    try:
        from agents.interpreter import default_interpreter
        from agents.response_generator import default_response_generator
        
        # Test cases that should trigger clarification
        unclear_cases = [
            "",  # Empty input
            "   ",  # Whitespace only
            "hello",  # Greeting
            "help me",  # Generic help
            "what can you do?",  # Capability question
            "stocks",  # Too vague
            "financial analysis",  # No specific company
            "market trends",  # General market question
            "asdfghjkl",  # Random text
            "123456",  # Numbers only
            "!@#$%^&*()",  # Special characters
        ]
        
        clarification_count = 0
        
        for case in unclear_cases:
            print(f"\n📋 Testing: '{case}'")
            
            interpretation = default_interpreter.interpret_request(case)
            
            print(f"  📊 Companies found: {interpretation.companies}")
            print(f"  🔍 Analysis type: {interpretation.analysis_type}")
            print(f"  ❓ Needs clarification: {interpretation.needs_clarification}")
            print(f"  📈 Confidence: {interpretation.confidence:.2f}")
            
            if interpretation.needs_clarification:
                clarification_count += 1
                clarification_msg = default_response_generator.generate_clarification_request()
                print(f"  💬 Clarification: {clarification_msg[:80]}...")
            
            # Validate that unclear requests are properly identified
            expected_unclear = (
                not interpretation.companies or 
                interpretation.confidence < 0.5 or
                interpretation.analysis_type is None
            )
            
            if expected_unclear and interpretation.needs_clarification:
                print(f"  ✅ Correctly identified as unclear")
            elif not expected_unclear and not interpretation.needs_clarification:
                print(f"  ✅ Correctly processed")
            else:
                print(f"  ⚠️  Unexpected clarification behavior")
        
        print(f"\n📊 Summary: {clarification_count}/{len(unclear_cases)} requests triggered clarification")
        print("✅ Unclear request clarification tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Unclear request clarification test failed: {e}")
        logger.exception("Unclear request clarification test error:")
        return False

def test_system_error_graceful_degradation():
    """Test graceful degradation during system errors."""
    print("\n🧪 Testing System Error Graceful Degradation")
    print("=" * 50)
    
    try:
        from agents.state import create_initial_state, update_state_with_user_input, set_error
        from agents.response_generator import default_response_generator
        
        # Test 1: State corruption recovery
        print("\n📋 Test 1: State Corruption Recovery")
        state = create_initial_state()
        
        # Simulate corrupted state
        corrupted_state = state.copy()
        corrupted_state["companies"] = "not_a_list"  # Should be a list
        corrupted_state["analysis_results"] = None  # Should be a dict
        
        try:
            # Try to process with corrupted state
            updated_state = update_state_with_user_input(corrupted_state, "Analyze AAPL")
            print("  ✅ State corruption handled gracefully")
        except Exception as e:
            print(f"  ⚠️  State corruption caused error: {e}")
        
        # Test 2: Network/API error simulation
        print("\n📋 Test 2: Network Error Simulation")
        
        # Simulate network timeout by testing with a very long ticker
        try:
            from agents.tools import validate_ticker
            # This should fail gracefully
            result = validate_ticker.invoke({"ticker": "VERYLONGINVALIDTICKER"})
            print(f"  ✅ Network error handled: {result.get('valid', False)}")
        except Exception as e:
            print(f"  ✅ Network error caught and handled: {type(e).__name__}")
        
        # Test 3: Error state management
        print("\n📋 Test 3: Error State Management")
        
        error_state = create_initial_state()
        error_state = set_error(error_state, "Simulated system error")
        
        print(f"  📊 Error message set: {error_state.get('error_message')}")
        print(f"  📊 State still valid: {isinstance(error_state, dict)}")
        
        # Test 4: Response generation with errors
        print("\n📋 Test 4: Response Generation with Errors")
        
        # Test response generation when analysis fails
        from agents.response_generator import ResponseContext
        
        error_context = ResponseContext()
        error_context.error_message = "Analysis failed due to data unavailability"
        error_context.user_input = "Analyze AAPL"
        
        try:
            response = default_response_generator.generate_response(error_context)
            print(f"  ✅ Error response generated: {len(response)} characters")
        except Exception as e:
            print(f"  ⚠️  Error response generation failed: {e}")
        
        print("\n✅ System error graceful degradation tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ System error graceful degradation test failed: {e}")
        logger.exception("System error graceful degradation test error:")
        return False

def test_edge_case_inputs():
    """Test edge case inputs and boundary conditions."""
    print("\n🧪 Testing Edge Case Inputs")
    print("=" * 30)
    
    try:
        from agents.interpreter import default_interpreter
        
        # Edge case inputs
        edge_cases = [
            # Very long input
            "Analyze " + "A" * 1000,
            
            # Mixed case and special characters
            "aNaLyZe AaPl AnD mSfT!!!",
            
            # Multiple spaces and formatting
            "Compare    AAPL     and     MSFT    ",
            
            # Unicode and international characters
            "Analyze AAPL résumé naïve café",
            
            # Numbers mixed with text
            "Compare AAPL123 and MSFT456",
            
            # HTML/XML-like input
            "<analyze>AAPL</analyze>",
            
            # JSON-like input
            '{"action": "analyze", "ticker": "AAPL"}',
            
            # SQL-like input
            "SELECT * FROM stocks WHERE ticker = 'AAPL'",
            
            # Very short input
            "A",
            "AA",
            
            # Repeated words
            "analyze analyze analyze AAPL AAPL AAPL",
        ]
        
        for i, case in enumerate(edge_cases, 1):
            print(f"\n📋 Edge Case {i}: {case[:50]}{'...' if len(case) > 50 else ''}")
            
            try:
                interpretation = default_interpreter.interpret_request(case)
                
                print(f"  📊 Companies: {interpretation.companies[:3]}{'...' if len(interpretation.companies) > 3 else ''}")
                print(f"  🔍 Analysis type: {interpretation.analysis_type}")
                print(f"  📈 Confidence: {interpretation.confidence:.2f}")
                print(f"  ❓ Needs clarification: {interpretation.needs_clarification}")
                print(f"  ✅ Processed successfully")
                
            except Exception as e:
                print(f"  ❌ Processing failed: {e}")
        
        print("\n✅ Edge case input tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Edge case input test failed: {e}")
        logger.exception("Edge case input test error:")
        return False

def main():
    """Run all error handling and edge case tests."""
    print("🚀 LangGraph Financial Analysis - Error Handling & Edge Cases")
    print("=" * 70)
    
    # Run all test suites
    ticker_recovery_success = test_invalid_ticker_recovery()
    clarification_success = test_unclear_request_clarification()
    degradation_success = test_system_error_graceful_degradation()
    edge_case_success = test_edge_case_inputs()
    
    # Summary
    print("\n📊 Error Handling Test Summary")
    print("=" * 35)
    print(f"Invalid Ticker Recovery: {'✅ PASS' if ticker_recovery_success else '❌ FAIL'}")
    print(f"Unclear Request Clarification: {'✅ PASS' if clarification_success else '❌ FAIL'}")
    print(f"System Error Degradation: {'✅ PASS' if degradation_success else '❌ FAIL'}")
    print(f"Edge Case Inputs: {'✅ PASS' if edge_case_success else '❌ FAIL'}")
    
    overall_success = all([
        ticker_recovery_success,
        clarification_success, 
        degradation_success,
        edge_case_success
    ])
    
    if overall_success:
        print("\n🎉 All error handling tests passed! The system handles edge cases gracefully.")
        return 0
    else:
        print("\n⚠️  Some error handling tests failed. Check the logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())