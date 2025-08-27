"""
Interpreter Layer for Financial Analysis Requests.

This module handles understanding user requests through rule-based parsing
and prepares for future LLM integration.
"""
import logging
import re
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class RequestInterpretation:
    """Structured representation of an interpreted user request."""
    
    def __init__(self):
        self.companies: List[str] = []
        self.analysis_type: Optional[str] = None
        self.time_period: Optional[str] = None
        self.confidence: float = 0.0
        self.needs_clarification: bool = False
        self.clarification_message: Optional[str] = None
        self.raw_input: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for state storage."""
        return {
            "companies": self.companies,
            "analysis_type": self.analysis_type,
            "time_period": self.time_period,
            "confidence": self.confidence,
            "needs_clarification": self.needs_clarification,
            "clarification_message": self.clarification_message,
            "raw_input": self.raw_input
        }


class BaseInterpreter(ABC):
    """Abstract base class for request interpreters."""
    
    @abstractmethod
    def interpret_request(self, user_input: str, context: Dict[str, Any] = None) -> RequestInterpretation:
        """
        Interpret a user request and return structured information.
        
        Args:
            user_input: Raw user input string
            context: Optional conversation context
            
        Returns:
            RequestInterpretation object with parsed information
        """
        pass


class RuleBasedInterpreter(BaseInterpreter):
    """
    Rule-based interpreter using regex and keyword matching.
    Fast and reliable for common patterns.
    """
    
    def __init__(self):
        """Initialize the rule-based interpreter."""
        # Company name to ticker mapping
        self.company_mappings = {
            'apple': 'AAPL',
            'microsoft': 'MSFT',
            'google': 'GOOGL',
            'alphabet': 'GOOGL',
            'amazon': 'AMZN',
            'tesla': 'TSLA',
            'meta': 'META',
            'facebook': 'META',
            'netflix': 'NFLX',
            'nvidia': 'NVDA',
            'amd': 'AMD',
            'intel': 'INTC',
            'ibm': 'IBM',
            'oracle': 'ORCL',
            'salesforce': 'CRM',
            'adobe': 'ADBE',
            'paypal': 'PYPL',
            'visa': 'V',
            'mastercard': 'MA',
            'jpmorgan': 'JPM',
            'goldman': 'GS',
            'morgan stanley': 'MS',
            'bank of america': 'BAC',
            'wells fargo': 'WFC',
            'coca cola': 'KO',
            'pepsi': 'PEP',
            'walmart': 'WMT',
            'target': 'TGT',
            'home depot': 'HD',
            'disney': 'DIS',
            'boeing': 'BA',
            'caterpillar': 'CAT',
            'general electric': 'GE',
            'ford': 'F',
            'general motors': 'GM'
        }
        
        # Analysis type keywords (order matters - more specific first)
        self.analysis_keywords = {
            'income_statement': ['income', 'revenue', 'earnings', 'profit', 'income statement'],
            'balance_sheet': ['balance', 'assets', 'liabilities', 'equity', 'balance sheet'],
            'cash_flow': ['cash', 'flow', 'cashflow', 'cash flow'],
            'recommendations': ['recommendations', 'analyst', 'rating', 'target', 'price target'],
            'comparison': ['compare', 'comparison', 'vs', 'versus', 'against', 'peer', 'competitors'],
            'metrics': ['metrics', 'ratios', 'performance', 'valuation', 'key metrics'],
            'profile': ['profile', 'company', 'info', 'information', 'about', 'overview', 'summary', 'financials']
        }
        
        # Ticker symbol pattern
        self.ticker_pattern = re.compile(r'\b[A-Z]{1,5}\b')
        
        logger.info("Rule-based interpreter initialized")
    
    def interpret_request(self, user_input: str, context: Dict[str, Any] = None) -> RequestInterpretation:
        """
        Interpret user request using rule-based parsing.
        
        Args:
            user_input: Raw user input string
            context: Optional conversation context
            
        Returns:
            RequestInterpretation with parsed information
        """
        interpretation = RequestInterpretation()
        interpretation.raw_input = user_input
        
        user_input_lower = user_input.lower()
        
        # Extract companies
        interpretation.companies = self._extract_companies(user_input, user_input_lower, context)
        
        # Determine analysis type
        interpretation.analysis_type = self._determine_analysis_type(user_input_lower, interpretation.companies)
        
        # Set confidence based on what we found
        interpretation.confidence = self._calculate_confidence(interpretation)
        
        # Check if clarification is needed
        if not interpretation.companies and not self._has_context_companies(context):
            interpretation.needs_clarification = True
            interpretation.clarification_message = (
                "I'd be happy to help with financial analysis! "
                "Could you please specify which company or companies you'd like me to analyze? "
                "You can use ticker symbols (like AAPL, MSFT) or company names (like Apple, Microsoft)."
            )
        
        logger.info(f"Interpreted request - Companies: {interpretation.companies}, "
                   f"Analysis: {interpretation.analysis_type}, Confidence: {interpretation.confidence}")
        
        return interpretation
    
    def _extract_companies(self, user_input: str, user_input_lower: str, context: Dict[str, Any]) -> List[str]:
        """Extract company ticker symbols from user input."""
        companies = []
        
        # Common words that are NOT ticker symbols but match the pattern
        # Include common English words, prepositions, articles, etc.
        false_positive_words = {
            # Common prepositions and articles
            'FOR', 'THE', 'AND', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HAD', 'HER', 'WAS', 'ONE', 
            'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 
            'OLD', 'SEE', 'TWO', 'WHO', 'BOY', 'DID', 'LET', 'PUT', 'SAY', 'SHE', 'TOO', 
            'USE', 'WAY', 'WHY', 'WIN', 'YES', 'YET', 'BIG', 'END', 'FAR', 'FEW', 'GOT', 'LOT',
            'MAN', 'OWN', 'RUN', 'SET', 'TOP', 'TRY', 'ASK', 'BAD', 'BAG', 'BED', 'BOX', 'BUY',
            'CAR', 'CUT', 'EAR', 'EYE', 'FUN', 'GUN', 'JOB', 'KEY', 'LAW', 'LEG', 'MAP', 'MOM',
            'POP', 'RED', 'SIT', 'SIX', 'SUN', 'TAX', 'TEA', 'TEN', 'VAN', 'WAR', 'ZIP',
            # Common words in financial queries
            'SHOW', 'WHAT', 'TELL', 'GIVE', 'FIND', 'LOOK', 'INFO', 'DATA', 'HELP', 'ABOUT',
            'FROM', 'WITH', 'THAT', 'THIS', 'THEY', 'THEM', 'THAN', 'WHEN', 'WHERE', 'WHICH',
            'WILL', 'WOULD', 'COULD', 'SHOULD', 'MIGHT', 'MUST', 'SHALL', 'OUGHT', 'NEED',
            'WANT', 'LIKE', 'LOVE', 'HATE', 'KNOW', 'THINK', 'FEEL', 'SEEM', 'LOOK', 'SOUND',
            'MAKE', 'TAKE', 'COME', 'GIVE', 'KEEP', 'TURN', 'MOVE', 'PLAY', 'WORK', 'LIVE',
            'SHEET', 'FLOW', 'CASH', 'DEBT', 'RISK', 'RATE', 'YEAR', 'TIME', 'WEEK', 'MONTH',
            'HIGH', 'LOW', 'GOOD', 'BEST', 'LAST', 'NEXT', 'FIRST', 'FINAL', 'TOTAL', 'FULL',
            'QUICK', 'FAST', 'SLOW', 'LONG', 'SHORT', 'SMALL', 'LARGE', 'GREAT', 'REAL', 'TRUE',
            # Additional common words
            'ARE', 'IS', 'BE', 'BEEN', 'BEING', 'HAVE', 'HAS', 'HAD', 'DO', 'DOES', 'DID', 'DONE',
            'WILL', 'WOULD', 'COULD', 'SHOULD', 'MAY', 'MIGHT', 'MUST', 'CAN', 'CANT', 'WONT',
            'ME', 'MY', 'MINE', 'WE', 'US', 'OURS', 'THEY', 'THEM', 'THEIR', 'THEIRS',
            # Company name words that aren't tickers
            'INTEL', 'APPLE', 'GOOGLE', 'AMAZON', 'TESLA', 'MICROSOFT', 'META', 'NVIDIA'
        }
        
        # Find company names first (more reliable)
        found_company_names = []
        for company_name, ticker in self.company_mappings.items():
            if company_name in user_input_lower:
                if ticker not in companies:
                    companies.append(ticker)
                    found_company_names.append(company_name)
        
        # Find ticker symbols using regex, but filter out false positives
        potential_tickers = self.ticker_pattern.findall(user_input.upper())
        for ticker in potential_tickers:
            # Skip if it's a common word that's not a ticker
            if ticker in false_positive_words:
                continue
            
            # Skip if we already found this company by name
            ticker_company_name = None
            for name, mapped_ticker in self.company_mappings.items():
                if mapped_ticker == ticker:
                    ticker_company_name = name
                    break
            
            if ticker_company_name and ticker_company_name in found_company_names:
                continue  # Already added this company by name
            
            # Add the ticker if it's not already in the list
            if ticker not in companies:
                companies.append(ticker)
        
        # Handle pronouns and context references
        if not companies and context:
            context_companies = context.get('companies', [])
            if context_companies and any(word in user_input_lower for word in ['it', 'them', 'they', 'this', 'that']):
                companies = context_companies.copy()
        
        return companies
    
    def _determine_analysis_type(self, user_input_lower: str, companies: List[str]) -> Optional[str]:
        """Determine the type of analysis requested."""
        # Check for explicit analysis type keywords
        for analysis_type, keywords in self.analysis_keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return analysis_type
        
        # Default logic based on number of companies
        if len(companies) > 1:
            return "comparison"
        elif len(companies) == 1:
            return "profile"
        
        return None
    
    def _calculate_confidence(self, interpretation: RequestInterpretation) -> float:
        """Calculate confidence score for the interpretation."""
        confidence = 0.0
        
        # Base confidence for finding companies
        if interpretation.companies:
            confidence += 0.5
        
        # Additional confidence for clear analysis type
        if interpretation.analysis_type:
            confidence += 0.3
        
        # Bonus for specific analysis keywords
        if interpretation.analysis_type in ['income_statement', 'balance_sheet', 'cash_flow']:
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _has_context_companies(self, context: Dict[str, Any]) -> bool:
        """Check if there are companies in the conversation context."""
        if not context:
            return False
        return bool(context.get('companies', []))


class LLMInterpreter(BaseInterpreter):
    """
    LLM-powered interpreter for complex natural language understanding.
    Future implementation for Phase 2.
    """
    
    def __init__(self, llm_client=None):
        """Initialize LLM interpreter (placeholder for future implementation)."""
        self.llm_client = llm_client
        logger.info("LLM interpreter initialized (placeholder)")
    
    def interpret_request(self, user_input: str, context: Dict[str, Any] = None) -> RequestInterpretation:
        """
        Interpret user request using LLM (future implementation).
        
        Args:
            user_input: Raw user input string
            context: Optional conversation context
            
        Returns:
            RequestInterpretation with parsed information
        """
        # Placeholder implementation - falls back to rule-based for now
        rule_based = RuleBasedInterpreter()
        interpretation = rule_based.interpret_request(user_input, context)
        
        # Mark as LLM-enhanced (future)
        interpretation.confidence = min(interpretation.confidence + 0.1, 1.0)
        
        logger.info("LLM interpretation (using rule-based fallback)")
        return interpretation


class HybridInterpreter(BaseInterpreter):
    """
    Hybrid interpreter that chooses between rule-based and LLM interpretation
    based on request complexity and confidence thresholds.
    """
    
    def __init__(self, llm_client=None, confidence_threshold: float = 0.7):
        """
        Initialize hybrid interpreter.
        
        Args:
            llm_client: Optional LLM client for complex requests
            confidence_threshold: Threshold for using rule-based vs LLM
        """
        self.rule_based = RuleBasedInterpreter()
        self.llm_interpreter = LLMInterpreter(llm_client) if llm_client else None
        self.confidence_threshold = confidence_threshold
        
        logger.info(f"Hybrid interpreter initialized (threshold: {confidence_threshold})")
    
    def interpret_request(self, user_input: str, context: Dict[str, Any] = None) -> RequestInterpretation:
        """
        Interpret user request using hybrid approach.
        
        Args:
            user_input: Raw user input string
            context: Optional conversation context
            
        Returns:
            RequestInterpretation with parsed information
        """
        # Always try rule-based first (fast path)
        rule_interpretation = self.rule_based.interpret_request(user_input, context)
        
        # If confidence is high enough, use rule-based result
        if rule_interpretation.confidence >= self.confidence_threshold:
            logger.info("Using rule-based interpretation (high confidence)")
            return rule_interpretation
        
        # If LLM is available and confidence is low, try LLM interpretation
        if self.llm_interpreter and rule_interpretation.confidence < self.confidence_threshold:
            logger.info("Attempting LLM interpretation (low confidence)")
            llm_interpretation = self.llm_interpreter.interpret_request(user_input, context)
            
            # Use LLM result if it has higher confidence
            if llm_interpretation.confidence > rule_interpretation.confidence:
                return llm_interpretation
        
        # Fall back to rule-based interpretation
        logger.info("Using rule-based interpretation (fallback)")
        return rule_interpretation


# Default interpreter instance
default_interpreter = HybridInterpreter()