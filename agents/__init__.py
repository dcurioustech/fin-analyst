"""
LangGraph Orchestrator System for Financial Analysis.

This module provides an orchestrator-driven architecture using LangGraph
for multi-turn financial analysis conversations with clear layer separation:

- Orchestrator: LangGraph workflow managing the entire process
- Interpreter: Understanding user requests (rule-based + future LLM)
- Analysis/Tools: Processing requests using existing analysis functions
- Data Service: Fetching external financial data
- Response Generation: Formatting responses (rule-based + future LLM)
"""

# Import main components for easier access
from .graph import financial_orchestrator
from .state import FinancialOrchestratorState, create_initial_state

__all__ = [
    "financial_orchestrator",
    "FinancialOrchestratorState",
    "create_initial_state",
]
