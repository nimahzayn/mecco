"""
Chat Routes Module

Handles all chat-related API endpoints.

Routes should be thin - they only handle HTTP request/response.
All business logic belongs in services.
"""

from flask import Blueprint, request, jsonify, current_app
from app.services.chat_service import ChatService
from app.utils.validators import validate_chat_request, sanitize_message
from app.utils.errors import create_error_response
from app.utils.logger import log_request

# Create blueprint
chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/chat', methods=['POST'])
def send_message():
    """
    Send a message and receive AI response.
    
    Request Body:
        {
            "message": "User's question",
            "conversation_id": "optional-conversation-id"
        }
    
    Response:
        {
            "success": true,
            "response": "AI generated response",
            "conversation_id": "conv-123456",
            "timestamp": "2024-01-01T12:00:00Z",
            "metadata": {...}
        }
    
    Error Response:
        {
            "success": false,
            "error": "Error message",
            "status_code": 400
        }
    """
    try:
        # Get request data
        data = request.get_json()
        
        # Validate request
        is_valid, error_message = validate_chat_request(data)
        if not is_valid:
            current_app.logger.warning(f"Invalid request: {error_message}")
            return create_error_response(error_message, 400)
        
        # Extract and sanitize message
        message = sanitize_message(data['message'])
        conversation_id = data.get('conversation_id', None)
        
        # Log request
        current_app.logger.info(f"Chat request received: {message[:50]}...")
        
        # Call chat service
        chat_service = ChatService()
        response_data = chat_service.get_response(message, conversation_id)
        
        # Build success response
        response = {
            'success': True,
            **response_data
        }
        
        # Log response
        log_request(current_app.logger, 'POST', '/api/chat', 200)
        
        return jsonify(response), 200
        
    except Exception as e:
        current_app.logger.error(f"Error in chat endpoint: {str(e)}")
        return create_error_response(
            "An error occurred processing your request. Please try again.",
            500
        )


@chat_bp.route('/chat/history/<conversation_id>', methods=['GET'])
def get_conversation_history(conversation_id):
    """
    Get conversation history.
    
    Path Parameters:
        conversation_id: ID of the conversation
    
    Response:
        {
            "success": true,
            "conversation_id": "conv-123456",
            "messages": [...],
            "created_at": "2024-01-01T12:00:00Z"
        }
    
    TODO for Member 2:
    Implement conversation history retrieval when database is set up.
    """
    try:
        chat_service = ChatService()
        
        # Validate conversation exists
        if not chat_service.validate_conversation(conversation_id):
            return create_error_response("Conversation not found", 404)
        
        # Get history
        history = chat_service.get_conversation_history(conversation_id)
        
        response = {
            'success': True,
            **history
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        current_app.logger.error(f"Error retrieving conversation history: {str(e)}")
        return create_error_response(
            "An error occurred retrieving conversation history.",
            500
        )