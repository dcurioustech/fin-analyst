# Design Document

## Overview

This design transforms the monolithic `analysis_bot.py` into a modular, maintainable architecture that separates concerns and provides a foundation for future enhancements. The design follows the single responsibility principle and creates clear boundaries between different functional areas.

## Architecture

### High-Level Architecture

```
fin_analyst/
├── main.py                 # Application entry point
├── services/
│   ├── __init__.py
│   └── financial_data_service.py    # Data access layer
├── analysis/
│   ├── __init__.py
│   ├── company_analyzer.py          # Company profile analysis
│   ├── metrics_analyzer.py          # Financial metrics analysis
│   ├── statement_analyzer.py        # Financial statements analysis
│   └── comparison_analyzer.py       # Peer comparison analysis
├── ui/
│   ├── __init__.py
│   ├── menu_handler.py             # Menu and user interaction
│   └── display_formatter.py        # Output formatting
├── utils/
│   ├── __init__.py
│   ├── formatters.py               # Number and text formatting
│   └── visualizations.py           # Text-based charts
└── config/
    ├── __init__.py
    └── settings.py                 # Configuration and constants
```

### Layer Responsibilities

1. **Services Layer**: Handles external data access and API interactions
2. **Analysis Layer**: Contains business logic for different types of financial analysis
3. **UI Layer**: Manages user interaction and output formatting
4. **Utils Layer**: Provides reusable utility functions
5. **Config Layer**: Manages application configuration and settings

## Components and Interfaces

### 1. Financial Data Service (`services/financial_data_service.py`)

**Purpose**: Abstracts yfinance interactions and provides a clean interface for financial data access.

**Key Methods**:
```python
class FinancialDataService:
    def get_company_info(self, ticker: str) -> dict
    def get_financial_statements(self, ticker: str) -> dict
    def get_recommendations(self, ticker: str) -> pd.DataFrame
    def validate_ticker(self, ticker: str) -> bool
    def get_multiple_company_info(self, tickers: list) -> dict
```

**Error Handling**: Returns structured error responses for invalid tickers, network issues, and API failures.

### 2. Company Analyzer (`analysis/company_analyzer.py`)

**Purpose**: Handles company profile and basic information analysis.

**Key Methods**:
```python
class CompanyAnalyzer:
    def analyze_company_profile(self, company_info: dict) -> dict
    def format_company_summary(self, company_info: dict) -> str
    def extract_key_company_details(self, company_info: dict) -> dict
```

### 3. Metrics Analyzer (`analysis/metrics_analyzer.py`)

**Purpose**: Processes and analyzes financial metrics and ratios.

**Key Methods**:
```python
class MetricsAnalyzer:
    def analyze_valuation_metrics(self, company_info: dict) -> dict
    def analyze_profitability_metrics(self, company_info: dict) -> dict
    def analyze_stock_price_metrics(self, company_info: dict) -> dict
    def analyze_dividend_metrics(self, company_info: dict) -> dict
    def get_comprehensive_metrics(self, company_info: dict) -> dict
```

### 4. Statement Analyzer (`analysis/statement_analyzer.py`)

**Purpose**: Handles financial statement processing and formatting.

**Key Methods**:
```python
class StatementAnalyzer:
    def process_income_statement(self, statement_data: pd.DataFrame) -> dict
    def process_balance_sheet(self, statement_data: pd.DataFrame) -> dict
    def process_cash_flow(self, statement_data: pd.DataFrame) -> dict
    def format_statement_for_display(self, statement: pd.DataFrame) -> str
```

### 5. Comparison Analyzer (`analysis/comparison_analyzer.py`)

**Purpose**: Handles peer comparison and competitive analysis.

**Key Methods**:
```python
class ComparisonAnalyzer:
    def perform_peer_comparison(self, main_ticker: str, peer_tickers: list) -> dict
    def suggest_peers(self, company_info: dict) -> list
    def calculate_comparison_metrics(self, companies_data: dict) -> pd.DataFrame
    def generate_comparison_visuals(self, comparison_data: pd.DataFrame) -> str
```

### 6. Menu Handler (`ui/menu_handler.py`)

**Purpose**: Manages user interaction, menu display, and input processing.

**Key Methods**:
```python
class MenuHandler:
    def display_main_menu(self) -> None
    def display_analysis_menu(self) -> None
    def get_user_choice(self, options: list) -> str
    def get_ticker_input(self) -> str
    def get_peer_tickers_input(self, suggested_peers: list) -> list
    def handle_menu_navigation(self) -> str
```

### 7. Display Formatter (`ui/display_formatter.py`)

**Purpose**: Handles output formatting and display logic.

**Key Methods**:
```python
class DisplayFormatter:
    def format_company_profile(self, profile_data: dict) -> str
    def format_metrics_display(self, metrics_data: dict) -> str
    def format_statement_display(self, statement_data: dict) -> str
    def format_comparison_display(self, comparison_data: dict) -> str
    def format_error_message(self, error: Exception) -> str
```

### 8. Formatters (`utils/formatters.py`)

**Purpose**: Provides utility functions for number and text formatting.

**Key Functions**:
```python
def format_large_number(num: float) -> str
def format_percentage(num: float) -> str
def format_currency(num: float) -> str
def safe_format_number(num: any) -> str
```

### 9. Visualizations (`utils/visualizations.py`)

**Purpose**: Provides text-based visualization utilities.

**Key Functions**:
```python
def plot_text_bar(label: str, value: float, max_value: float) -> str
def create_comparison_chart(data: dict) -> str
def create_metrics_visualization(metrics: dict) -> str
```

### 10. Settings (`config/settings.py`)

**Purpose**: Manages application configuration and constants.

**Contents**:
```python
# Pandas display options
PANDAS_DISPLAY_OPTIONS = {
    'display.max_rows': 500,
    'display.max_columns': 500,
    'display.width': 1000
}

# Analysis configuration
COMPARISON_METRICS = {
    'marketCap': 'Market Cap',
    'trailingPE': 'P/E Ratio',
    # ... other metrics
}

# UI configuration
MENU_OPTIONS = {
    'main_menu': [...],
    'analysis_menu': [...]
}
```

## Data Models

### Company Data Model
```python
@dataclass
class CompanyData:
    ticker: str
    name: str
    sector: str
    industry: str
    market_cap: float
    current_price: float
    # ... other fields
```

### Analysis Result Model
```python
@dataclass
class AnalysisResult:
    success: bool
    data: dict
    error_message: str = None
    timestamp: datetime = field(default_factory=datetime.now)
```

### Comparison Data Model
```python
@dataclass
class ComparisonData:
    main_ticker: str
    peer_tickers: list
    metrics: pd.DataFrame
    visual_data: dict
```

## Error Handling

### Error Categories
1. **Data Access Errors**: Invalid tickers, network failures, API limits
2. **Analysis Errors**: Missing data, calculation failures
3. **User Input Errors**: Invalid menu choices, malformed ticker symbols
4. **System Errors**: Configuration issues, module import failures

### Error Handling Strategy
- Each module implements specific error handling for its domain
- Errors are logged with appropriate severity levels
- User-friendly error messages are displayed through the UI layer
- System continues operation when possible, gracefully degrading functionality

### Error Response Format
```python
class ErrorResponse:
    def __init__(self, error_type: str, message: str, details: dict = None):
        self.error_type = error_type
        self.message = message
        self.details = details or {}
        self.timestamp = datetime.now()
```

## Testing Strategy

### Unit Testing Approach
- Each module will have corresponding test files
- Mock external dependencies (yfinance API calls)
- Test both success and failure scenarios
- Focus on business logic validation

### Test Structure
```
tests/
├── test_services/
│   └── test_financial_data_service.py
├── test_analysis/
│   ├── test_company_analyzer.py
│   ├── test_metrics_analyzer.py
│   ├── test_statement_analyzer.py
│   └── test_comparison_analyzer.py
├── test_ui/
│   ├── test_menu_handler.py
│   └── test_display_formatter.py
└── test_utils/
    ├── test_formatters.py
    └── test_visualizations.py
```

### Integration Testing
- Test complete user workflows
- Verify module interactions
- Test error propagation between layers

## Migration Strategy

### Phase 1: Extract Utilities
- Move formatting and visualization functions to utils modules
- Update imports in main file
- Verify functionality remains intact

### Phase 2: Extract Data Service
- Create FinancialDataService class
- Move all yfinance interactions to service layer
- Update main file to use service

### Phase 3: Extract Analysis Modules
- Create analyzer classes for different analysis types
- Move business logic from main file to analyzers
- Update main file to use analyzers

### Phase 4: Extract UI Layer
- Create menu handler and display formatter
- Move UI logic from main file
- Create new main.py as orchestrator

### Phase 5: Configuration and Cleanup
- Move configuration to settings module
- Clean up imports and dependencies
- Add proper error handling and logging

## Dependencies

### External Dependencies
- `yfinance`: Financial data access (existing)
- `pandas`: Data manipulation (existing)
- `sys`: System operations (existing)

### Internal Dependencies
- Clear dependency flow: UI → Analysis → Services → Utils
- No circular dependencies
- Minimal coupling between modules

## Performance Considerations

### Caching Strategy
- Service layer prepared for future caching implementation
- Data fetching abstracted to support caching layers
- Comparison data can be cached to avoid repeated API calls

### Memory Management
- Large DataFrames handled efficiently
- Proper cleanup of resources
- Lazy loading where appropriate

### API Rate Limiting
- Service layer designed to handle rate limiting
- Batch requests where possible
- Graceful degradation when limits reached