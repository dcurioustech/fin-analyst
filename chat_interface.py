"""
Enhanced Chat Interface for Financial Analysis using LangGraph.

This provides a conversational interface that works both locally
and with GCP services for session persistence and caching.
"""
import os
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

from agents.graph import financial_orchestrator
from agents.state import FinancialOrchestratorState, create_initial_state
from utils.error_handling import setup_logging
from config.settings import configure_pandas
from config.gcp_config import get_gcp_service_manager, is_gcp_available

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class FinancialChatInterface:
    """
    Enhanced chat interface for financial analysis conversations.
    Supports both local and GCP-backed session persistence.
    """
    
    def __init__(self, session_id: Optional[str] = None):
        """Initialize the chat interface."""
        # Set up logging
        setup_logging('INFO')
        
        # Configure pandas
        configure_pandas()
        
        # Session management
        self.session_id = session_id or f"cli_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.current_state: Optional[FinancialOrchestratorState] = None
        
        # GCP services (if available)
        self.gcp_manager = get_gcp_service_manager() if is_gcp_available() else None
        self.use_gcp = self.gcp_manager is not None
        
        # Local session storage (fallback)
        self.local_sessions_file = "data/cache/sessions.json"
        os.makedirs(os.path.dirname(self.local_sessions_file), exist_ok=True)
        
        logger.info(f"Financial Chat Interface initialized (Session: {self.session_id}, GCP: {self.use_gcp})")
    
    def start_chat(self) -> None:
        """Start the interactive chat session."""
        print("=" * 60)
        print("🏦 Financial Analysis Assistant (Enhanced)")
        print("=" * 60)
        print(f"Session ID: {self.session_id}")
        print(f"Backend: {'GCP' if self.use_gcp else 'Local'}")
        print("=" * 60)
        
        # Check for API keys
        api_keys = self._check_api_keys()
        if not api_keys.get('google_api_key'):
            print("⚠️  Warning: GOOGLE_API_KEY not found.")
            print("   The LangGraph integration requires a Google API key for Gemini.")
            print("   You can still use basic analysis features.")
            print()
        
        # Load or start conversation
        self.current_state = self._load_session_state()
        if not self.current_state:
            self.current_state = financial_orchestrator.start_conversation()
            self._save_session_state()
        
        print(f"🤖 {self.current_state['agent_response']}")
        
        # Show session context if available
        if self.current_state.get('companies'):
            companies_str = ', '.join(self.current_state['companies'])
            print(f"📊 Current context: {companies_str}")
        
        print()
        
        # Main chat loop
        try:
            self._chat_loop()
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using the Financial Analysis Assistant!")
        except Exception as e:
            logger.error(f"Unexpected error in chat loop: {e}")
            print(f"\n❌ An unexpected error occurred: {e}")
        finally:
            logger.info("Financial Analysis Assistant shutting down")
            self._save_session_state()  # Save final state
    
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
                
                # Save updated state
                self._save_session_state()
                
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
    main()    def
 _check_api_keys(self) -> Dict[str, Optional[str]]:
        """Check and return available API keys."""
        if self.gcp_manager:
            return self.gcp_manager.get_api_keys()
        else:
            return {
                'google_api_key': os.getenv('GOOGLE_API_KEY'),
                'alpha_vantage_key': os.getenv('ALPHA_VANTAGE_API_KEY'),
                'polygon_key': os.getenv('POLYGON_API_KEY')
            }
    
    def _load_session_state(self) -> Optional[FinancialOrchestratorState]:
        """Load session state from storage."""
        try:
            # Try GCP Firestore first
            if self.use_gcp and self.gcp_manager:
                doc = self.gcp_manager.firestore_client.collection("sessions").document(self.session_id).get()
                if doc.exists:
                    logger.info(f"Loaded session state from Firestore: {self.session_id}")
                    return doc.to_dict()
            
            # Fallback to local file storage
            if os.path.exists(self.local_sessions_file):
                with open(self.local_sessions_file, 'r') as f:
                    sessions = json.load(f)
                    if self.session_id in sessions:
                        logger.info(f"Loaded session state from local file: {self.session_id}")
                        return sessions[self.session_id]
            
        except Exception as e:
            logger.error(f"Error loading session state: {e}")
        
        return None
    
    def _save_session_state(self):
        """Save session state to storage."""
        if not self.current_state:
            return
        
        try:
            # Save to GCP Firestore
            if self.use_gcp and self.gcp_manager:
                self.gcp_manager.firestore_client.collection("sessions").document(self.session_id).set(self.current_state)
                logger.debug(f"Saved session state to Firestore: {self.session_id}")
            
            # Always save to local file as backup
            sessions = {}
            if os.path.exists(self.local_sessions_file):
                with open(self.local_sessions_file, 'r') as f:
                    sessions = json.load(f)
            
            sessions[self.session_id] = self.current_state
            
            with open(self.local_sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2, default=str)
            
            logger.debug(f"Saved session state to local file: {self.session_id}")
            
        except Exception as e:
            logger.error(f"Error saving session state: {e}")
    
    def clear_session(self):
        """Clear the current session state."""
        try:
            # Clear from GCP Firestore
            if self.use_gcp and self.gcp_manager:
                self.gcp_manager.firestore_client.collection("sessions").document(self.session_id).delete()
            
            # Clear from local file
            if os.path.exists(self.local_sessions_file):
                with open(self.local_sessions_file, 'r') as f:
                    sessions = json.load(f)
                
                if self.session_id in sessions:
                    del sessions[self.session_id]
                    
                    with open(self.local_sessions_file, 'w') as f:
                        json.dump(sessions, f, indent=2, default=str)
            
            # Reset current state
            self.current_state = financial_orchestrator.start_conversation()
            self._save_session_state()
            
            print("🔄 Session cleared! Starting fresh conversation.")
            
        except Exception as e:
            logger.error(f"Error clearing session: {e}")
            print(f"❌ Error clearing session: {e}")


def main():
    """Main entry point for the enhanced chat interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Financial Analysis Assistant Chat Interface")
    parser.add_argument("--session-id", help="Session ID to resume or create")
    parser.add_argument("--clear-session", action="store_true", help="Clear session before starting")
    
    args = parser.parse_args()
    
    chat = FinancialChatInterface(session_id=args.session_id)
    
    if args.clear_session:
        chat.clear_session()
    
    chat.start_chat()