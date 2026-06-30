"""Routes package."""

from .chat import chat_bp
from .health import health_bp

__all__ = ['chat_bp', 'health_bp']