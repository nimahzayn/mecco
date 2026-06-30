"""
Configuration Module

Manages different configurations for development, testing, and production.
All configuration values should be loaded from environment variables.
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class with default values."""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # Server Configuration
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # API Configuration
    API_VERSION = os.getenv('API_VERSION', 'v1')
    API_PREFIX = '/api'
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization']
    
    # Chat Configuration
    MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', 500))
    MOCK_RESPONSE_DELAY = float(os.getenv('MOCK_RESPONSE_DELAY', 1.0))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Future Integration (Placeholders for teammates)
    # These will be used by Member 1 and Member 2
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', None)
    CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', './data/chroma')
    CHROMA_COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME', 'college_docs')
    
    # Rate Limiting (optional, for future implementation)
    RATELIMIT_ENABLED = False


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # In production, these must be set
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Production security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """
    Get configuration based on FLASK_ENV environment variable.
    
    Returns:
        Config: Configuration object
    """
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)