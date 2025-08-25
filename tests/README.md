# Financial Analysis Bot Test Suite

This directory contains comprehensive tests for the modularized Financial Analysis Bot.

## Test Structure

### Test Files

- **`test_utils.py`** - Unit tests for utility modules (formatters, error handling, input validation, visualizations)
- **`test_services.py`** - Unit tests for service layer (financial data service)
- **`test_analysis.py`** - Unit tests for analysis modules (company, metrics, statement, comparison analyzers)
- **`test_ui.py`** - Unit tests for UI components (menu handler, display formatter)
- **`test_integration.py`** - Integration tests for complete user workflows
- **`test_fixtures.py`** - Mock data and fixtures for consistent testing
- **`test_config.py`** - Test configuration and base test classes

### Test Runners

- **`run_tests.py`** - Comprehensive test runner with detailed reporting
- **`test_suite_simple.py`** - Simple test suite focusing on core functionality

## Running Tests

### Run All Tests
```bash
python3 tests/run_tests.py
```

### Run Specific Module Tests
```bash
python3 tests/run_tests.py --module tests.test_utils
python3 tests/run_tests.py --module tests.test_services
python3 tests/run_tests.py --module tests.test_analysis
python3 tests/run_tests.py --module tests.test_ui
python3 tests/run_tests.py --module tests.test_integration
```

### Run Simple Test Suite
```bash
python3 test_suite_simple.py
```

### Run Specific Test Pattern
```bash
python3 tests/run_tests.py --pattern tests.test_utils.TestFormatters
```

### Verbose Output
```bash
python3 tests/run_tests.py --verbose
```

## Test Categories

### 1. Unit Tests

**Utility Tests (`test_utils.py`)**
- Formatters: Number, percentage, currency formatting
- Error handling: Ticker validation, logging setup
- Input validation: Ticker lists, menu choices
- Visualizations: Text bar charts, comparison charts

**Service Tests (`test_services.py`)**
- Financial data service: Ticker validation, company info retrieval
- Batch operations: Multiple company data, peer comparison data
- Error handling: API failures, invalid tickers
- Mock external API calls using unittest.mock

**Analysis Tests (`test_analysis.py`)**
- Company analyzer: Profile analysis, business summary processing
- Metrics analyzer: Valuation, profitability, stock price metrics
- Statement analyzer: Income statement, balance sheet, cash flow processing
- Comparison analyzer: Peer comparison, visual comparisons

**UI Tests (`test_ui.py`)**
- Menu handler: User input processing, menu navigation
- Display formatter: Output formatting for different analysis types
- Error message formatting and display

### 2. Integration Tests

**Workflow Tests (`test_integration.py`)**
- End-to-end analysis workflows
- Complete user interaction flows
- Error recovery and resilience testing
- Application initialization and component integration

### 3. Mock Data and Fixtures

**Test Fixtures (`test_fixtures.py`)**
- `MockData` class with realistic financial data
- `MockYFinance` class for mocking external API calls
- Standardized test data for consistent testing
- Mock service responses and error scenarios

## Test Features

### Mock Objects
- External API dependencies are mocked using `unittest.mock`
- Realistic mock data based on actual financial data structures
- Configurable mock responses for different test scenarios

### Error Testing
- Network failures and API timeouts
- Invalid data and malformed responses
- Edge cases and boundary conditions
- Graceful error recovery

### Data Validation
- Input validation for all user inputs
- Data type checking and format validation
- Boundary testing for numeric values
- Error message validation

### Integration Testing
- Complete user workflows from start to finish
- Component interaction testing
- Configuration and initialization testing
- Real-world usage scenarios

## Test Coverage

The test suite covers:

✅ **Module Imports** - All modules can be imported successfully  
✅ **Application Initialization** - Main application starts correctly  
✅ **Utility Functions** - All formatting and validation functions  
✅ **Data Services** - Financial data retrieval and processing  
✅ **Analysis Components** - All analyzer classes and methods  
✅ **UI Components** - Menu handling and display formatting  
✅ **Error Handling** - Graceful error recovery and user feedback  
✅ **Integration Workflows** - End-to-end user scenarios  

## Test Requirements

### Dependencies
- Python 3.7+
- unittest (built-in)
- unittest.mock (built-in)
- pandas
- yfinance (for integration tests)

### Mock Strategy
- External API calls are mocked to avoid network dependencies
- Realistic mock data ensures tests reflect real-world scenarios
- Configurable mocks allow testing various success/failure scenarios

## Best Practices

### Test Organization
- Each module has dedicated test file
- Tests are grouped by functionality
- Clear test names describe what is being tested

### Mock Usage
- External dependencies are always mocked
- Mock data is realistic and comprehensive
- Tests don't depend on external services

### Error Testing
- All error paths are tested
- Edge cases and boundary conditions covered
- Graceful error handling verified

### Maintainability
- Tests are independent and can run in any order
- Clear setup and teardown for each test
- Comprehensive documentation and comments

## Continuous Integration

The test suite is designed to run in CI/CD environments:
- No external dependencies required (all mocked)
- Fast execution (no network calls)
- Clear pass/fail reporting
- Detailed error messages for debugging

## Adding New Tests

When adding new functionality:

1. **Add unit tests** for individual functions/methods
2. **Add integration tests** for complete workflows
3. **Update mock data** if new data structures are used
4. **Test error scenarios** and edge cases
5. **Update documentation** to reflect new test coverage

### Example Test Structure
```python
class TestNewFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def test_feature_success(self):
        """Test successful feature operation."""
        pass
    
    def test_feature_error_handling(self):
        """Test feature error handling."""
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass
```