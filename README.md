# Financial Analysis Bot

![Test Suite](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Test%20Suite/badge.svg)
![CI/CD Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI%2FCD%20Pipeline/badge.svg)
[![Coverage](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO)

An intelligent financial analysis assistant that provides comprehensive company analysis, financial metrics, and market insights through natural language conversations.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start the chat interface
python3 chat_interface.py

# Begin analyzing
> Analyze AAPL
> Compare Apple and Microsoft
> Show me Tesla's financial metrics
```

## ✨ Features

- **Conversational Interface**: Natural language queries with context awareness
- **Company Analysis**: Profiles, financial metrics, and statement analysis
- **Smart Comparisons**: Side-by-side company and peer analysis
- **Real-time Data**: Live financial data from Yahoo Finance API
- **Multiple Interfaces**: CLI chat, web interface, and programmatic API
- **Production Ready**: GCP deployment with auto-scaling and monitoring

## 🏗️ Architecture

```
User Input → LangGraph Orchestrator → Analysis Tools → Financial Data
     ↓              ↓                      ↓              ↓
Chat Interface → Workflow Engine → Company Analyzer → Yahoo Finance API
```

The system uses LangGraph to orchestrate intelligent workflows across specialized analysis layers, providing reliable financial insights with conversational ease.

## 📚 Documentation

- **[User Guide](USER_GUIDE.md)** - Complete guide to using the application
- **[Developer Guide](DEVELOPER_GUIDE.md)** - Technical details and contributing
- **[Quick Reference](QUICK_REFERENCE.md)** - Commands, examples, and troubleshooting
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment on GCP

## 🛠️ Installation

### Local Development
```bash
git clone <repository-url>
cd financial-analysis-bot
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
```

### Usage Options
```bash
# Interactive chat (recommended)
python3 chat_interface.py

# Web interface
python3 web_app.py

# Original menu interface
python3 main.py
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=term-missing

# Run specific tests
python3 test_orchestrator_comprehensive.py
```

See [Developer Guide](DEVELOPER_GUIDE.md) for comprehensive testing information.

## 🤝 Contributing

We welcome contributions! See the [Developer Guide](DEVELOPER_GUIDE.md) for setup instructions, architecture details, and contribution guidelines.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Note**: This application is for educational and research purposes. Always consult with financial professionals before making investment decisions.