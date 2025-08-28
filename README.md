# Financial Analysis Bot with LangGraph Integration

![Test Suite](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Test%20Suite/badge.svg)
![CI/CD Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI%2FCD%20Pipeline/badge.svg)
[![Coverage](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO)

A sophisticated financial analysis tool that combines rule-based analysis with an orchestrated LangGraph workflow for intelligent financial data processing and insights.

## 🚀 Features

### Core Analysis Capabilities
- **Company Profile Analysis**: Comprehensive company information, sector analysis, and business summaries
- **Financial Metrics Analysis**: Key financial ratios, valuation metrics, and performance indicators  
- **Financial Statements Analysis**: Income statement, balance sheet, and cash flow analysis
- **Company Comparison**: Side-by-side comparison of multiple companies with peer analysis
- **Real-time Data**: Live financial data from Yahoo Finance API

### LangGraph Orchestrator Architecture
- **Intelligent Request Interpretation**: Rule-based parsing with future LLM integration capability
- **Orchestrated Workflow**: Multi-step analysis pipeline with state management
- **Layer Separation**: Clean separation between interpretation, analysis, data services, and response generation
- **Error Handling**: Comprehensive error recovery and graceful degradation
- **Extensible Design**: Hybrid architecture ready for LLM enhancement

## 🏗️ Architecture Overview

The application follows a layered orchestrator-driven architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    Chat Interface                           │
│                 (User Interaction)                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                LangGraph Orchestrator                       │
│              (Workflow Management)                          │
└─┬─────────────┬─────────────┬─────────────┬─────────────────┘
  │             │             │             │
  ▼             ▼             ▼             ▼
┌─────────┐ ┌─────────┐ ┌─────────────┐ ┌─────────────┐
│Interpret│ │Analysis │ │Data Services│ │Response Gen │
│  Layer  │ │  Tools  │ │   Layer     │ │   Layer     │
└─────────┘ └─────────┘ └─────────────┘ └─────────────┘
```

### Layer Responsibilities

1. **Interpreter Layer**: Parses user requests, extracts companies and analysis types
2. **Analysis Tools Layer**: Wraps existing analysis functions for orchestrator consumption  
3. **Data Services Layer**: Handles financial data retrieval and caching
4. **Response Generation Layer**: Formats analysis results into user-friendly responses
5. **LangGraph Orchestrator**: Manages workflow, state, and coordination between layers

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip or conda package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd financial-analysis-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment (optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your Google API key for future LLM features
   ```

## 🚀 Usage

### Interactive Chat Interface

Start the interactive chat interface for conversational financial analysis:

```bash
python3 chat_interface.py
```

**Example interactions:**
```
> Analyze AAPL
> Compare Apple and Microsoft  
> Show me TSLA financial metrics
> What's Google's revenue trend?
```

### Direct Analysis (Legacy)

Run direct analysis using the original interface:

```bash
python3 main.py
```

### Programmatic Usage

```python
from agents.graph import financial_orchestrator

# Start a conversation
state = financial_orchestrator.start_conversation()
print(state['agent_response'])

# Process user requests
result = financial_orchestrator.process_user_request("Analyze AAPL", state)
print(result['agent_response'])
```

## 🧪 Testing

The project includes comprehensive test suites with both pytest and unittest support:

### Run All Tests with pytest (Recommended)
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=html --cov-report=term-missing

# Run specific test file
pytest tests/test_utils.py

# Run tests matching a pattern
pytest -k "test_format"

# Using the convenience script
python run_pytest.py

# Using Makefile
make test
make test-verbose
make test-coverage
```

### Alternative: Legacy Test Scripts
```bash
# Core component tests (no LangGraph dependencies required)
python3 test_orchestrator_comprehensive.py

# Error handling and edge cases
python3 test_error_handling.py

# Integration flow validation
python3 test_integration_flow.py

# Legacy analysis tests
python3 test_suite_simple.py

# Using the unified test runner
python tests/run_tests.py --pytest
```

### Test Coverage
- ✅ **Core Components**: State management, interpreter, tools, response generation
- ✅ **Orchestrator Logic**: Workflow routing and execution
- ✅ **Error Handling**: Invalid inputs, network errors, graceful degradation
- ✅ **Integration Flow**: End-to-end data flow validation
- ✅ **Analysis Quality**: Regression testing for analysis accuracy

## 📊 Supported Analysis Types

| Analysis Type | Description | Example Input |
|---------------|-------------|---------------|
| **Company Profile** | Basic company information, sector, business summary | "Analyze AAPL", "Tell me about Microsoft" |
| **Financial Metrics** | Key ratios, valuation metrics, performance indicators | "AAPL metrics", "Show me Tesla's ratios" |
| **Income Statement** | Revenue, expenses, profit analysis | "AAPL income statement", "Google earnings" |
| **Balance Sheet** | Assets, liabilities, equity analysis | "MSFT balance sheet" |
| **Cash Flow** | Operating, investing, financing cash flows | "AAPL cash flow" |
| **Company Comparison** | Side-by-side analysis of multiple companies | "Compare AAPL and MSFT", "Tesla vs Ford" |

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Google Gemini API Configuration (for future LLM features)
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Specify Gemini model (default: gemini-pro)
GEMINI_MODEL=gemini-pro

# Optional: Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
```

### Customization

- **Add new analysis types**: Extend `agents/interpreter.py` and `agents/tools.py`
- **Modify response templates**: Update `agents/response_generator.py`
- **Add new data sources**: Extend `services/financial_data_service.py`
- **Customize orchestrator workflow**: Modify `agents/graph.py` and `agents/nodes.py`

## 🔄 CI/CD and Development

### Continuous Integration

This project uses GitHub Actions for automated testing and deployment:

- **Test Suite**: Runs on every push and pull request
- **Code Quality**: Automated linting and formatting checks  
- **Security Scanning**: Vulnerability detection with bandit and safety
- **Python 3.12**: Latest Python version compatibility
- **Coverage Reporting**: Automated coverage analysis

### Development Commands

```bash
# Run tests as they run in CI
make ci-test

# Run linting checks
make ci-lint

# Run security scans
make ci-security

# Build Docker image
make docker-build

# Run container locally
make docker-run
```

### GitHub Workflows

- **`test.yml`**: Fast test execution for immediate feedback
- **`pr-check.yml`**: Pull request validation
- **`ci.yml`**: Comprehensive CI pipeline
- **`release.yml`**: Automated deployment to production

For detailed CI/CD setup instructions, see [docs/CI_CD_SETUP.md](docs/CI_CD_SETUP.md).

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
ModuleNotFoundError: No module named 'langgraph'
```
**Solution**: Install dependencies with `pip install -r requirements.txt`

#### 2. API Rate Limits
```bash
HTTP Error 429: Too Many Requests
```
**Solution**: The system includes automatic retry logic. Wait a few minutes and try again.

#### 3. Invalid Ticker Symbols
```bash
No data found for ticker 'INVALID'
```
**Solution**: Use valid ticker symbols (e.g., AAPL, MSFT, GOOGL). The system will suggest corrections.

#### 4. Network Connectivity
```bash
HTTP Error 404: Not Found
```
**Solution**: Check internet connection. The system gracefully handles network errors.

### Layer-Specific Debugging

#### Interpreter Layer Issues
- **Problem**: Wrong companies extracted from input
- **Debug**: Check `agents/interpreter.py` company mappings and regex patterns
- **Solution**: Add company names to the mapping dictionary

#### Analysis Tools Issues  
- **Problem**: Analysis fails with valid ticker
- **Debug**: Test individual tools in `agents/tools.py`
- **Solution**: Check data service connectivity and error handling

#### Response Generation Issues
- **Problem**: Malformed or empty responses
- **Debug**: Check `agents/response_generator.py` templates
- **Solution**: Verify analysis results structure and template formatting

#### State Management Issues
- **Problem**: State corruption or missing fields
- **Debug**: Check `agents/state.py` state updates
- **Solution**: Ensure proper state initialization and field validation

### Performance Optimization

- **Caching**: Financial data is cached to reduce API calls
- **Batch Processing**: Multiple requests are batched when possible
- **Error Recovery**: Failed requests are retried with exponential backoff
- **Memory Management**: Large datasets are processed in chunks

## 🔮 Future Enhancements

### Planned Features
- **LLM Integration**: Full Gemini model integration for natural language processing
- **Advanced Analytics**: Technical analysis, sentiment analysis, news integration
- **Portfolio Management**: Portfolio tracking and optimization features
- **Real-time Alerts**: Price alerts and news notifications
- **Web Interface**: Browser-based UI for easier access
- **API Endpoints**: REST API for programmatic access

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Yahoo Finance API** for providing financial data
- **LangGraph** for orchestrator workflow capabilities
- **LangChain** for LLM integration framework
- **Pandas** for data manipulation and analysis

---

**Note**: This application is for educational and research purposes. Always consult with financial professionals before making investment decisions.