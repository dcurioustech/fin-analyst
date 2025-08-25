"""
Simple Chat Interface for Financial Analysis using LangGraph.

This provides a basic conversational interface that demonstrates
the LangGraph integration for financial analysis.
"""
import os
import logging
from typing import Optional
from dotenv import load_dotenv

from agents.graph import financial_orchestrator
from agents.state import FinancialOrchestratorState
from utils.error_handling import setup_logging
from config.settings import configure_pandas

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class FinancialChatInterface:
    """
    Simple chat interface for financial analysis conversations.
    """
    
    def __init__(self):
        """Initialize the chat interface."""
        # Set up logging
        setup_logging('INFO')
        
        # Configure pandas
        configure_pandas()
        
        # Initialize conversation state
        self.current_state: Optional[FinancialOrchestratorState] = None
        
        logger.info("Financial Chat Interface initialized")
    
    def start_chat(self) -> None:
        """Start the interactive chat session."""
        print("=" * 60)
        print("🏦 Financial Analysis Assistant (LangGraph Powered)")
        print("=" * 60)
        
        # Check for Google API key
        if not os.getenv("GOOGLE_API_KEY"):
            print("⚠️  Warning: GOOGLE_API_KEY not found in environment variables.")
            print("   The LangGraph integration requires a Google API key for Gemini.")
            print("   For now, you can still use the basic analysis features.")
            print()
        
        # Start conversation
        self.current_state = financial_orchestrator.start_conversation()
        print(f"🤖 {self.current_state['agent_response']}")
        print()
        
        # Main chat loop
        try:
            self._chat_loop()
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using the Financial Analysis Assistant!")
        except Exception as e:
            logger.error(f"Unexpected error in chat loop: {e}")
            print(f"\n❌ An unexpected error occurred: {e}")
    
    def _chat_loop(self) -> None:
        """Main chat interaction loop."""
        while True:
            # Get user input
            try:
                user_input = input("💬 You: ").strip()
            except EOFError:
                break
            
            if not user_input:
                continue
            
            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("👋 Goodbye! Thanks for using the Financial Analysis Assistant!")
                break
            
            # Check for help command
            if user_input.lower() in ['help', '?']:
                self._show_help()
                continue
            
            # Check for clear command
            if user_input.lower() in ['clear', 'reset']:
                self.current_state = financial_orchestrator.start_conversation()
                print("🔄 Conversation reset!")
                print(f"🤖 {self.current_state['agent_response']}")
                continue
            
            # Process the message
            print("🔄 Analyzing...")
            try:
                self.current_state = financial_orchestrator.process_user_request(user_input, self.current_state)
                
                # Display response
                response = self.current_state.get('agent_response', 'I apologize, but I was unable to process your request.')
                print(f"\n🤖 {response}")
                
                # Show conversation context if available
                if self.current_state.get('companies'):
                    companies_str = ', '.join(self.current_state['companies'])
                    print(f"📊 Current context: {companies_str}")
                
                print()
                
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                print(f"❌ I encountered an error: {str(e)}")
                print("Please try again or type 'help' for assistance.")
                print()
    
    def _show_help(self) -> None:
        """Display help information."""
        help_text = """
🆘 Financial Analysis Assistant Help

📝 What you can ask:
• "Analyze Apple" or "Tell me about AAPL"
• "Compare Apple and Microsoft"
• "Show me Tesla's financial metrics"
• "What are Amazon's earnings?"
• "Analyze GOOGL's balance sheet"

🎯 Supported Analysis Types:
• Company profiles and basic information
• Financial metrics and ratios
• Financial statements (income, balance sheet, cash flow)
• Company comparisons
• Analyst recommendations

💡 Tips:
• Use company names (Apple, Microsoft) or ticker symbols (AAPL, MSFT)
• Ask follow-up questions - I remember our conversation context
• Be specific about what type of analysis you want

🔧 Commands:
• 'help' or '?' - Show this help
• 'clear' or 'reset' - Start a new conversation
• 'exit', 'quit', 'bye' - Exit the chat

Example conversations:
💬 "Analyze Apple's financials"
💬 "How does Tesla compare to Ford?"
💬 "Show me Microsoft's income statement"
        """
        print(help_text)


def main():
    """Main entry point for the chat interface."""
    chat = FinancialChatInterface()
    chat.start_chat()


if __name__ == "__main__":
    main()