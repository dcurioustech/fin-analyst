"""
LangGraph State Management for Financial Analysis Orchestrator.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, TypedDict


class FinancialOrchestratorState(TypedDict):
    """State schema for the financial analysis orchestrator."""

    # User interaction
    user_input: str
    agent_response: str
    messages: List[Dict[str, Any]]

    # Interpretation layer results
    interpretation: Dict[str, Any]  # Parsed user request
    needs_clarification: bool
    clarification_message: Optional[str]

    # Analysis planning
    analysis_plan: Dict[str, Any]  # What analysis to perform
    required_tools: List[str]  # Tools needed for analysis
    data_requirements: List[str]  # Data needed from services

    # Financial context
    companies: List[str]  # List of ticker symbols being discussed
    analysis_type: Optional[str]  # Type of analysis requested
    time_period: Optional[str]  # Time period for analysis

    # Data and results
    financial_data: Dict[str, Any]  # Cached financial data from services
    analysis_results: Dict[str, Any]  # Results from analysis tools

    # Response generation
    response_context: Dict[str, Any]  # Context for response generation
    response_method: str  # 'rule_based' or 'llm'

    # Conversation management
    conversation_context: Dict[str, Any]  # Conversation history and context
    user_preferences: Dict[str, Any]  # User preferences

    # Orchestrator metadata
    workflow_step: str  # Current step in orchestrator workflow
    session_id: Optional[str]
    timestamp: Optional[str]
    error_message: Optional[str]


def create_initial_state() -> FinancialOrchestratorState:
    """Create an initial state for a new conversation."""
    return FinancialOrchestratorState(
        # User interaction
        user_input="",
        agent_response="",
        messages=[],
        # Interpretation layer
        interpretation={},
        needs_clarification=False,
        clarification_message=None,
        # Analysis planning
        analysis_plan={},
        required_tools=[],
        data_requirements=[],
        # Financial context
        companies=[],
        analysis_type=None,
        time_period=None,
        # Data and results
        financial_data={},
        analysis_results={},
        # Response generation
        response_context={},
        response_method="rule_based",
        # Conversation management
        conversation_context={},
        user_preferences={},
        # Orchestrator metadata
        workflow_step="entry",
        session_id=None,
        timestamp=datetime.now().isoformat(),
        error_message=None,
    )


def update_state_with_user_input(
    state: FinancialOrchestratorState, user_input: str
) -> FinancialOrchestratorState:
    """Update state with new user input."""
    state["user_input"] = user_input
    state["messages"].append(
        {"role": "user", "content": user_input, "timestamp": datetime.now().isoformat()}
    )
    state["timestamp"] = datetime.now().isoformat()
    state["workflow_step"] = "interpretation"
    return state


def update_state_with_agent_response(
    state: FinancialOrchestratorState, response: str
) -> FinancialOrchestratorState:
    """Update state with agent response."""
    state["agent_response"] = response
    state["messages"].append(
        {
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat(),
        }
    )
    state["timestamp"] = datetime.now().isoformat()
    state["workflow_step"] = "complete"
    return state


def update_interpretation(
    state: FinancialOrchestratorState, interpretation: Dict[str, Any]
) -> FinancialOrchestratorState:
    """Update state with interpretation results."""
    state["interpretation"] = interpretation
    state["companies"] = interpretation.get("companies", [])
    state["analysis_type"] = interpretation.get("analysis_type")
    state["needs_clarification"] = interpretation.get("needs_clarification", False)
    state["clarification_message"] = interpretation.get("clarification_message")
    state["workflow_step"] = "planning"
    return state


def update_analysis_plan(
    state: FinancialOrchestratorState, plan: Dict[str, Any]
) -> FinancialOrchestratorState:
    """Update state with analysis plan."""
    state["analysis_plan"] = plan
    state["required_tools"] = plan.get("tools", [])
    state["data_requirements"] = plan.get("data_requirements", [])
    state["workflow_step"] = "data_collection"
    return state


def store_financial_data(
    state: FinancialOrchestratorState, ticker: str, data: Dict[str, Any]
) -> FinancialOrchestratorState:
    """Store financial data in the state."""
    state["financial_data"][ticker] = data
    return state


def store_analysis_results(
    state: FinancialOrchestratorState, results: Dict[str, Any]
) -> FinancialOrchestratorState:
    """Store analysis results in the state."""
    state["analysis_results"].update(results)
    state["workflow_step"] = "response_generation"
    return state


def update_response_context(
    state: FinancialOrchestratorState, context: Dict[str, Any]
) -> FinancialOrchestratorState:
    """Update state with response generation context."""
    state["response_context"] = context
    return state


def add_company_to_context(
    state: FinancialOrchestratorState, ticker: str
) -> FinancialOrchestratorState:
    """Add a company ticker to the conversation context."""
    if ticker.upper() not in [t.upper() for t in state["companies"]]:
        state["companies"].append(ticker.upper())
    return state


def set_workflow_step(
    state: FinancialOrchestratorState, step: str
) -> FinancialOrchestratorState:
    """Set the current workflow step."""
    state["workflow_step"] = step
    return state


def set_error(
    state: FinancialOrchestratorState, error_message: str
) -> FinancialOrchestratorState:
    """Set error message in state."""
    state["error_message"] = error_message
    state["workflow_step"] = "error"
    return state
