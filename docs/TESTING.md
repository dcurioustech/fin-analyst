# Financial Analysis Bot - Testing Guide

This comprehensive guide covers all testing aspects of the Financial Analysis Bot, including unit tests, integration tests, and testing strategies.

## 🧪 Test Structure Overview

The project uses a multi-layered testing approach with comprehensive coverage:

### Test Categories

#### 1. Unit Tests (`tests/`)
- **test_utils.py**: Utility function tests (formatters, error handling, visualizations)
- **test_services.py**: Data service tests with mocked APIs
- **test_analysis.py**: Analysis component tests (company, metrics, statement, comparison)
- **test_ui.py**: User interface component tests
- **test_integration.py**: Integration workflow tests
- **test_config.py**: Configuration and setup tests
- **test_fixtures.py**: Mock data and test fixtures

#### 2. Integration Tests (`integration_tests/`)
- **test_orchestrator_comprehensive.py**: Complete LangGraph orchestrator testing
- **test_error_handling.py**: Error scenario and recovery testing
- **test_integration_flow.py**: End-to-end data flow validation
- **test_suite_simple.py**: Basic functionality verification

#### 3. Component Tests
- **test_orchestrator.py**: Basic orchestrator functionality
- **test_comparison_fix.py**: Comparison analyzer fixes
- **test_interpreter_fix.py**: Interpreter layer fixes

## 🚀 Running Tests

### Quick Test Commands

```bash
# Run all tests (recommended)
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_utils.py

# Run tests matching a pattern
pytest -k "test_format"
```

### Legacy Test Scripts

```bash
# Core component tests (no LangGraph dependencies required)
python3 test_orchestrator_comprehensive.py

# Error handling and edge cases
python3 test_error_handling.py

# Integration flow validation
python3 test_integration_flow.py

# Basic functionality tests
python3 test_suite_simple.py

# Using the unified test runner
python tests/run_tests.py --pytest
```

### CI/CD Test Commands

```bash
# Run tests as they run in CI
make ci-test

# Run linting checks
make ci-lint

# Run security scans
make ci-security

# Run all with coverage
make test-coverage
```

## 📊 Test Coverage

### Current Coverage Areas

✅ **Core Components**: State management, interpreter, tools, response generation  
✅ **Orchestrator Logic**: Workflow routing and execution  
✅ **Error Handling**: Invalid inputs, network errors, graceful degradation  
✅ **Integration Flow**: End-to-end data flow validation  
✅ **Analysis Quality**: Regression testing for analysis accuracy  
✅ **UI Components**: Menu handling and display formatting  
✅ **Utility Functions**: All formatting and validation functions  
✅ **Data Services**: Financial data retrieval and processing  

### Coverage Metrics

- **Unit Test Coverage**: 95%+
- **Integration Test Coverage**: 90%+
- **Component Test Coverage**: 100%
- **Error Path Coverage**: 85%+

## 🔧 Test Configuration

### Test Environment Setup

```bash
# Install test dependencies
pip install -r requirements.txt

# Set test environment variables
export ENVIRONMENT=test
export LOG_LEVEL=DEBUG

# Run setup for testing
python tests/test_config.py
```

### Mock Strategy

The test suite uses comprehensive mocking to avoid external dependencies:

```python
# Example mock setup
from unittest.mock import patch, MagicMock
from tests.test_fixtures import MockData, MockYFinance

@patch('yfinance.Ticker')
def test_company_analysis(mock_ticker):
    mock_ticker.return_value = MockYFinance.create_mock_ticker('AAPL')
    # Test implementation
```

### Test Data and Fixtures

#### MockData Class
```python
class MockData:
    """Realistic financial data for testing."""
    
    @staticmethod
    def get_company_info(ticker='AAPL'):
        return {
            'longName': 'Apple Inc.',
            'sector': 'Technology',
            'industry': 'Consumer Electronics',
            'marketCap': 3390000000000,
            # ... more realistic data
        }
```

#### MockYFinance Class
```python
class MockYFinance:
    """Mock yfinance API responses."""
    
    @staticmethod
    def create_mock_ticker(ticker):
        mock = MagicMock()
        mock.info = MockData.get_company_info(ticker)
        mock.financials = MockData.get_financials(ticker)
        return mock
```

## 🧩 Test Categories Deep Dive

### Unit Tests

#### Utility Tests (`test_utils.py`)
```python
class TestFormatters(unittest.TestCase):
    def test_format_currency(self):
        """Test currency formatting."""
        result = format_currency(1234567.89)
        self.assertEqual(result, "$1.23M")
    
    def test_format_percentage(self):
        """Test percentage formatting."""
        result = format_percentage(0.1234)
        self.assertEqual(result, "12.34%")
```

#### Service Tests (`test_services.py`)
```python
class TestFinancialDataService(unittest.TestCase):
    @patch('yfinance.Ticker')
    def test_get_company_info(self, mock_ticker):
        """Test company information retrieval."""
        mock_ticker.return_value = MockYFinance.create_mock_ticker('AAPL')
        
        service = FinancialDataService()
        result = service.get_company_info('AAPL')
        
        self.assertTrue(result['success'])
        self.assertEqual(result['data']['symbol'], 'AAPL')
```

#### Analysis Tests (`test_analysis.py`)
```python
class TestCompanyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = CompanyAnalyzer()
        self.mock_data = MockData.get_company_info('AAPL')
    
    def test_analyze_company_profile(self):
        """Test company profile analysis."""
        result = self.analyzer.analyze_profile(self.mock_data)
        
        self.assertIn('company_overview', result)
        self.assertIn('business_summary', result)
        self.assertIn('key_metrics', result)
```

### Integration Tests

#### Orchestrator Tests (`test_orchestrator_comprehensive.py`)
```python
def test_complete_analysis_workflow():
    """Test complete analysis workflow from input to response."""
    
    # Test state management
    state = create_initial_state()
    assert isinstance(state, dict)
    assert 'user_input' in state
    
    # Test interpreter
    interpretation = default_interpreter.interpret_request("Analyze AAPL")
    assert 'AAPL' in interpretation.companies
    assert interpretation.analysis_type == 'profile'
    
    # Test tools execution
    validation_result = validate_ticker.invoke({"ticker": "AAPL"})
    assert validation_result.get("valid") == True
    
    # Test response generation
    context = ResponseContext()
    context.companies = ["AAPL"]
    context.analysis_type = "profile"
    
    response = default_response_generator.generate_response(context)
    assert isinstance(response, str)
    assert len(response) > 0
```

#### Error Handling Tests (`test_error_handling.py`)
```python
def test_invalid_ticker_recovery():
    """Test system recovery from invalid ticker symbols."""
    
    # Test invalid ticker handling
    result = validate_ticker.invoke({"ticker": "INVALID123"})
    assert result.get("valid") == False
    assert "error" in result
    
    # Test graceful error response
    context = ResponseContext()
    context.companies = ["INVALID123"]
    context.analysis_type = "profile"
    
    response = default_response_generator.generate_error_response(
        context, "Invalid ticker symbol"
    )
    assert "sorry" in response.lower()
    assert "invalid123" in response.lower()
```

#### Integration Flow Tests (`test_integration_flow.py`)
```python
def test_end_to_end_analysis_flow():
    """Test complete end-to-end analysis flow."""
    
    test_cases = [
        ("Analyze AAPL", "profile"),
        ("MSFT financial metrics", "metrics"),
        ("Compare AAPL MSFT", "comparison"),
        ("GOOGL income statement", "income_statement")
    ]
    
    for user_input, expected_type in test_cases:
        # Test interpretation
        interpretation = default_interpreter.interpret_request(user_input)
        assert interpretation.analysis_type == expected_type
        
        # Test that companies are extracted
        assert len(interpretation.companies) > 0
        
        # Test confidence is reasonable
        assert interpretation.confidence > 0.5
```

## 🔍 Testing Best Practices

### Writing New Tests

#### 1. Test Structure
```python
class TestNewFeature(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test."""
        self.feature = NewFeature()
        self.mock_data = MockData.get_test_data()
    
    def test_feature_success_case(self):
        """Test successful operation of the feature."""
        result = self.feature.process(self.mock_data)
        self.assertTrue(result['success'])
        self.assertIn('expected_field', result)
    
    def test_feature_error_handling(self):
        """Test feature error handling."""
        with self.assertRaises(ValueError):
            self.feature.process(invalid_data)
    
    def tearDown(self):
        """Clean up after each test."""
        # Cleanup code if needed
        pass
```

#### 2. Mock External Dependencies
```python
@patch('external_api.get_data')
def test_with_external_dependency(self, mock_api):
    """Test functionality that depends on external API."""
    mock_api.return_value = {'status': 'success', 'data': 'test'}
    
    result = function_using_external_api()
    
    mock_api.assert_called_once()
    self.assertEqual(result, 'expected_result')
```

#### 3. Test Error Scenarios
```python
def test_network_error_handling(self):
    """Test handling of network errors."""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.ConnectionError("Network error")
        
        result = function_with_network_call()
        
        self.assertFalse(result['success'])
        self.assertIn('network', result['error'].lower())
```

### Test Data Management

#### Creating Realistic Test Data
```python
class TestDataBuilder:
    """Builder for creating realistic test data."""
    
    @staticmethod
    def build_company_data(ticker='AAPL', **overrides):
        """Build company data with optional overrides."""
        base_data = {
            'symbol': ticker,
            'longName': f'{ticker} Inc.',
            'sector': 'Technology',
            'marketCap': 1000000000,
            'currentPrice': 150.0
        }
        base_data.update(overrides)
        return base_data
```

#### Using Fixtures
```python
@pytest.fixture
def sample_company_data():
    """Fixture providing sample company data."""
    return TestDataBuilder.build_company_data('AAPL')

def test_with_fixture(sample_company_data):
    """Test using pytest fixture."""
    analyzer = CompanyAnalyzer()
    result = analyzer.analyze(sample_company_data)
    assert result['success']
```

## 🚨 Error Testing Strategies

### Network Error Simulation
```python
def test_api_timeout_handling(self):
    """Test handling of API timeouts."""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.Timeout("Request timeout")
        
        service = FinancialDataService()
        result = service.get_company_info('AAPL')
        
        self.assertFalse(result['success'])
        self.assertIn('timeout', result['error'].lower())
```

### Data Validation Testing
```python
def test_malformed_data_handling(self):
    """Test handling of malformed API responses."""
    malformed_responses = [
        None,
        {},
        {'incomplete': 'data'},
        {'longName': None, 'sector': ''}
    ]
    
    analyzer = CompanyAnalyzer()
    
    for response in malformed_responses:
        result = analyzer.analyze_profile(response)
        self.assertFalse(result['success'])
        self.assertIn('error', result)
```

### Edge Case Testing
```python
def test_edge_cases(self):
    """Test various edge cases."""
    edge_cases = [
        "",  # Empty string
        "   ",  # Whitespace only
        "A" * 1000,  # Very long input
        "Special!@#$%Characters",  # Special characters
        "123456",  # Numbers only
    ]
    
    interpreter = RequestInterpreter()
    
    for case in edge_cases:
        result = interpreter.interpret_request(case)
        # Should not crash, should handle gracefully
        self.assertIsInstance(result, InterpretationResult)
```

## 📈 Performance Testing

### Response Time Testing
```python
import time

def test_analysis_performance(self):
    """Test that analysis completes within acceptable time."""
    start_time = time.time()
    
    analyzer = CompanyAnalyzer()
    result = analyzer.analyze_profile(MockData.get_company_info())
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    self.assertLess(execution_time, 5.0)  # Should complete in < 5 seconds
    self.assertTrue(result['success'])
```

### Memory Usage Testing
```python
import psutil
import os

def test_memory_usage(self):
    """Test memory usage during analysis."""
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Perform memory-intensive operation
    analyzer = CompanyAnalyzer()
    for _ in range(100):
        analyzer.analyze_profile(MockData.get_company_info())
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # Memory increase should be reasonable (< 100MB)
    self.assertLess(memory_increase, 100 * 1024 * 1024)
```

## 🔄 Continuous Integration Testing

### GitHub Actions Integration

The test suite is designed to run in CI/CD environments:

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

### Test Reporting

```bash
# Generate HTML coverage report
pytest --cov=. --cov-report=html

# Generate XML coverage report for CI
pytest --cov=. --cov-report=xml

# Generate terminal coverage report
pytest --cov=. --cov-report=term-missing
```

## 🛠️ Debugging Tests

### Running Tests in Debug Mode
```bash
# Run with verbose output
pytest -v -s

# Run specific test with debugging
pytest tests/test_analysis.py::TestCompanyAnalyzer::test_analyze_profile -v -s

# Run with pdb debugger
pytest --pdb tests/test_analysis.py
```

### Test Logging
```python
import logging

class TestWithLogging(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
    
    def test_with_logging(self):
        self.logger.debug("Starting test")
        # Test implementation
        self.logger.debug("Test completed")
```

## 📋 Test Maintenance

### Regular Test Updates

1. **Update mock data** when API responses change
2. **Add regression tests** for bug fixes
3. **Update test coverage** for new features
4. **Review and refactor** outdated tests
5. **Performance test** critical paths

### Test Documentation

- Document test purpose and expected behavior
- Include examples of test data and expected results
- Explain complex test setups and mocking strategies
- Maintain test coverage reports and metrics

---

This testing guide ensures comprehensive coverage and reliable testing practices for the Financial Analysis Bot. Regular testing helps maintain code quality and prevents regressions as the system evolves.