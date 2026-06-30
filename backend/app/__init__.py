"""
Flask Application Factory

Creates and configures the Flask application instance.
Uses the application factory pattern for better testing and scalability.
"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from app.config import get_config
from app.utils.logger import setup_logger
from app.utils.errors import register_error_handlers


def create_app():
    """
    Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application instance
    """
    
    # Load environment variables
    load_dotenv()
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    config = get_config()
    app.config.from_object(config)
    
    # Setup logging
    app.logger = setup_logger(
        __name__,
        level=app.config.get('LOG_LEVEL', 'INFO'),
        log_format=app.config.get('LOG_FORMAT')
    )
    
    app.logger.info("Starting College Information Chatbot API")
    app.logger.info(f"Environment: {app.config.get('FLASK_ENV', 'development')}")
    
    # Configure CORS
    CORS(
        app,
        origins=app.config.get('CORS_ORIGINS'),
        methods=app.config.get('CORS_METHODS'),
        allow_headers=app.config.get('CORS_ALLOW_HEADERS'),
        supports_credentials=True
    )
    app.logger.info(f"CORS enabled for origins: {app.config.get('CORS_ORIGINS')}")
    
    # Register error handlers
    register_error_handlers(app)
    app.logger.info("Error handlers registered")
    
    # Register blueprints
    from app.routes import chat_bp, health_bp
    
    # Health routes (no prefix)
    app.register_blueprint(health_bp)
    
    # API routes (with /api prefix)
    api_prefix = app.config.get('API_PREFIX', '/api')
    app.register_blueprint(chat_bp, url_prefix=api_prefix)
    
    app.logger.info(f"Blueprints registered with prefix: {api_prefix}")
    
    # Log all registered routes
    app.logger.info("Registered routes:")
    for rule in app.url_map.iter_rules():
        app.logger.info(f"  {rule.rule} [{', '.join(rule.methods - {'HEAD', 'OPTIONS'})}]")
    
    app.logger.info("Application initialization complete")
    
    return app