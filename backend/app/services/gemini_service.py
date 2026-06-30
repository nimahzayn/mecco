"""
Gemini API Service Module (Placeholder)

This file is a placeholder for Member 2.

PURPOSE:
Handle all interactions with Google's Gemini API.

RESPONSIBILITIES:
1. Prompt construction
2. API calls to Gemini
3. Response parsing and validation
4. Error handling and retries
5. Rate limiting management

INTEGRATION POINTS:
- Will be called by chat_service.py
- Will receive context from rag_service.py
- Will use configuration from config.py (GEMINI_API_KEY)

TODO for Member 2:
- Set up Gemini API client
- Implement prompt engineering
- Handle API responses
- Implement error handling and retries
"""


class GeminiService:
    """
    Gemini API service for generating AI responses.
    
    TODO: Implement the following methods:
    - generate_response(message: str, context: str) -> str
    - construct_prompt(message: str, context: str) -> str
    - call_gemini_api(prompt: str) -> Dict
    - parse_response(api_response: Dict) -> str
    """
    
    def __init__(self):
        """Initialize Gemini service."""
        pass
    
    def generate_response(self, message: str, context: str = None):
        """
        Generate AI response using Gemini API.
        
        Args:
            message: User message
            context: Retrieved context from RAG
        
        Returns:
            Generated response text
        
        TODO: Implement Gemini API integration
        """
        raise NotImplementedError("Gemini service will be implemented by Member 2")