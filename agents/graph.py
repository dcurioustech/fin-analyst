"""
LangGraph Orchestrator Workflow for Financial Analysis.

This module defines the main orchestrator graph that manages
the financial analysis workflow with clear layer separation.
"""

import logging
from typing import Any, Dict

from langgraph.graph import END, StateGraph

from .nodes import (
    analysis_execution_node,
    analysis_planning_node,
    data_collection_node,
    final_response_node,
    interpreter_routing_node,
    orchestrator_entry_node,
    response_generation_routing_node,
    response_planning_node,
    result_aggregation_node,
    route_after_analysis,
    route_after_data_collection,
    route_after_interpretation,
    route_after_planning,
    route_response_generation,
)
from .response_generator import default_response_generator
from .state import (
    FinancialOrchestratorState,
    create_initial_state,
    update_state_with_agent_response,
    update_state_with_user_input,
)

logger = logging.getLogger(__name__)


class FinancialAnalysisOrchestrator:
    """
    LangGraph orchestrator for financial analysis workflows.
    """

    def __init__(self):
        """Initialize the financial analysis orchestrator."""
        self.graph = self._build_graph()
        self.app = self.graph.compile()
        logger.info("Financial Analysis Orchestrator initialized")

    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph orchestrator workflow.

        Returns:
            Compiled StateGraph for financial analysis orchestration
        """
        # Create the graph
        workflow = StateGraph(FinancialOrchestratorState)

        # Add orchestrator nodes
        workflow.add_node("orchestrator_entry", orchestrator_entry_node)
        workflow.add_node("interpreter_routing", interpreter_routing_node)
        workflow.add_node("analysis_planning", analysis_planning_node)
        workflow.add_node("data_collection", data_collection_node)
        workflow.add_node("analysis_execution", analysis_execution_node)
        workflow.add_node("result_aggregation", result_aggregation_node)
        workflow.add_node("response_planning", response_planning_node)
        workflow.add_node(
            "response_generation_routing", response_generation_routing_node
        )
        workflow.add_node("final_response", final_response_node)

        # Set entry point
        workflow.set_entry_point("orchestrator_entry")

        # Add workflow edges
        workflow.add_edge("orchestrator_entry", "interpreter_routing")

        # Conditional routing after interpretation
        workflow.add_conditional_edges(
            "interpreter_routing",
            route_after_interpretation,
            {
                "analysis_planning": "analysis_planning",
                "response_planning": "response_planning",
                "final_response": "final_response",
            },
        )

        # Conditional routing after planning
        workflow.add_conditional_edges(
            "analysis_planning",
            route_after_planning,
            {"data_collection": "data_collection", "final_response": "final_response"},
        )

        # Conditional routing after data collection
        workflow.add_conditional_edges(
            "data_collection",
            route_after_data_collection,
            {
                "analysis_execution": "analysis_execution",
                "final_response": "final_response",
            },
        )

        # Conditional routing after analysis
        workflow.add_conditional_edges(
            "analysis_execution",
            route_after_analysis,
            {
                "result_aggregation": "result_aggregation",
                "final_response": "final_response",
            },
        )

        # Result aggregation goes to response planning
        workflow.add_edge("result_aggregation", "response_planning")

        # Response planning goes to response generation routing
        workflow.add_edge("response_planning", "response_generation_routing")

        # Response generation routing goes to final response
        workflow.add_conditional_edges(
            "response_generation_routing",
            route_response_generation,
            {"final_response": "final_response"},
        )

        # Final response goes to END
        workflow.add_edge("final_response", END)

        return workflow

    def process_user_request(
        self, user_input: str, state: FinancialOrchestratorState = None
    ) -> FinancialOrchestratorState:
        """
        Process a user request through the orchestrator workflow.

        Args:
            user_input: User's input message
            state: Current conversation state (optional, creates new if None)

        Returns:
            Updated state with agent response
        """
        try:
            # Create or update state
            if state is None:
                state = create_initial_state()

            # Update state with user input
            state = update_state_with_user_input(state, user_input)

            logger.info(f"Processing user request: {user_input[:100]}...")

            # Run the orchestrator workflow
            result = self.app.invoke(state)

            logger.info("User request processed successfully")
            return result

        except Exception as e:
            logger.error(f"Error processing user request: {e}")

            # Create error response
            error_response = f"I encountered an error processing your request: {str(e)}"
            if state is None:
                state = create_initial_state()

            state = update_state_with_user_input(state, user_input)
            state = update_state_with_agent_response(state, error_response)
            from .state import set_error

            state = set_error(state, str(e))

            return state

    def start_conversation(self) -> FinancialOrchestratorState:
        """
        Start a new conversation with a welcome message.

        Returns:
            Initial state with welcome message
        """
        state = create_initial_state()
        welcome_message = default_response_generator.generate_welcome_message()

        state = update_state_with_agent_response(state, welcome_message)
        logger.info("Started new conversation")

        return state


# Global instance for easy access
financial_orchestrator = FinancialAnalysisOrchestrator()
