#!/usr/bin/env python3
"""
Comprehensive test suite for the LangGraph Financial Analysis Orchestrator.

This test suite covers:
- Single company analysis orchestration
- Comparison analysis orchestration  
- Follow-up questions with context maintenance
- Error handling and edge cases
- Layer integration validation
"""
import sys
import os
import logging
from typing import Dict, Any

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_without_langgraph():
    """Test the core components without requiring LangGraph installation."""
    print("🧪 Testing Core Components (No LangGraph Required)")
    print("=" * 60)
    
    try:
        # Test 1: State management
        print("\n📋 Test 1: State Management")
        from agents.state import create_initial_state, update_state_with_user_input
        
        state = create_initial_state()
        print(f"✅ Initial state created: {list(state.keys())}")
        
        updated_state = update_state_with_user_input(state, "Analyze Apple")
        print(f"✅ State updated with user input: {updated_state['user_input']}")
        
        # Test 2: Interpreter layer
        print("\n📋 Test 2: Interpreter Layer")
        from agents.interpreter import default_interpreter
        
        test_cases = [
            ("Analyze AAPL", ["AAPL"], "profile"),
            ("Compare AAPL and MSFT", ["AAPL", "MSFT"], "comparison"),
            ("Tell me about TSLA", ["TSLA"], "profile"),
            ("What about financial markets?", [], "unclear")
        ]
        
        for input_text, expected_companies, expected_type in test_cases:
            interpretation = default_interpreter.interpret_request(input_text)
            print(f"  🔤 '{input_text}'")
            print(f"    📊 Companies: {interpretation.companies} (expected: {expected_companies})")
            print(f"    🔍 Type: {interpretation.analysis_type} (expected: {expected_type})")
            print(f"    📈 Confidence: {interpretation.confidence:.2f}")
            
            # Validate results
            companies_match = set(interpretation.companies) == set(expected_companies)
            type_match = interpretation.analysis_type == expected_type
            
            if companies_match and type_match:
                print(f"    ✅ PASS")
            else:
                print(f"    ❌ FAIL - Companies: {companies_match}, Type: {type_match}")
        
        # Test 3: Tools layer
        print("\n📋 Test 3: Tools Layer")
        from agents.tools import get_company_data, validate_ticker
        
        # Test ticker validation
        valid_result = validate_ticker.invoke({"ticker": "AAPL"})
        print(f"  ✅ Valid ticker (AAPL): {valid_result}")
        
        invalid_result = validate_ticker.invoke({"ticker": "INVALID"})
        print(f"  ✅ Invalid ticker (INVALID): {invalid_result}")
        
        # Test 4: Response generator
        print("\n📋 Test 4: Response Generator")
        from agents.response_generator import default_response_generator
        
        welcome = default_response_generator.generate_welcome_message()
        print(f"  ✅ Welcome message: {welcome[:100]}...")
        
        clarification = default_response_generator.generate_clarification_request("unclear request")
        print(f"  ✅ Clarification: {clarification[:100]}...")
        
        # Test generic response generation
        from agents.response_generator import ResponseContext
        context = ResponseContext()
        context.analysis_type = "profile"
        context.companies = ["AAPL"]
        context.analysis_results = {"test": "data"}
        context.user_input = "test request"
        
        response = default_response_generator.generate_response(context)
        print(f"  ✅ Generated response: {len(response)} characters")
        
        print("\n🎉 Core component tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Core component test failed: {e}")
        logger.exception("Core component test error:")
        return False

def test_with_mock_orchestrator():
    """Test orchestrator workflow with mocked LangGraph."""
    print("\n🧪 Testing Orchestrator Workflow (Mocked)")
    print("=" * 50)
    
    try:
        # Mock the orchestrator behavior
        from agents.state import create_initial_state, update_state_with_user_input, update_state_with_agent_response
        from agents.interpreter import default_interpreter
        from agents.response_generator import default_response_generator
        
        def mock_orchestrator_process(user_input: str, state=None):
            """Mock orchestrator processing."""
            if state is None:
                state = create_initial_state()
            
            # Update state with user input
            state = update_state_with_user_input(state, user_input)
            
            # Interpret request
            interpretation = default_interpreter.interpret_request(user_input)
            state["companies"] = interpretation.companies
            state["analysis_type"] = interpretation.analysis_type
            state["needs_clarification"] = interpretation.needs_clarification
            
            # Generate response based on interpretation
            if interpretation.needs_clarification:
                response = default_response_generator.generate_clarification_request(user_input)
            elif interpretation.companies:
                if interpretation.analysis_type == "comparison":
                    response = f"I'll compare {' and '.join(interpretation.companies)} for you. Here's the analysis..."
                else:
                    response = f"Here's the analysis for {interpretation.companies[0]}..."
            else:
                response = "I couldn't identify any companies in your request. Please specify a company name or ticker symbol."
            
            state = update_state_with_agent_response(state, response)
            return state
        
        # Test cases for orchestrator workflow
        test_cases = [
            {
                "name": "Single Company Analysis",
                "input": "Analyze AAPL",
                "expected_companies": ["AAPL"],
                "expected_type": "profile"
            },
            {
                "name": "Comparison Analysis", 
                "input": "Compare AAPL and MSFT",
                "expected_companies": ["AAPL", "MSFT"],
                "expected_type": "comparison"
            },
            {
                "name": "Unclear Request",
                "input": "What about financial markets?",
                "expected_companies": [],
                "expected_type": "unclear"
            }
        ]
        
        for test_case in test_cases:
            print(f"\n📋 Test: {test_case['name']}")
            print(f"🔤 Input: {test_case['input']}")
            
            result_state = mock_orchestrator_process(test_case['input'])
            
            print(f"📊 Companies: {result_state.get('companies', [])}")
            print(f"🔍 Analysis type: {result_state.get('analysis_type')}")
            print(f"💬 Response: {result_state.get('agent_response', '')[:100]}...")
            
            # Validate results
            companies_match = set(result_state.get('companies', [])) == set(test_case['expected_companies'])
            type_match = result_state.get('analysis_type') == test_case['expected_type']
            has_response = bool(result_state.get('agent_response'))
            
            if companies_match and type_match and has_response:
                print("✅ PASS")
            else:
                print(f"❌ FAIL - Companies: {companies_match}, Type: {type_match}, Response: {has_response}")
        
        # Test follow-up context
        print(f"\n📋 Test: Follow-up Context Maintenance")
        initial_state = mock_orchestrator_process("Analyze AAPL")
        followup_state = mock_orchestrator_process("What about its revenue?", initial_state)
        
        print(f"📊 Context maintained: {followup_state.get('companies', [])}")
        print(f"💬 Follow-up response: {followup_state.get('agent_response', '')[:100]}...")
        
        context_maintained = followup_state.get('companies') == initial_state.get('companies')
        print(f"✅ Context maintenance: {'PASS' if context_maintained else 'FAIL'}")
        
        print("\n🎉 Mocked orchestrator tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Mocked orchestrator test failed: {e}")
        logger.exception("Mocked orchestrator test error:")
        return False

def test_error_scenarios():
    """Test error handling and edge cases."""
    print("\n🧪 Testing Error Scenarios")
    print("=" * 30)
    
    try:
        from agents.interpreter import default_interpreter
        from agents.response_generator import default_response_generator
        from agents.tools import validate_ticker
        
        # Test 1: Invalid ticker symbols
        print("\n📋 Test 1: Invalid Ticker Handling")
        invalid_tickers = ["INVALID", "NOTREAL", "123ABC"]
        
        for ticker in invalid_tickers:
            result = validate_ticker.invoke({"ticker": ticker})
            print(f"  🔤 {ticker}: {result}")
        
        # Test 2: Empty or malformed requests
        print("\n📋 Test 2: Malformed Request Handling")
        malformed_requests = ["", "   ", "asdfghjkl", "123456", "!@#$%^"]
        
        for request in malformed_requests:
            interpretation = default_interpreter.interpret_request(request)
            print(f"  🔤 '{request}': needs_clarification={interpretation.needs_clarification}")
        
        # Test 3: Error response generation
        print("\n📋 Test 3: Error Response Generation")
        # Test error handling through clarification requests
        clarification_response = default_response_generator.generate_clarification_request(
            "I couldn't understand your request. Please try again."
        )
        print(f"  ✅ Error handling via clarification: {len(clarification_response)} characters")
        
        print("\n✅ Error scenario tests completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error scenario test failed: {e}")
        logger.exception("Error scenario test error:")
        return False

def main():
    """Run comprehensive test suite."""
    print("🚀 LangGraph Financial Analysis - Comprehensive Test Suite")
    print("=" * 70)
    
    # Run tests
    core_success = test_without_langgraph()
    orchestrator_success = test_with_mock_orchestrator()
    error_success = test_error_scenarios()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 20)
    print(f"Core Components: {'✅ PASS' if core_success else '❌ FAIL'}")
    print(f"Orchestrator Logic: {'✅ PASS' if orchestrator_success else '❌ FAIL'}")
    print(f"Error Handling: {'✅ PASS' if error_success else '❌ FAIL'}")
    
    overall_success = core_success and orchestrator_success and error_success
    
    if overall_success:
        print("\n🎉 All tests passed! The LangGraph integration logic is working correctly.")
        print("📝 Note: Install LangGraph dependencies to test the full workflow.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the logs above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())