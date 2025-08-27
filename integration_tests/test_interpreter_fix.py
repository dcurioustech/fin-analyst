#!/usr/bin/env python3
"""
Test script to verify the interpreter fix for company extraction.
"""
from agents.interpreter import RuleBasedInterpreter

def test_interpreter_fix():
    """Test the interpreter with various problematic inputs."""
    
    interpreter = RuleBasedInterpreter()
    
    test_cases = [
        {
            'input': 'Analyst ratings for Intel',
            'expected_companies': ['INTC'],
            'expected_analysis': 'recommendations',
            'description': 'Should extract Intel (INTC) and ignore "FOR"'
        },
        {
            'input': 'Show me Apple financials',
            'expected_companies': ['AAPL'],
            'expected_analysis': 'profile',
            'description': 'Should extract Apple (AAPL)'
        },
        {
            'input': 'Compare AAPL and MSFT',
            'expected_companies': ['AAPL', 'MSFT'],
            'expected_analysis': 'comparison',
            'description': 'Should extract both tickers'
        },
        {
            'input': 'What are the earnings for Tesla?',
            'expected_companies': ['TSLA'],
            'expected_analysis': 'income_statement',
            'description': 'Should extract Tesla (TSLA) and identify earnings analysis'
        },
        {
            'input': 'Get me info about Google',
            'expected_companies': ['GOOGL'],
            'expected_analysis': 'profile',
            'description': 'Should extract Google (GOOGL)'
        },
        {
            'input': 'Balance sheet for Microsoft',
            'expected_companies': ['MSFT'],
            'expected_analysis': 'balance_sheet',
            'description': 'Should extract Microsoft (MSFT) and identify balance sheet'
        },
        {
            'input': 'How is AMD performing?',
            'expected_companies': ['AMD'],
            'expected_analysis': 'profile',
            'description': 'Should extract AMD ticker'
        }
    ]
    
    print("=== INTERPRETER FIX TEST RESULTS ===\n")
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['description']}")
        print(f"Input: '{test_case['input']}'")
        
        # Run interpretation
        result = interpreter.interpret_request(test_case['input'])
        
        # Check companies
        companies_match = set(result.companies) == set(test_case['expected_companies'])
        analysis_match = result.analysis_type == test_case['expected_analysis']
        
        print(f"Expected companies: {test_case['expected_companies']}")
        print(f"Actual companies: {result.companies}")
        print(f"Expected analysis: {test_case['expected_analysis']}")
        print(f"Actual analysis: {result.analysis_type}")
        
        if companies_match and analysis_match:
            print("✅ PASSED")
        else:
            print("❌ FAILED")
            all_passed = False
            if not companies_match:
                print(f"   Companies mismatch!")
            if not analysis_match:
                print(f"   Analysis type mismatch!")
        
        print(f"Confidence: {result.confidence:.2f}")
        print("-" * 50)
    
    print(f"\n=== SUMMARY ===")
    if all_passed:
        print("🎉 All tests passed! The interpreter fix is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    # Specific test for the original issue
    print(f"\n=== ORIGINAL ISSUE TEST ===")
    result = interpreter.interpret_request("Analyst ratings for Intel")
    print(f"Input: 'Analyst ratings for Intel'")
    print(f"Companies extracted: {result.companies}")
    print(f"Analysis type: {result.analysis_type}")
    
    if result.companies == ['INTC'] and 'FOR' not in result.companies:
        print("✅ ORIGINAL ISSUE FIXED: 'FOR' is no longer extracted as a company")
    else:
        print("❌ ORIGINAL ISSUE NOT FIXED: Still extracting incorrect companies")

if __name__ == "__main__":
    test_interpreter_fix()