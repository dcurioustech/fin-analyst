"""
LangGraph Orchestrator Nodes for Financial Analysis Workflow.

This module contains the orchestrator nodes that manage the financial analysis
workflow with clear separation between interpretation, planning, execution,
and response generation.
"""

import logging
from typing import Any, Dict, List

from .interpreter import default_interpreter
from .response_generator import ResponseContext, default_response_generator
from .state import FinancialOrchestratorState
from .tools import TOOL_MAP

logger = logging.getLogger(__name__)


# =============================================================================
# ORCHESTRATOR ENTRY AND ROUTING NODES
# =============================================================================


def orchestrator_entry_node(
    state: FinancialOrchestratorState,
) -> FinancialOrchestratorState:
    """
    Entry point for the orchestrator workflow.

    Args:
        state: Current orchestrator state

    Returns:
        Updated state ready for interpretation
    """
    logger.info(
        f"Orchestrator entry - processing user input: {state['user_input'][:100]}..."
    )

    # Set workflow step
    state["workflow_step"] = "interpretation"

    # Clear any previous error messages
    state["error_message"] = None

    return state


def interpreter_routing_node(
    state: FinancialOrchestratorState,
) -> FinancialOrchestratorState:
    """
    Route user input through the interpreter layer.

    Args:
        state: Current orchestrator state

    Returns:
        Updated state with interpretation results
    """
    try:
        logger.info("Routing to interpreter layer")

        # Get conversation context for interpreter
        context = {
            "companies": state.get("companies", []),
            "conversation_context": state.get("conversation_context", {}),
            "messages": state.get("messages", []),
        }

        # Interpret the user request
        interpretation = default_interpreter.interpret_request(
            state["user_input"], context
        )

        # Update state with interpretation results
        from .state import update_interpretation

        state = update_interpretation(state, interpretation.to_dict())

        logger.info(
            f"Interpretation complete - Companies: {state['companies']}, "
            f"Analysis: {state['analysis_type']}, "
            f"Needs clarification: {state['needs_clarification']}"
        )

        return state

    except Exception as e:
        logger.error(f"Error in interpreter routing: {e}")
        from .state import set_error

        return set_error(state, f"Error interpreting request: {str(e)}")


def analysis_planning_node(
    state: FinancialOrchestratorState,
) -> FinancialOrchestratorState:
    """
    Plan the analysis workflow based on interpretation results.

    Args:
        state: Current orchestrator state

    Returns:
        Updated state with analysis plan
    """
    try:
        logger.info("Planning analysis workflow")

        # Check if clarification is needed
        if state.get("needs_clarification", False):
            logger.info("Clarification needed - skipping analysis planning")
            state["workflow_step"] = "response_generation"
            return state

        companies = state.get("companies", [])
        analysis_type = state.get("analysis_type")

        # Create analysis plan
        plan = {
            "companies": companies,
            "analysis_type": analysis_type,
            "tools": [],
            "data_requirements": [],
        }

        # Determine required tools and data based on analysis type
        if analysis_type == "comparison" and len(companies) > 1:
            plan["tools"] = ["get_peer_comparison_data", "compare_companies"]
            plan["data_requirements"] = ["comparison_data"]
        elif analysis_type == "profile":
            plan["tools"] = ["get_company_data", "analyze_company_profile"]
            plan["data_requirements"] = ["company_data"]
        elif analysis_type == "metrics":
            plan["tools"] = ["get_company_data", "analyze_financial_metrics"]
            plan["data_requirements"] = ["company_data"]
        elif analysis_type in ["income_statement", "balance_sheet", "cash_flow"]:
            plan["tools"] = [
                "get_financial_statements_data",
                "analyze_financial_statements",
            ]
            plan["data_requirements"] = ["statements_data"]
        elif analysis_type == "recommendations":
            plan["tools"] = ["get_analyst_recommendations"]
            plan["data_requirements"] = []
        else:
            # Default to profile analysis
            plan["tools"] = ["get_company_data", "analyze_company_profile"]
            plan["data_requirements"] = ["company_data"]
            plan["analysis_type"] = "profile"

        # Update state with plan
        from .state import update_analysis_plan

        state = update_analysis_plan(state, plan)

        logger.info(
            f"Analysis plan created - Tools: {plan['tools']}, "
            f"Data requirements: {plan['data_requirements']}"
        )

        return state

    except Exception as e:
        logger.error(f"Error in analysis planning: {e}")
        from .state import set_error

        return set_error(state, f"Error planning analysis: {str(e)}")


# =============================================================================
# ANALYSIS EXECUTION ORCHESTRATION NODES
# =============================================================================


def data_collection_node(
    state: FinancialOrchestratorState,
) -> FinancialOrchestratorState:
    """
    Collect required financial data from external services.

    Args:
        state: Current orchestrator state

    Returns:
        Updated state with collected data
    """
    try:
        logger.info("Collecting financial data")

        companies = state.get("companies", [])
        data_requirements = state.get("data_requirements", [])
        analysis_type = state.get("analysis_type")

        # Collect data based on requirements
        for requirement in data_requirements:
            if requirement == "company_data":
                for ticker in companies:
                    tool = TOOL_MAP["get_company_data"]
                    result = tool.invoke({"ticker": ticker})
                    if result.get("success"):
                        from .state import store_financial_data

                        state = store_financial_data(state, ticker, result["data"])
                    else:
                        logger.warning(
                            f"Failed to get company data for {ticker}: {result.get('error')}"
                        )

            elif requirement == "statements_data":
                for ticker in companies:
                    tool = TOOL_MAP["get_financial_statements_data"]
                    result = tool.invoke({"ticker": ticker})
                    if result.get("success"):
                        state["financial_data"][f"{ticker}_statements"] = result["data"]
                    else:
                        logger.warning(
                            f"Failed to get statements data for {ticker}: {result.get('error')}"
                        )

            elif requirement == "comparison_data" and len(companies) > 1:
                main_ticker = companies[0]
                peer_tickers = companies[1:]
                tool = TOOL_MAP["get_peer_comparison_data"]
                result = tool.invoke(
                    {"main_ticker": main_ticker, "peer_tickers": peer_tickers}
                )
                if result.get("success"):
                    state["financial_data"]["comparison_data"] = result["data"]
                else:
                    logger.warning(
                        f"Failed to get comparison data: {result.get('error')}"
                    )

        state["workflow_step"] = "analysis_execution"
        logger.info("Data collection complete")

        return state

    except Exception as e:
        logger.error(f"Error in data collection: {e}")
        from .state import set_error

        return set_error(state, f"Error collecting data: {str(e)}")


def analysis_execution_node(
    state: FinancialOrchestratorState,
) -> FinancialOrchestratorState:
    """
    Execute analysis tools using collected data.

    Args:
        state: Current orchestrator state

    Returns:
        Updated state with analysis results
    """
    try:
        logger.info("Executing analysis tools")

        companies = state.get("companies", [])
        analysis_type = state.get("analysis_type")
        required_tools = state.get("required_tools", [])
        financial_data = state.get("financial_data", {})

        results = {}

        # Execute tools based on analysis plan
        for tool_name in required_tools:
            if tool_name not in TOOL_MAP:
                logger.warning(f"Tool {tool_name} not found in tool map")
                continue

            tool = TOOL_MAP[tool_name]

            # Execute tool based on type
            if tool_name == "analyze_company_profile":
                for ticker in companies:
                    company_data = financial_data.get(ticker)
                    if company_data:
                        result = tool.invoke(
                            {"ticker": ticker, "company_data": company_data}
                        )
                        results[f"{ticker}_profile"] = result

            elif tool_name == "analyze_financial_metrics":
                for ticker in companies:
                    company_data = financial_data.get(ticker)
                    if company_data:
                        result = tool.invoke(
                            {"ticker": ticker, "company_data": company_data}
                        )
                        results[f"{ticker}_metrics"] = result

            elif tool_name == "analyze_financial_statements":
                for ticker in companies:
                    statements_data = financial_data.get(f"{ticker}_statements")
                    if statements_data:
                        result = tool.invoke(
                            {
                                "ticker": ticker,
                                "statement_type": analysis_type,
                                "statements_data": statements_data,
                            }
                        )
                        results[f"{ticker}_{analysis_type}"] = result

            elif tool_name == "compare_companies" and len(companies) > 1:
                main_ticker = companies[0]
                peer_tickers = companies[1:]
                comparison_data = financial_data.get("comparison_data")
                if comparison_data:
                    result = tool.invoke(
                        {
                            "main_ticker": main_ticker,
                            "peer_tickers": peer_tickers,
                            "comparison_data": comparison_data,
                        }
                    )
                    results["comparison"] = result

            elif tool_name == "get_analyst_recommendations":
                for ticker in companies:
                    result = tool.invoke({"ticker": ticker})
                    results[f"{ticker}_recommendations"] = result

        # Store results in state
        from .state import store_analysis_results

        state = store_analysis_results(state, results)

        logger.info(f"Analysis execution complete - {len(results)} results generated")

        return state

    except Exception as e:
        logger.error(f"Error in analysis execution: {e}")
        from .state import set_error

        return set_error(state, f"Error executing analysis: {str(e)}")


def result_aggregation_node(
    state: FinancialOrchestratorState,
) -> FinancialOrchestratorState:
    """
    Aggregate and prepare analysis results for response generation.

    Args:
        state: Current orchestrator state

    Returns:
        Updated state with aggregated results
    """
    try:
        logger.info("Aggregating analysis results")

        # Results are already stored in state from analysis execution
        # This node can be used for additional processing if needed

        # Prepare response context
        response_context = ResponseContext()
        response_context.analysis_results = state.get("analysis_results", {})
        response_context.companies = state.get("companies", [])
        response_context.analysis_type = state.get("analysis_type")
        response_context.conversation_context = state.get("conversation_context", {})
        response_context.user_input = state.get("user_input", "")
        response_context.error_message = state.get("error_message")

        # Store response context in state
        from .state import update_response_context

        state = update_response_context(state, response_context.to_dict())

        state["workflow_step"] = "response_generation"
        logger.info("Result aggregation complete")

        return state

    except Exception as e:
        logger.error(f"Error in result aggregation: {e}")
        from .state import set_error

        return set_error(state, f"Error aggregating results: {str(e)}")


# =============================================================================
# RESPONSE ORCHESTRATION NODES
# =============================================================================


def response_planning_node(
    state: FinancialOrchestratorState,
) -> FinancialOrchestratorState:
    """
    Plan response generation strategy.

    Args:
        state: Current orchestrator state

    Returns:
        Updated state with response plan
    """
    try:
        logger.info("Planning response generation")

        # Determine response method (rule-based vs LLM)
        # For Phase 1, always use rule-based
        state["response_method"] = "rule_based"

        # Check if we need clarification response
        if state.get("needs_clarification", False):
            state["workflow_step"] = "clarification_response"
        else:
            state["workflow_step"] = "response_generation"

        logger.info(f"Response planning complete - method: {state['response_method']}")

        return state

    except Exception as e:
        logger.error(f"Error in response planning: {e}")
        from .state import set_error

        return set_error(state, f"Error planning response: {str(e)}")


def response_generation_routing_node(
    state: FinancialOrchestratorState,
) -> FinancialOrchestratorState:
    """
    Route to appropriate response generation method.

    Args:
        state: Current orchestrator state

    Returns:
        Updated state with routing decision
    """
    try:
        logger.info("Routing response generation")

        response_method = state.get("response_method", "rule_based")

        if response_method == "rule_based":
            state["workflow_step"] = "rule_based_response"
        else:
            # Future: LLM response generation
            state["workflow_step"] = "rule_based_response"  # Fallback for now

        return state

    except Exception as e:
        logger.error(f"Error in response generation routing: {e}")
        from .state import set_error

        return set_error(state, f"Error routing response generation: {str(e)}")


def final_response_node(
    state: FinancialOrchestratorState,
) -> FinancialOrchestratorState:
    """
    Generate final response using the selected method.

    Args:
        state: Current orchestrator state

    Returns:
        Updated state with final response
    """
    try:
        logger.info("Generating final response")

        # Handle clarification requests
        if state.get("needs_clarification", False):
            clarification_message = state.get("clarification_message")
            response = default_response_generator.generate_clarification_request(
                clarification_message
            )
        else:
            # Generate response from analysis results
            response_context_data = state.get("response_context", {})
            response_context = ResponseContext()
            response_context.analysis_results = response_context_data.get(
                "analysis_results", {}
            )
            response_context.companies = response_context_data.get("companies", [])
            response_context.analysis_type = response_context_data.get("analysis_type")
            response_context.conversation_context = response_context_data.get(
                "conversation_context", {}
            )
            response_context.user_input = response_context_data.get("user_input", "")
            response_context.error_message = response_context_data.get("error_message")

            response = default_response_generator.generate_response(response_context)

        # Update state with final response
        from .state import update_state_with_agent_response

        state = update_state_with_agent_response(state, response)

        logger.info("Final response generated successfully")

        return state

    except Exception as e:
        logger.error(f"Error generating final response: {e}")
        from .state import set_error, update_state_with_agent_response

        error_state = set_error(state, f"Error generating response: {str(e)}")
        return update_state_with_agent_response(
            error_state, f"I encountered an error: {str(e)}"
        )


# =============================================================================
# ORCHESTRATOR ROUTING FUNCTIONS
# =============================================================================


def route_after_interpretation(state: FinancialOrchestratorState) -> str:
    """
    Route workflow after interpretation based on results.

    Args:
        state: Current orchestrator state

    Returns:
        Next node name to execute
    """
    if state.get("error_message"):
        return "final_response"
    elif state.get("needs_clarification", False):
        return "response_planning"
    else:
        return "analysis_planning"


def route_after_planning(state: FinancialOrchestratorState) -> str:
    """
    Route workflow after analysis planning.

    Args:
        state: Current orchestrator state

    Returns:
        Next node name to execute
    """
    if state.get("error_message"):
        return "final_response"
    else:
        return "data_collection"


def route_after_data_collection(state: FinancialOrchestratorState) -> str:
    """
    Route workflow after data collection.

    Args:
        state: Current orchestrator state

    Returns:
        Next node name to execute
    """
    if state.get("error_message"):
        return "final_response"
    else:
        return "analysis_execution"


def route_after_analysis(state: FinancialOrchestratorState) -> str:
    """
    Route workflow after analysis execution.

    Args:
        state: Current orchestrator state

    Returns:
        Next node name to execute
    """
    if state.get("error_message"):
        return "final_response"
    else:
        return "result_aggregation"


def route_response_generation(state: FinancialOrchestratorState) -> str:
    """
    Route response generation based on method.

    Args:
        state: Current orchestrator state

    Returns:
        Next node name to execute
    """
    return "final_response"  # Always go to final response for now
