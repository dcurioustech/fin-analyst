# Financial Analysis Bot - Quick Reference

A comprehensive cheat sheet for commands, examples, and troubleshooting.

## 🚀 Quick Start Commands

```bash
# Installation
pip install -r requirements.txt

# Start interfaces
python3 chat_interface.py    # Interactive chat (recommended)
python3 web_app.py          # Web interface
python3 main.py             # Menu interface

# Basic analysis
> Analyze AAPL
> Compare AAPL MSFT
> TSLA financial metrics
```

## 💬 Chat Commands

| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show help and examples | `help` |
| `clear` | Clear conversation history | `clear` |
| `exit`, `quit`, `bye` | Exit application | `exit` |

## 📊 Analysis Types & Examples

### Company Profile Analysis
```bash
# Basic formats
> Analyze AAPL
> Tell me about Microsoft
> TSLA profile
> What can you tell me about Google?

# What you get: Company overview, business summary, market info, key metrics
```

### Financial Metrics Analysis
```bash
# Metrics queries
> AAPL financial metrics
> Show me Tesla's ratios
> Microsoft valuation metrics
> Google profitability analysis

# What you get: P/E, P/B, ROE, ROA, profit margins, growth rates
```

### Financial Statements
```bash
# Statement analysis
> AAPL income statement
> Google earnings analysis
> MSFT balance sheet
> Apple cash flow
> Tesla financial statements

# What you get: Revenue, expenses, assets, liabilities, cash flows
```

### Company Comparison
```bash
# Comparison formats
> Compare AAPL and MSFT
> Tesla vs Ford
> Apple versus Microsoft
> Compare AAPL MSFT GOOGL

# What you get: Side-by-side metrics, relative analysis, investment insights
```

## 🎯 Query Patterns

### ✅ Recommended Patterns
```bash
# Use ticker symbols (most reliable)
> AAPL profile
> AAPL metrics
> Compare AAPL MSFT

# Be specific about analysis type
> AAPL income statement
> MSFT balance sheet
> GOOGL cash flow

# Use context effectively
> Analyze AAPL
> What about the debt ratios?
> How does it compare to Microsoft?
```

### ❌ Patterns to Avoid
```bash
# Too vague
> Tell me about stocks
> Analyze financials

# Overly complex company names
> Apple Computer Inc profile
> Microsoft Corporation metrics

# Ambiguous comparisons
> Compare Apple with that tech company
```

## 🔧 Environment Variables

### Required
```bash
# Basic setup
GOOGLE_API_KEY=your_google_api_key_here

# Development
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

### Optional
```bash
# Additional data sources
ALPHA_VANTAGE_API_KEY=your_key_here
POLYGON_API_KEY=your_key_here

# GCP deployment
PROJECT_ID=your-gcp-project-id
REGION=us-central1

# Application settings
PORT=8080
```

## 🌐 API Endpoints

### Web Interface Endpoints
```bash
GET  /                           # Web chat interface
GET  /health                     # Health check
POST /api/chat                   # Chat API
GET  /api/sessions/{session_id}  # Session info
DELETE /api/sessions/{session_id} # Clear session
```

### API Usage Example
```python
import requests

# Chat API
response = requests.post('http://localhost:8080/api/chat', json={
    'message': 'Analyze Tesla',
    'session_id': 'my-session'
})

data = response.json()
print(data['response'])
```

## 🧪 Testing Commands

### Run Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=. --cov-report=term-missing

# Specific tests
pytest tests/test_utils.py -v
python3 test_orchestrator_comprehensive.py

# CI tests
make ci-test
```

### Test Categories
- **Unit Tests**: `tests/test_*.py`
- **Integration Tests**: `integration_tests/test_*.py`
- **Component Tests**: `test_orchestrator_comprehensive.py`
- **Error Tests**: `test_error_handling.py`

## 🚨 Common Issues & Quick Fixes

### Installation Issues

#### Missing Dependencies
```bash
# Error: ModuleNotFoundError: No module named 'langgraph'
# Fix:
pip install -r requirements.txt
```

#### Python Version
```bash
# Error: Syntax errors or import issues
# Fix: Use Python 3.8+
python3 --version
```

### Analysis Issues

#### Company Not Found
```bash
# Error: "I couldn't identify any companies in your request"
# Fix: Use ticker symbols
> Analyze XYZ  # Instead of "XYZ Corp"
```

#### Invalid Ticker
```bash
# Error: "Ticker 'INVALID' not found"
# Fix: Verify ticker on Yahoo Finance
# Use: AAPL, MSFT, GOOGL, TSLA, etc.
```

#### No Data Available
```bash
# Error: "No data available for ticker"
# Reason: Private company or delisted stock
# Fix: Use publicly traded companies only
```

### Performance Issues

#### Slow Responses
```bash
# Causes: Network latency, API limits
# Fixes:
- Wait for current analysis to complete
- Use ticker symbols instead of company names
- Check internet connection
```

#### Memory Issues
```bash
# Cause: Extended sessions
# Fix: Clear context periodically
> clear
```

### Network Issues

#### API Rate Limits
```bash
# Error: HTTP Error 429: Too Many Requests
# Fix: Wait a few minutes, system has retry logic
```

#### Connection Errors
```bash
# Error: HTTP Error 404/Connection failed
# Fixes:
- Check internet connection
- Verify Yahoo Finance API accessibility
- Try again in a few minutes
```

## 🔍 Debugging Commands

### System Health Check
```bash
# Verify all components
python3 test_orchestrator_comprehensive.py

# Test individual layers
python3 -c "from agents.interpreter import default_interpreter; print(default_interpreter.interpret_request('Analyze AAPL'))"
python3 -c "from agents.tools import validate_ticker; print(validate_ticker.invoke({'ticker': 'AAPL'}))"
```

### Enable Debug Logging
```bash
# Environment variable
export LOG_LEVEL=DEBUG
python3 chat_interface.py

# Or in .env file
LOG_LEVEL=DEBUG
```

### Check Configuration
```bash
# Verify environment setup
python3 -c "import os; print('API Key:', 'SET' if os.getenv('GOOGLE_API_KEY') else 'NOT SET')"

# Check dependencies
pip list | grep -E "(langgraph|langchain|pandas|yfinance)"
```

## 📈 Example Analysis Workflows

### Basic Company Research
```bash
1. > Analyze AAPL                    # Get overview
2. > Show me the financial metrics   # Check ratios
3. > What about the income statement # Revenue analysis
4. > How's the cash flow?           # Liquidity check
```

### Competitive Analysis
```bash
1. > Compare AAPL MSFT              # Direct comparison
2. > Which one is more profitable?  # Follow-up question
3. > What about growth prospects?   # Future outlook
4. > Show me their debt levels      # Risk assessment
```

### Sector Analysis
```bash
1. > Compare AAPL MSFT GOOGL AMZN   # Tech giants
2. > Analyze TSLA                   # EV leader
3. > Compare TSLA F GM              # Auto sector
4. > clear                          # Reset for new sector
5. > Compare JPM BAC WFC            # Banking sector
```

## 🎨 Advanced Usage Tips

### Context Management
```bash
# The bot remembers context within a session
> Analyze AAPL
> What about its revenue?           # "its" = Apple
> Compare it with Microsoft         # "it" = Apple
> clear                            # Reset context
```

### Batch Analysis
```bash
# Multiple companies at once
> Compare AAPL MSFT GOOGL AMZN

# Sequential analysis
> Analyze AAPL
> Now MSFT
> Now GOOGL
```

### Specific Metrics Focus
```bash
# Target specific areas
> AAPL debt ratios
> MSFT profitability metrics
> GOOGL growth rates
> TSLA valuation metrics
```

## 🔧 Configuration Files

### .env File Template
```bash
# Copy from .env.example and customize
cp .env.example .env

# Required settings
GOOGLE_API_KEY=your_key_here
ENVIRONMENT=development
LOG_LEVEL=INFO

# Optional settings
ALPHA_VANTAGE_API_KEY=optional
POLYGON_API_KEY=optional
PROJECT_ID=your-gcp-project
REGION=us-central1
PORT=8080
```

### Development vs Production
```bash
# Development
ENVIRONMENT=development
LOG_LEVEL=DEBUG

# Production
ENVIRONMENT=production
LOG_LEVEL=INFO
PROJECT_ID=your-gcp-project
```

## 📚 Documentation Links

- **[User Guide](USER_GUIDE.md)** - Complete usage instructions
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Technical details and architecture
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment
- **[Testing Guide](docs/TESTING.md)** - Comprehensive testing information
- **[CI/CD Guide](docs/CI_CD.md)** - Continuous integration setup

## 🆘 Getting Help

### Built-in Help
```bash
> help                             # Show available commands
```

### Documentation
1. Check this Quick Reference first
2. Read the [User Guide](USER_GUIDE.md) for detailed usage
3. Check [Developer Guide](DEVELOPER_GUIDE.md) for technical issues
4. Review error logs with `LOG_LEVEL=DEBUG`

### Support Channels
- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Comprehensive guides and examples
- **Code Comments**: Inline documentation in source files

### Self-Help Checklist
- [ ] Check internet connection
- [ ] Verify dependencies installed (`pip install -r requirements.txt`)
- [ ] Use valid ticker symbols (AAPL, MSFT, etc.)
- [ ] Check API key configuration
- [ ] Try clearing context (`> clear`)
- [ ] Restart the application
- [ ] Check logs with debug logging enabled

---

## 📚 Related Documentation

- **[README](README.md)** - Project overview and quick start
- **[User Guide](USER_GUIDE.md)** - Complete usage instructions
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Technical details and contributing
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment
- **[API Documentation](docs/API.md)** - Programmatic access

**Quick Tip**: When in doubt, use `> help` for examples and `> clear` to reset context! 🚀