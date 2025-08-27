# Integration Tests

This directory contains integration and end-to-end tests for the Financial Analysis Bot.

## Test Categories

### 🔄 Integration Tests
- `test_integration_flow.py` - Complete data flow through all layers
- `test_orchestrator.py` - Basic orchestrator functionality
- `test_orchestrator_comprehensive.py` - Comprehensive orchestrator testing

### 🚨 Error Handling Tests
- `test_error_handling.py` - Error scenarios and recovery mechanisms
  - Invalid ticker recovery
  - Unclear request clarification
  - System error graceful degradation
  - Edge case inputs

### 🔍 Smoke Tests
- `test_suite_simple.py` - Basic functionality verification
  - Module imports
  - Application initialization
  - Core component functionality

### 🐛 Bug Fix Tests
- `test_comparison_fix.py` - Comparison analyzer fixes
- `test_interpreter_fix.py` - Interpreter fixes

## Running Integration Tests

### Individual Tests
```bash
# Run specific integration test
python integration_tests/test_orchestrator.py

# Run error handling tests
python integration_tests/test_error_handling.py

# Run complete integration flow
python integration_tests/test_integration_flow.py
```

### All Integration Tests
```bash
# Run all integration tests
python -m pytest integration_tests/ -v

# Run with coverage
python -m pytest integration_tests/ --cov=. --cov-report=term-missing
```

## Test Characteristics

- **Manual execution**: Can be run as standalone scripts
- **Integration focused**: Test component interactions
- **Orchestrator testing**: Validate LangGraph workflow
- **Error scenarios**: Focus on edge cases and recovery
- **No mocking**: Use real components where possible

## When to Run

- **Before releases**: Validate end-to-end functionality
- **After major changes**: Ensure integration still works
- **Bug investigation**: Reproduce and verify fixes
- **Performance testing**: Check workflow efficiency