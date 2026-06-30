"""
Application Entry Point

Runs the Flask development server.
For production, use gunicorn: gunicorn run:app
"""

import os
from app import create_app

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║   College Information Chatbot - Backend API              ║
    ║                                                           ║
    ║   Environment: {os.getenv('FLASK_ENV', 'development').ljust(44)}║
    ║   Server:      http://{host}:{port}{' ' * (35 - len(host) - len(str(port)))}║
    ║   Health:      http://{host}:{port}/health{' ' * (28 - len(host) - len(str(port)))}║
    ║   API Docs:    http://{host}:{port}/api/chat{' ' * (26 - len(host) - len(str(port)))}║
    ║                                                           ║
    ║   Ready to integrate with React frontend!                ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug
    )