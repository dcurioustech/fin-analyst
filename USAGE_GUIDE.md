# Usage Guide - LangGraph Financial Analysis Bot

This guide provides comprehensive instructions for using the Financial Analysis Bot's chat interface and understanding the orchestrator workflow.

## 🚀 Getting Started

### Quick Start
1. **Install dependencies**: `pip install -r requirements.txt`
2. **Start chat interface**: `python3 chat_interface.py`
3. **Begin analyzing**: Type your financial analysis requests

### First Steps
```bash
$ python3 chat_interface.py

🤖 Financial Analysis Assistant
==============================

Hello! I'm your Financial Analysis Assistant. I can help you analyze companies, 
compare stocks, and provide financial insights.

Available commands:
• help - Show available commands and examples
• clear - Clear conversation history  
• exit/quit/bye - Exit the application

What would you like to analyze today?

> Analyze AAPL
```

## 💬 Chat Interface Commands

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show help and examples | `help` |
| `clear` | Clear conversation history | `clear` |
| `exit`, `quit`, `bye` | Exit the application | `exit` |

### Analysis Commands

#### Single Company Analysis
```bash
# Basic company analysis
> Analyze AAPL
> Tell me about Microsoft
> TSLA profile

# Specific analysis types
> AAPL financial metrics
> Google income statement
> MSFT balance sheet
> Apple cash flow
```

#### Company Comparison
```bash
# Compare two companies
> Compare AAPL and MSFT
> TSLA vs F
> Apple versus Microsoft

# Multiple company comparison
> Compare AAPL MSFT GOOGL
```

#### Follow-up Questions
```bash
# Initial analysis
> Analyze AAPL

# Follow-up (maintains context)
> What about its revenue?
> Show me the balance sheet
> How does it compare to Microsoft?
```

## 🎯 Input Formats and Examples

### Supported Input Patterns

#### 1. Direct Ticker Symbols (Recommended)
```bash
> AAPL                    # Basic analysis
> AAPL profile           # Company profile
> AAPL metrics           # Financial metrics
> AAPL income statement  # Income statement analysis
> Compare AAPL MSFT      # Comparison
```

#### 2. Company Names
```bash
> Analyze Apple
> Tell me about Microsoft
> Google financial metrics
> Tesla vs Ford comparison
```

#### 3. Natural Language
```bash
> What can you tell me about Apple?
> I want to analyze Tesla's financials
> Show me a comparison between Apple and Microsoft
> How is Google performing financially?
```

### Analysis Type Keywords

| Analysis Type | Keywords | Example Input |
|---------------|----------|---------------|
| **Company Profile** | profile, company, info, about, overview | "AAPL profile", "Tell me about Apple" |
| **Financial Metrics** | metrics, ratios, financial, performance, valuation | "AAPL metrics", "Tesla financial ratios" |
| **Income Statement** | income, revenue, earnings, profit | "AAPL income statement", "Google earnings" |
| **Balance Sheet** | balance, assets, liabilities, equity | "MSFT balance sheet", "Apple assets" |
| **Cash Flow** | cash, flow, cashflow | "AAPL cash flow", "Tesla cash analysis" |
| **Comparison** | compare, comparison, vs, versus, against | "Compare AAPL MSFT", "Tesla vs Ford" |

## 🔄 Orchestrator Workflow

### Understanding the Analysis Process

The bot follows a structured workflow for each request:

```
User Input → Interpreter → Orchestrator → Tools → Response
```

#### 1. Request Interpretation
```bash
> "Analyze Apple's financial metrics"

Interpreter extracts:
- Companies: ["AAPL"] (mapped from "Apple")
- Analysis Type: "metrics"
- Confidence: 0.8
```

#### 2. Orchestrator Planning
```bash
Orchestrator determines:
- Required tools: [validate_ticker, get_company_data, analyze_financial_metrics]
- Data requirements: [company_info, financial_statements]
- Response format: structured_metrics
```

#### 3. Tool Execution
```bash
Step 1: validate_ticker("AAPL") → ✅ Valid
Step 2: get_company_data("AAPL") → ✅ Data retrieved
Step 3: analyze_financial_metrics("AAPL", data) → ✅ Analysis complete
```

#### 4. Response Generation
```bash
Response Generator creates:
- Formatted analysis results
- User-friendly explanations
- Actionable insights
```

### Workflow States

The orchestrator maintains conversation state:

```python
{
    "user_input": "Analyze AAPL",
    "companies": ["AAPL"],
    "analysis_type": "profile",
    "financial_data": {...},
    "analysis_results": {...},
    "agent_response": "Here's the analysis...",
    "conversation_context": {...}
}
```

## 📊 Understanding Analysis Results

### Company Profile Analysis
```bash
> Analyze AAPL

Response includes:
• Company Overview (name, sector, industry)
• Business Summary
• Market Information (market cap, shares outstanding)
• Key Metrics (P/E ratio, revenue, profit margins)
• Recent Performance
```

### Financial Metrics Analysis
```bash
> AAPL metrics

Response includes:
• Valuation Ratios (P/E, P/B, EV/EBITDA)
• Profitability Metrics (ROE, ROA, profit margins)
• Liquidity Ratios (current ratio, quick ratio)
• Efficiency Metrics (asset turnover, inventory turnover)
• Growth Rates (revenue, earnings growth)
```

### Company Comparison
```bash
> Compare AAPL MSFT

Response includes:
• Side-by-side key metrics
• Relative performance analysis
• Strengths and weaknesses
• Investment considerations
• Peer ranking
```

## 🎨 Customizing Your Experience

### Conversation Context

The bot remembers context within a session:

```bash
> Analyze AAPL
# Bot provides Apple analysis

> What about its competitors?
# Bot understands "its" refers to Apple

> Compare it with Microsoft
# Bot compares Apple (from context) with Microsoft
```

### Clearing Context
```bash
> clear
# Conversation history cleared
# Next query starts fresh context
```

### Getting Help
```bash
> help

Available Analysis Types:
• Company Profile: Basic company information and overview
• Financial Metrics: Key ratios and performance indicators  
• Financial Statements: Income, balance sheet, cash flow analysis
• Company Comparison: Side-by-side analysis of multiple companies

Example Queries:
• "Analyze AAPL" - Get Apple's company profile
• "MSFT metrics" - Microsoft's financial ratios
• "Compare AAPL MSFT" - Compare Apple and Microsoft
• "TSLA income statement" - Tesla's earnings analysis

Tips:
• Use ticker symbols (AAPL, MSFT) for best results
• Ask follow-up questions to dive deeper
• Type 'clear' to reset conversation context
```

## 🔍 Advanced Usage Patterns

### Multi-Step Analysis
```bash
# Step 1: Get overview
> Analyze AAPL

# Step 2: Dive into specifics  
> Show me the income statement

# Step 3: Compare with peers
> How does this compare to Microsoft?

# Step 4: Focus on specific metrics
> What about the debt levels?
```

### Batch Analysis
```bash
# Analyze multiple companies
> Compare AAPL MSFT GOOGL AMZN

# Sequential analysis
> Analyze AAPL
> Now analyze MSFT  
> Now analyze GOOGL
```

### Contextual Queries
```bash
# Initial context
> Analyze Tesla

# Contextual follow-ups
> What's the revenue trend?
> How's the cash flow?
> Compare with Ford
> What about the stock price?
```

## ⚠️ Common Usage Issues

### Input Recognition Problems

#### Issue: Company not recognized
```bash
> Analyze XYZ Corp
❌ "I couldn't identify any companies in your request."
```
**Solution**: Use ticker symbol instead
```bash
> Analyze XYZ
✅ Analysis proceeds if XYZ is valid ticker
```

#### Issue: Ambiguous requests
```bash
> Tell me about stocks
❌ "Could you please specify which company?"
```
**Solution**: Be specific
```bash
> Tell me about AAPL stock
✅ Analysis proceeds
```

### Analysis Limitations

#### Issue: Data not available
```bash
> PRIVATE income statement
❌ "No income data available for PRIVATE"
```
**Reason**: Private companies or delisted stocks may lack data

#### Issue: Invalid ticker
```bash
> Analyze INVALID
❌ "Ticker 'INVALID' not found"
```
**Solution**: Verify ticker symbol on financial websites

### Performance Considerations

#### Slow responses
- **Cause**: Network latency, API rate limits
- **Solution**: Wait for response, avoid rapid successive queries

#### Memory usage
- **Cause**: Large datasets, extended sessions
- **Solution**: Use `clear` command periodically

## 🚀 Best Practices

### Effective Query Patterns

1. **Start with ticker symbols**
   ```bash
   ✅ "AAPL profile"
   ❌ "Apple Computer Inc profile"
   ```

2. **Use specific analysis types**
   ```bash
   ✅ "AAPL income statement"
   ❌ "AAPL financials" (too vague)
   ```

3. **Build on context**
   ```bash
   > Analyze AAPL
   > What about the debt ratios?  # Uses AAPL context
   ```

4. **Compare systematically**
   ```bash
   ✅ "Compare AAPL MSFT"
   ❌ "Compare Apple with that other tech company"
   ```

### Session Management

1. **Clear context when switching focus**
   ```bash
   > Analyze AAPL
   > clear  # Clear before analyzing different sector
   > Analyze JPM
   ```

2. **Use help when stuck**
   ```bash
   > help
   # Review examples and try again
   ```

3. **Exit gracefully**
   ```bash
   > exit
   # Proper cleanup and session termination
   ```

## 📈 Sample Analysis Session

Here's a complete analysis session example:

```bash
$ python3 chat_interface.py

🤖 Financial Analysis Assistant
==============================

> Analyze AAPL

📊 Apple Inc. (AAPL) - Company Analysis
=====================================

Company Overview:
• Name: Apple Inc.
• Sector: Technology  
• Industry: Consumer Electronics
• Market Cap: $3.39T
• Employees: 164,000

Key Metrics:
• Current Price: $189.84
• P/E Ratio: 29.12
• Revenue (TTM): $394.33B
• Net Income: $99.80B
• Profit Margin: 25.31%

Business Summary:
Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets...

> What about the cash flow?

💰 Apple Inc. (AAPL) - Cash Flow Analysis
========================================

Operating Cash Flow: $104.04B
• Strong operational cash generation
• Consistent positive cash flow trends

Free Cash Flow: $84.73B
• Excellent free cash flow margin
• Supports dividend and buyback programs

Cash Position: $162.11B
• Strong balance sheet liquidity
• Low debt-to-equity ratio

> Compare with Microsoft

⚖️ Company Comparison: AAPL vs MSFT
==================================

Market Metrics:
• AAPL Market Cap: $3.39T | MSFT Market Cap: $2.89T
• AAPL P/E: 29.12 | MSFT P/E: 32.45
• AAPL Revenue: $394.33B | MSFT Revenue: $211.92B

Profitability:
• AAPL Profit Margin: 25.31% | MSFT Profit Margin: 36.69%
• AAPL ROE: 160.58% | MSFT ROE: 38.52%

Investment Considerations:
• Apple: Higher revenue, strong consumer brand
• Microsoft: Higher profit margins, cloud growth

> exit

Thank you for using Financial Analysis Assistant! 
Session ended.
```

## 🔧 Troubleshooting Usage Issues

### Common Problems and Solutions

1. **Bot doesn't respond**
   - Check internet connection
   - Verify dependencies installed
   - Restart chat interface

2. **Incorrect analysis results**
   - Verify ticker symbol is correct
   - Check if company is publicly traded
   - Try alternative company name

3. **Performance issues**
   - Use `clear` to reset session
   - Avoid very long queries
   - Wait for current analysis to complete

4. **Context confusion**
   - Use `clear` to reset context
   - Be explicit in follow-up queries
   - Restart session if needed

For detailed troubleshooting, see `TROUBLESHOOTING.md`.

---

**Happy Analyzing!** 📈

The Financial Analysis Bot is designed to make financial analysis accessible and conversational. Experiment with different query patterns to find what works best for your analysis needs.