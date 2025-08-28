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
