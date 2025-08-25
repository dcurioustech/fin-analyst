# Design Document

## Overview

This design implements basic LangGraph integration to provide conversational AI capabilities for the financial analysis system. The design leverages the existing modular architecture and wraps current analysis functions as LangGraph tools, enabling natural language interactions while maintaining all existing functionality.

## Architecture

### High-Level Architecture

```
Chat Interface
      ↓
LangGraph Workflow
      ↓
┌─────────────────────────────────────────────────────────┐
│                 LangGraph Nodes                         │
├─────────────────────────────────────────────────────────┤
│ Parse Input → Route Analysis → Execute Analysis         │
│                    ↓                    ↓               │
│            Single Company        Comparison             │
│            Analysis Node         Analysis Node          │
│                    ↓                    ↓               │
│            Generate Response ← ← ← ← ← ←                │
└─────────────────────────────────────────────────────────┘
      ↓
LangGraph Tools (Wrappers)
      ↓
┌─────────────────────────────────────────────────────────┐
│              Existing Analysis Layer                    │
├─────────────────────────────────────────────────────────┤
│ CompanyAnalyzer │ MetricsAnalyzer │ ComparisonAnalyzer  │
│ StatementAnalyzer │ FinancialDataService               │
└─────────────────────────────────────────────────────────┘
```

### Component Structure

```
agents/
├── __init__.py
├── state.py              # Conversation state management
├── tools.py              # LangGraph tools wrapping existing functions
├── nodes.py              # Workflow nodes for different analysis types
└── graph.py              # Main LangGraph workflow definition

chat_interface.py         # Simple chat interface for testing
.env.example             # Environment configuration template
```

## Components and Interfaces

### 1. Conversation State (`agents/state.py`)

**Purpose**: Manages conversation state across multiple turns, tracking companies, analysis types, and results.

**Key Components**:
```python
class FinancialAgentState(TypedDict):
    # Conversation management
    messages: List[Dict[str, Any]]
    user_input: str
    agent_response: str
    
    # Financial context
    companies: List[str]  # Ticker symbols
    analysis_type: Optional[str]
    time_period: Optional[str]
    
    # Data and results
    financial_data: Dict[str, Any]
    analysis_results: Dict[str, Any]
    
    # User preferences and metadata
    user_preferences: Dict[str, Any]
    conversation_context: Dict[str, Any]
    session_id: Optional[str]
    timestamp: Optional[str]
    error_message: Optional[str]
```

**State Management Functions**:
- `create_initial_state()`: Initialize new conversation
- `update_state_with_user_input()`: Add user message to state
- `update_state_with_agent_response()`: Add agent response to state
- `add_company_to_context()`: Track companies in conversation
- `store_financial_data()`: Cache financial data
- `store_analysis_results()`: Store analysis results

### 2. LangGraph Tools (`agents/tools.py`)

**Purpose**: Wraps existing analysis functions as LangGraph tools for agent use.

**Key Tools**:
```python
@tool
def get_company_info(ticker: str) -> Dict[str, Any]

@tool
def analyze_company_profile(ticker: str) -> Dict[str, Any]

@tool
def analyze_financial_metrics(ticker: str) -> Dict[str, Any]

@tool
def analyze_financial_statement(ticker: str, statement_type: str) -> Dict[str, Any]

@tool
def compare_companies(main_ticker: str, peer_tickers: List[str]) -> Dict[str, Any]

@tool
def get_analyst_recommendations(ticker: str) -> Dict[str, Any]

@tool
def validate_ticker_symbol(ticker: str) -> Dict[str, Any]

@tool
def suggest_peer_companies(ticker: str) -> Dict[str, Any]
```

**Tool Design Principles**:
- Each tool wraps one or more existing analysis functions
- Tools return structured data compatible with both LangGraph and existing formatters
- Error handling is consistent across all tools
- Tools are stateless and rely on the existing service layer

### 3. Workflow Nodes (`agents/nodes.py`)

**Purpose**: Implements the conversation workflow logic as LangGraph nodes.

**Key Nodes**:

#### Input Processing Node
```python
def parse_user_input_node(state: FinancialAgentState) -> FinancialAgentState
```
- Extracts ticker symbols using regex patterns
- Maps company names to ticker symbols
- Determines analysis type from keywords
- Updates conversation state with parsed information

#### Routing Node
```python
def route_analysis_node(state: FinancialAgentState) -> str
```
- Routes to appropriate analysis based on parsed input
- Handles single company vs. comparison scenarios
- Returns next node name for conditional routing

#### Analysis Nodes
```python
def single_company_analysis_node(state: FinancialAgentState) -> FinancialAgentState
def comparison_analysis_node(state: FinancialAgentState) -> FinancialAgentState
def general_analysis_node(state: FinancialAgentState) -> FinancialAgentState
```
- Execute appropriate tools based on analysis type
- Store results in conversation state
- Handle errors gracefully

#### Response Generation Node
```python
def response_generation_node(state: FinancialAgentState) -> FinancialAgentState
```
- Formats analysis results using existing display formatters
- Generates contextual responses
- Handles error cases with user-friendly messages

#### Clarification Node
```python
def clarification_node(state: FinancialAgentState) -> FinancialAgentState
```
- Handles ambiguous or unclear user input
- Requests specific information from users
- Provides examples and guidance

### 4. Main Workflow (`agents/graph.py`)

**Purpose**: Orchestrates the conversation workflow using LangGraph.

**Workflow Structure**:
```python
class FinancialAnalysisGraph:
    def __init__(self):
        self.graph = self._build_graph()
        self.app = self.graph.compile()
    
    def _build_graph(self) -> StateGraph:
        # Create workflow with nodes and edges
        # Set up conditional routing
        # Define entry and exit points
    
    def process_message(self, user_input: str, state: FinancialAgentState = None) -> FinancialAgentState:
        # Process user message through workflow
        # Return updated state with response
    
    def start_conversation(self) -> FinancialAgentState:
        # Initialize new conversation with welcome message
```

**Graph Flow**:
1. **Entry Point**: `parse_input`
2. **Conditional Routing**: Based on parsed input
   - Single company analysis
   - Comparison analysis
   - General analysis
   - Clarification request
3. **Response Generation**: Format and return response
4. **Exit Point**: End conversation turn

### 5. Chat Interface (`chat_interface.py`)

**Purpose**: Provides a simple command-line interface for testing the LangGraph integration.

**Key Features**:
```python
class FinancialChatInterface:
    def start_chat(self) -> None:
        # Initialize chat session
        # Display welcome message
        # Enter main chat loop
    
    def _chat_loop(self) -> None:
        # Handle user input
        # Process through LangGraph
        # Display responses
        # Handle special commands (help, exit, clear)
```

**Special Commands**:
- `help` or `?`: Display usage instructions
- `clear` or `reset`: Reset conversation context
- `exit`, `quit`, `bye`: Exit chat session

## Data Models

### Input Processing

**Company Recognition**:
- Regex pattern for ticker symbols: `\b[A-Z]{1,5}\b`
- Company name mapping dictionary for common companies
- Case-insensitive matching for company names

**Analysis Type Detection**:
```python
analysis_keywords = {
    'profile': ['profile', 'company', 'info', 'information', 'about'],
    'metrics': ['metrics', 'ratios', 'financial', 'performance', 'valuation'],
    'comparison': ['compare', 'comparison', 'vs', 'versus', 'against', 'peer'],
    'income_statement': ['income', 'revenue', 'earnings', 'profit'],
    'balance_sheet': ['balance', 'assets', 'liabilities', 'equity'],
    'cash_flow': ['cash', 'flow', 'cashflow'],
    'recommendations': ['recommendations', 'analyst', 'rating', 'target']
}
```

### Response Formatting

**Response Structure**:
- Uses existing `DisplayFormatter` for consistent output
- Maintains text-based visualizations
- Provides contextual information about current companies
- Includes error handling and user guidance

## Error Handling

### Error Categories
1. **Input Parsing Errors**: Unrecognized companies or unclear requests
2. **Tool Execution Errors**: API failures, invalid tickers, missing data
3. **Workflow Errors**: Node execution failures, state corruption
4. **System Errors**: Configuration issues, missing dependencies

### Error Handling Strategy
- Each node implements specific error handling
- Tools return structured error responses
- User-friendly error messages in chat interface
- Graceful degradation when possible
- Logging for debugging and monitoring

### Error Response Format
```python
{
    "success": False,
    "error": "User-friendly error message",
    "details": {
        "error_type": "category",
        "technical_details": "...",
        "timestamp": "..."
    }
}
```

## Testing Strategy

### Unit Testing Approach
- Test individual nodes with mock states
- Test tools with mock service responses
- Test state management functions
- Test input parsing logic

### Integration Testing
- Test complete workflow with real data
- Test conversation context maintenance
- Test error propagation through workflow
- Test chat interface interactions

### Test Structure
```
tests/
├── test_agents/
│   ├── test_state.py
│   ├── test_tools.py
│   ├── test_nodes.py
│   └── test_graph.py
└── test_chat_interface.py
```

## Configuration and Environment

### Environment Variables
```bash
# Required for LLM integration (future)
OPENAI_API_KEY=your_api_key_here

# Optional configuration
OPENAI_MODEL=gpt-3.5-turbo
LOG_LEVEL=INFO
```

### Dependencies
```
langgraph>=0.0.40
langchain>=0.1.0
langchain-openai>=0.0.8
openai>=1.0.0
python-dotenv>=1.0.0
```

## Performance Considerations

### Caching Strategy
- Reuse financial data within conversation context
- Cache analysis results for repeated requests
- Leverage existing service layer caching

### Memory Management
- Clean up old conversation states
- Limit message history length
- Efficient state updates

### Scalability
- Stateless tool design for horizontal scaling
- Conversation state can be externalized to database
- Graph compilation is done once at startup

## Future Extensibility

### Adding New Analysis Types
1. Create new tool function in `tools.py`
2. Add keywords to analysis type detection
3. Add routing logic in `route_analysis_node`
4. Add handling in appropriate analysis node

### Adding New Conversation Flows
1. Create new node function in `nodes.py`
2. Add node to graph in `_build_graph`
3. Add routing logic and edges
4. Update state schema if needed

### LLM Integration (Future)
- Current design is LLM-ready but doesn't require it
- Can add LLM-powered intent parsing
- Can enhance response generation with LLM
- Can add conversational memory and personalization

## Benefits

### User Experience
- Natural language interaction instead of menu navigation
- Contextual conversations with follow-up questions
- Intelligent routing to appropriate analysis
- Helpful error messages and guidance

### Developer Experience
- Modular design with clear separation of concerns
- Reuses existing analysis infrastructure
- Easy to test and extend
- Clear workflow visualization with LangGraph

### Maintainability
- Wraps existing functions without modification
- Consistent error handling patterns
- Comprehensive logging and monitoring
- Clear state management