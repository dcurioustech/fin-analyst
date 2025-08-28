"""
Response Generation Layer for Financial Analysis.

This module handles formatting analysis results into user-friendly responses
using rule-based templates and preparing for future LLM integration.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ui.display_formatter import DisplayFormatter

logger = logging.getLogger(__name__)


class ResponseContext:
    """Context information for response generation."""

    def __init__(self):
        self.analysis_results: Dict[str, Any] = {}
        self.companies: list = []
        self.analysis_type: Optional[str] = None
        self.conversation_context: Dict[str, Any] = {}
        self.error_message: Optional[str] = None
        self.user_input: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for state storage."""
        return {
            "analysis_results": self.analysis_results,
            "companies": self.companies,
            "analysis_type": self.analysis_type,
            "conversation_context": self.conversation_context,
            "error_message": self.error_message,
            "user_input": self.user_input,
        }


class BaseResponseGenerator(ABC):
    """Abstract base class for response generators."""

    @abstractmethod
    def generate_response(self, context: ResponseContext) -> str:
        """
        Generate a response based on the provided context.

        Args:
            context: ResponseContext with analysis results and metadata

        Returns:
            Formatted response string
        """
        pass


class RuleBasedResponseGenerator(BaseResponseGenerator):
    """
    Rule-based response generator using existing display formatters.
    Fast and consistent formatting for structured analysis results.
    """

    def __init__(self):
        """Initialize the rule-based response generator."""
        self.display_formatter = DisplayFormatter()

        # Response templates for different scenarios
        self.templates = {
            "welcome": (
                "Hello! I'm your Financial Analysis Assistant. "
                "I can help you analyze companies, compare stocks, and provide financial insights. "
                "Just tell me which company you'd like to analyze or ask me a financial question!"
            ),
            "clarification": (
                "I'd be happy to help with financial analysis! "
                "Could you please specify which company or companies you'd like me to analyze? "
                "You can use ticker symbols (like AAPL, MSFT) or company names (like Apple, Microsoft)."
            ),
            "error": "I encountered an error: {error_message}",
            "no_results": "I wasn't able to generate analysis results for your request. Please try again with a specific company or request.",
            "context_update": "📊 Current context: {companies}",
        }

        logger.info("Rule-based response generator initialized")

    def generate_response(self, context: ResponseContext) -> str:
        """
        Generate response using rule-based formatting.

        Args:
            context: ResponseContext with analysis results and metadata

        Returns:
            Formatted response string
        """
        # Handle errors first
        if context.error_message:
            return self.templates["error"].format(error_message=context.error_message)

        # Handle empty results
        if not context.analysis_results:
            return self.templates["no_results"]

        try:
            response_parts = []

            # Format each analysis result
            for key, result in context.analysis_results.items():
                if not result.get("success", False):
                    continue

                formatted_result = self._format_analysis_result(key, result, context)
                if formatted_result:
                    response_parts.append(formatted_result)

            if response_parts:
                response = "\n\n".join(response_parts)

                # Add context information if helpful
                if context.companies:
                    companies_str = ", ".join(context.companies)
                    response += f"\n\n{self.templates['context_update'].format(companies=companies_str)}"

                return response
            else:
                return self.templates["no_results"]

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I encountered an error generating the response: {str(e)}"

    def _format_analysis_result(
        self, result_key: str, result: Dict[str, Any], context: ResponseContext
    ) -> Optional[str]:
        """
        Format a single analysis result using appropriate formatter.

        Args:
            result_key: Key identifying the type of result
            result: Analysis result dictionary
            context: Response context for additional information

        Returns:
            Formatted result string or None if formatting fails
        """
        try:
            # Determine formatting method based on result key
            if "profile" in result_key:
                return self.display_formatter.format_company_profile(result)
            elif "metrics" in result_key:
                return self.display_formatter.format_metrics_display(result)
            elif "comparison" in result_key:
                return self.display_formatter.format_comparison_display(result)
            elif any(
                stmt in result_key
                for stmt in ["income_statement", "balance_sheet", "cash_flow"]
            ):
                statement_name = self._extract_statement_name(result_key)
                return self.display_formatter.format_statement_display(
                    result, statement_name
                )
            elif "recommendations" in result_key:
                return self.display_formatter.format_recommendations_display(result)
            else:
                # Generic formatting for unknown result types
                return str(result.get("data", result))

        except Exception as e:
            logger.error(f"Error formatting result {result_key}: {e}")
            return f"Error formatting {result_key}: {str(e)}"

    def _extract_statement_name(self, result_key: str) -> str:
        """Extract and format statement name from result key."""
        if "income_statement" in result_key:
            return "Income Statement"
        elif "balance_sheet" in result_key:
            return "Balance Sheet"
        elif "cash_flow" in result_key:
            return "Cash Flow Statement"
        else:
            return "Financial Statement"

    def generate_welcome_message(self) -> str:
        """Generate welcome message for new conversations."""
        return self.templates["welcome"]

    def generate_clarification_request(self, message: str = None) -> str:
        """Generate clarification request message."""
        return message or self.templates["clarification"]


class LLMResponseGenerator(BaseResponseGenerator):
    """
    LLM-powered response generator for natural, conversational responses.
    Future implementation for Phase 2.
    """

    def __init__(self, llm_client=None):
        """Initialize LLM response generator (placeholder for future implementation)."""
        self.llm_client = llm_client
        self.fallback_generator = RuleBasedResponseGenerator()

        logger.info("LLM response generator initialized (placeholder)")

    def generate_response(self, context: ResponseContext) -> str:
        """
        Generate response using LLM (future implementation).

        Args:
            context: ResponseContext with analysis results and metadata

        Returns:
            Formatted response string
        """
        # Placeholder implementation - falls back to rule-based for now
        logger.info("LLM response generation (using rule-based fallback)")
        return self.fallback_generator.generate_response(context)


class HybridResponseGenerator(BaseResponseGenerator):
    """
    Hybrid response generator that chooses between rule-based and LLM generation
    based on response complexity and user preferences.
    """

    def __init__(self, llm_client=None, use_llm_for_complex: bool = False):
        """
        Initialize hybrid response generator.

        Args:
            llm_client: Optional LLM client for complex responses
            use_llm_for_complex: Whether to use LLM for complex responses
        """
        self.rule_based = RuleBasedResponseGenerator()
        self.llm_generator = LLMResponseGenerator(llm_client) if llm_client else None
        self.use_llm_for_complex = (
            use_llm_for_complex and self.llm_generator is not None
        )

        logger.info(
            f"Hybrid response generator initialized (LLM enabled: {self.use_llm_for_complex})"
        )

    def generate_response(self, context: ResponseContext) -> str:
        """
        Generate response using hybrid approach.

        Args:
            context: ResponseContext with analysis results and metadata

        Returns:
            Formatted response string
        """
        # For now, always use rule-based (fast and reliable)
        # Future: Add logic to determine when to use LLM

        if self.use_llm_for_complex and self._is_complex_response(context):
            logger.info("Using LLM response generation (complex response)")
            return self.llm_generator.generate_response(context)
        else:
            logger.info("Using rule-based response generation")
            return self.rule_based.generate_response(context)

    def _is_complex_response(self, context: ResponseContext) -> bool:
        """
        Determine if response is complex enough to warrant LLM generation.

        Args:
            context: ResponseContext to evaluate

        Returns:
            True if response is considered complex
        """
        # Future logic for determining complexity
        # For now, always return False to use rule-based
        return False

    def generate_welcome_message(self) -> str:
        """Generate welcome message for new conversations."""
        return self.rule_based.generate_welcome_message()

    def generate_clarification_request(self, message: str = None) -> str:
        """Generate clarification request message."""
        return self.rule_based.generate_clarification_request(message)


# Default response generator instance
default_response_generator = HybridResponseGenerator()
