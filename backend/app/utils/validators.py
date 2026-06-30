"""
Request Validation Module

Validates incoming API requests.
"""

from typing import Dict, Tuple, Optional
from flask import current_app


def validate_chat_request(data: Dict) -> Tuple[bool, Optional[str]]:
    """
    Validate chat API request data.
    
    Args:
        data: Request JSON data
    
    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    
    # Check if data exists
    if not data:
        return False, "Request body is required"
    
    # Check if message field exists
    if 'message' not in data:
        return False, "Missing required field: 'message'"
    
    message = data.get('message', '')
    
    # Check if message is empty
    if not message or not message.strip():
        return False, "Message cannot be empty"
    
    # Check message length
    max_length = current_app.config.get('MAX_MESSAGE_LENGTH', 500)
    if len(message) > max_length:
        return False, f"Message exceeds maximum length of {max_length} characters"
    
    # Message is valid
    return True, None


def sanitize_message(message: str) -> str:
    """
    Sanitize user message by removing extra whitespace.
    
    Args:
        message: User message
    
    Returns:
        str: Sanitized message
    """
    return ' '.join(message.strip().split())