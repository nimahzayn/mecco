"""
Error Handling Module

Defines custom error handlers and error response formatting.
"""

from flask import jsonify
from werkzeug.exceptions import HTTPException
import traceback


def register_error_handlers(app):
    """
    Register custom error handlers with Flask app.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify({
            'success': False,
            'error': 'Bad Request',
            'message': str(error.description) if hasattr(error, 'description') else 'Invalid request',
            'status_code': 400
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({
            'success': False,
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status_code': 404
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors."""
        return jsonify({
            'success': False,
            'error': 'Method Not Allowed',
            'message': 'The method is not allowed for the requested URL',
            'status_code': 405
        }), 405
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error."""
        app.logger.error(f"Internal Server Error: {str(error)}")
        app.logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred. Please try again later.',
            'status_code': 500
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all unhandled exceptions."""
        
        # Pass through HTTP errors
        if isinstance(error, HTTPException):
            return error
        
        # Log the error
        app.logger.error(f"Unhandled Exception: {str(error)}")
        app.logger.error(traceback.format_exc())
        
        # Return JSON response
        return jsonify({
            'success': False,
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred. Please try again later.',
            'status_code': 500
        }), 500


def create_error_response(message: str, status_code: int = 400):
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        status_code: HTTP status code
    
    Returns:
        tuple: (response, status_code)
    """
    return jsonify({
        'success': False,
        'error': message,
        'status_code': status_code
    }), status_code