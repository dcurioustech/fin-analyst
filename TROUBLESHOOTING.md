# Troubleshooting Guide - Financial Analysis Bot

This guide provides detailed troubleshooting information for the LangGraph-integrated Financial Analysis Bot, organized by system layer and common issue types.

## 🔍 Quick Diagnostics

### System Health Check
Run this command to verify all components are working:
```bash
python3 test_orchestrator_comprehensive.py
```

### Layer-Specific Tests
```bash
# Test interpreter layer
python3 -c "from agents.interpreter import default_interpreter; print(default_interpreter.interpret_request('Analyze AAPL'))"

# Test tools layer  
python3 -c "from agents.tools import validate_ticker; print(validate_ticker.invoke({'ticker': 'AAPL'}))"

# Test response generation
python3 -c "from agents.response_generator import default_response_generator; print(default_response_generator.generate_welcome_message())"
```

## 🏗️ Layer-Specific Issues

### 1. Interpreter Layer Problems

#### Issue: Wrong Companies Extracted
**Symptoms:**
- Input: "Analyze Apple" → Companies: ['APPLE', 'ANALYZE']
- Input: "Tell me about MSFT" → Companies: ['TELL', 'ME', 'ABOUT', 'MSFT']

**Root Cause:** Overly aggressive regex pattern matching any uppercase words

**Debug Steps:**
```python
from agents.interpreter import default_interpreter
interpretation = default_interpreter.interpret_request("Your problematic input")
print(f"Companies: {interpretation.companies}")
print(f"Analysis type: {interpretation.analysis_type}")
print(f"Confidence: {interpretation.confidence}")
```

**Solutions:**
1. **Immediate Fix**: Use ticker symbols directly (e.g., "AAPL" instead of "Apple")
2. **Long-term Fix**: Update `agents/interpreter.py` regex pattern:
   ```python
   # Current (too aggressive)
   self.ticker_pattern = re.compile(r'\b[A-Z]{1,5}\b')
   
   # Better (more selective)
   self.ticker_pattern = re.compile(r'\b[A-Z]{2,5}\b(?=\s|$|[.,!?])')
   ```

#### Issue: Analysis Type Misidentification
**Symptoms:**
- Comparison requests detected as profile analysis
- Specific analysis types not recognized

**Debug Steps:**
```python
from agents.interpreter import default_interpreter
interpreter = default_interpreter
print("Analysis keywords:", interpreter.analysis_keywords)
```

**Solutions:**
1. Add missing keywords to `analysis_keywords` dictionary
2. Improve keyword matching logic
3. Add context-aware analysis type detection

### 2. Analysis Tools Layer Problems

#### Issue: Tool Execution Failures
**Symptoms:**
```
Error: No data found for ticker 'AAPL'
Tool execution failed: HTTP Error 404
```

**Debug Steps:**
```python
from agents.tools import validate_ticker, get_company_data

# Test ticker validation
result = validate_ticker.invoke({"ticker": "AAPL"})
print(f"Validation result: {result}")

# Test data retrieval
if result.get("valid"):
    data_result = get_company_data.invoke({"ticker": "AAPL"})
    print(f"Data result: {data_result}")
```

**Common Causes & Solutions:**

1. **Network Connectivity Issues**
   - Check internet connection
   - Verify Yahoo Finance API accessibility
   - Solution: Implement retry logic with exponential backoff

2. **Invalid Ticker Symbols**
   - Verify ticker exists and is actively traded
   - Check for delisted or merged companies
   - Solution: Use ticker validation before analysis

3. **API Rate Limiting**
   - Yahoo Finance has rate limits
   - Solution: Implement request throttling and caching

4. **Data Format Changes**
   - Yahoo Finance occasionally changes data structure
   - Solution: Add robust error handling and data validation

#### Issue: Analysis Quality Problems
**Symptoms:**
- Missing fields in analysis results
- Incorrect data types
- Empty or malformed responses

**Debug Steps:**
```python
from agents.tools import analyze_company_profile

result = analyze_company_profile.invoke({"ticker": "AAPL"})
print(f"Success: {result.get('success')}")
print(f"Data structure: {result.get('data', {}).keys()}")
print(f"Basic info: {result.get('data', {}).get('basic_info', {})}")
```

**Solutions:**
1. **Data Validation**: Add input validation to all analysis functions
2. **Error Handling**: Implement graceful degradation for missing data
3. **Data Normalization**: Standardize data formats across all tools

### 3. Response Generation Layer Problems

#### Issue: Malformed Responses
**Symptoms:**
- Empty responses
- Template rendering errors
- Incorrect response format

**Debug Steps:**
```python
from agents.response_generator import default_response_generator, ResponseContext

context = ResponseContext()
context.analysis_type = "profile"
context.companies = ["AAPL"]
context.user_input = "Analyze AAPL"

response = default_response_generator.generate_response(context)
print(f"Response: {response}")
```

**Common Issues & Solutions:**

1. **Missing Analysis Results**
   - Ensure analysis_results are properly populated in context
   - Add fallback templates for missing data

2. **Template Errors**
   - Check template syntax in `agents/response_generator.py`
   - Validate template variables exist in context

3. **Response Context Issues**
   - Verify all required context fields are populated
   - Add context validation before response generation

### 4. State Management Problems

#### Issue: State Corruption
**Symptoms:**
- KeyError exceptions for expected state fields
- Type errors (list expected, got string)
- State inconsistencies between workflow steps

**Debug Steps:**
```python
from agents.state import create_initial_state, update_state_with_user_input

state = create_initial_state()
print(f"Initial state keys: {list(state.keys())}")
print(f"State types: {[(k, type(v)) for k, v in state.items()]}")

updated_state = update_state_with_user_input(state, "Test input")
print(f"Updated state: {updated_state}")
```

**Solutions:**
1. **State Validation**: Add type checking for all state updates
2. **Immutable Updates**: Use proper state copying to avoid mutations
3. **Default Values**: Ensure all state fields have proper defaults

### 5. LangGraph Orchestrator Problems

#### Issue: Workflow Execution Failures
**Symptoms:**
```
ModuleNotFoundError: No module named 'langgraph'
Workflow execution stopped unexpectedly
Node routing errors
```

**Debug Steps:**
```python
# Check if LangGraph is available
try:
    from langgraph.graph import StateGraph
    print("LangGraph available")
except ImportError as e:
    print(f"LangGraph not available: {e}")

# Test orchestrator initialization
try:
    from agents.graph import financial_orchestrator
    print("Orchestrator initialized successfully")
except Exception as e:
    print(f"Orchestrator initialization failed: {e}")
```

**Solutions:**

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Node Routing Issues**
   - Check conditional edge logic in `agents/nodes.py`
   - Verify all routing functions return valid node names
   - Add logging to track workflow execution

3. **State Compatibility**
   - Ensure state schema matches LangGraph requirements
   - Verify all nodes properly handle state updates

## 🚨 Common Error Patterns

### 1. Import and Dependency Errors

#### Error: `ModuleNotFoundError: No module named 'langgraph'`
**Solution:**
```bash
# Install in virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Error: `ImportError: cannot import name 'X' from 'Y'`
**Solution:**
- Check for circular imports
- Verify module structure
- Update import paths if modules were moved

### 2. Data and API Errors

#### Error: `HTTP Error 429: Too Many Requests`
**Solution:**
```python
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "429" in str(e) and attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
                continue
            raise e
```

#### Error: `KeyError: 'longName'` or similar data field errors
**Solution:**
```python
def safe_get(data, key, default='N/A'):
    """Safely get data with fallback."""
    return data.get(key, default) if data else default

# Usage
company_name = safe_get(company_info, 'longName', 'Unknown Company')
```

### 3. Configuration and Environment Errors

#### Error: Missing environment variables
**Solution:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("Warning: GOOGLE_API_KEY not found. LLM features will be disabled.")
```

## 🔧 Performance Optimization

### 1. Slow Response Times

**Diagnosis:**
```python
import time
import logging

# Add timing to identify bottlenecks
start_time = time.time()
result = some_analysis_function()
end_time = time.time()
logging.info(f"Analysis took {end_time - start_time:.2f} seconds")
```

**Solutions:**
1. **Implement Caching**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def cached_company_data(ticker):
       return expensive_data_fetch(ticker)
   ```

2. **Batch API Requests**
   ```python
   def batch_ticker_validation(tickers):
       # Validate multiple tickers in single request
       pass
   ```

3. **Async Processing**
   ```python
   import asyncio
   
   async def async_analysis(ticker):
       # Non-blocking analysis
       pass
   ```

### 2. Memory Usage Issues

**Diagnosis:**
```python
import psutil
import os

process = psutil.Process(os.getpid())
memory_usage = process.memory_info().rss / 1024 / 1024  # MB
print(f"Memory usage: {memory_usage:.2f} MB")
```

**Solutions:**
1. **Data Streaming**: Process large datasets in chunks
2. **Memory Cleanup**: Explicitly delete large objects
3. **Lazy Loading**: Load data only when needed

## 🧪 Testing and Validation

### Automated Testing
```bash
# Run all tests with verbose output
python3 -m pytest tests/ -v

# Run specific test categories
python3 test_orchestrator_comprehensive.py  # Core components
python3 test_error_handling.py              # Error scenarios  
python3 test_integration_flow.py            # Integration tests
```

### Manual Testing Checklist

#### Basic Functionality
- [ ] Chat interface starts without errors
- [ ] Valid ticker analysis works (e.g., "Analyze AAPL")
- [ ] Company comparison works (e.g., "Compare AAPL MSFT")
- [ ] Error handling for invalid tickers
- [ ] Help command works

#### Edge Cases
- [ ] Empty input handling
- [ ] Very long input handling
- [ ] Special characters in input
- [ ] Network disconnection recovery
- [ ] API rate limit handling

#### Performance
- [ ] Response time < 10 seconds for simple queries
- [ ] Memory usage stable over multiple queries
- [ ] No memory leaks during extended usage

## 📞 Getting Help

### Debug Information Collection
When reporting issues, include:

1. **System Information**
   ```bash
   python3 --version
   pip list | grep -E "(langgraph|langchain|pandas|yfinance)"
   ```

2. **Error Logs**
   ```bash
   # Enable debug logging
   export LOG_LEVEL=DEBUG
   python3 chat_interface.py 2>&1 | tee debug.log
   ```

3. **Test Results**
   ```bash
   python3 test_orchestrator_comprehensive.py > test_results.txt 2>&1
   ```

### Support Channels
- **GitHub Issues**: For bugs and feature requests
- **Documentation**: Check README.md and ARCHITECTURE.md
- **Code Comments**: Inline documentation in source files

### Self-Help Resources
1. **Code Examples**: See `tests/` directory for usage examples
2. **Architecture Guide**: `ARCHITECTURE.md` for system design
3. **API Documentation**: Docstrings in all modules
4. **Test Cases**: Comprehensive test suites show expected behavior

---

**Remember**: Most issues can be resolved by checking logs, validating inputs, and ensuring all dependencies are properly installed. When in doubt, run the test suites to identify the specific component causing problems.