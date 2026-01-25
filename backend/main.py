"""
AI-Patient-Record-Intelligence - Flask Backend
Doctor-first, safety-critical patient record system

Application entry point
"""

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'development'))

# Enable CORS
CORS(app, 
     origins=os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(','),
     supports_credentials=True)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'AI Patient Record Intelligence API is running'}, 200

@app.route('/', methods=['GET'])
def index():
    """API info endpoint"""
    return {
        'name': 'AI Patient Record Intelligence API',
        'version': '1.0.0',
        'status': 'running',
        'environment': os.getenv('FLASK_ENV', 'development')
    }, 200

if __name__ == '__main__':
    debug = os.getenv('FLASK_ENV') == 'development'
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug)

