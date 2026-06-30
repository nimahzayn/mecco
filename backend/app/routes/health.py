"""
Health Check Routes Module

Provides endpoints for monitoring application health and status.
"""

from flask import Blueprint, jsonify, current_app
from datetime import datetime

# Create blueprint
health_bp = Blueprint('health', __name__)


@health_bp.route('/', methods=['GET'])
def root():
    """
    Root endpoint.
    
    Returns:
        Simple message indicating the API is running.
    """
    return jsonify({
        'message': 'College Information Chatbot API',
        'status': 'running',
        'version': current_app.config.get('API_VERSION', '1.0.0')
    }), 200


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    Returns detailed information about the application status.
    Useful for monitoring and deployment platforms.
    
    Response:
        {
            "status": "healthy",
            "version": "v1",
            "environment": "development",
            "timestamp": "2024-01-01T12:00:00Z",
            "services": {
                "chat": "operational",
                "database": "not_configured"
            }
        }
    """
    try:
        # Check service statuses
        services = {
            'chat': 'operational',
            # TODO: Add more service checks when integrated
            # 'database': check_database_status(),
            # 'vector_db': check_vector_db_status(),
            # 'gemini_api': check_gemini_api_status(),
        }
        
        # Overall status
        all_operational = all(status == 'operational' for status in services.values())
        overall_status = 'healthy' if all_operational else 'degraded'
        
        response = {
            'status': overall_status,
            'version': current_app.config.get('API_VERSION', 'v1'),
            'environment': current_app.config.get('FLASK_ENV', 'development'),
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'services': services
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        current_app.logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500


@health_bp.route('/ping', methods=['GET'])
def ping():
    """
    Simple ping endpoint for quick availability checks.
    
    Returns:
        {
            "message": "pong",
            "timestamp": "2024-01-01T12:00:00Z"
        }
    """
    return jsonify({
        'message': 'pong',
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }), 200