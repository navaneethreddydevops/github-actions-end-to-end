"""
Simple Flask web application for demonstrating GitHub Actions workflows.
"""

from flask import Flask, jsonify, request
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)


@app.route('/')
def home():
    """Home endpoint returning a welcome message."""
    return jsonify({
        'message': 'Welcome to GitHub Actions Learning App!',
        'version': '1.0.0',
        'status': 'healthy'
    })


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'github-actions-demo',
        'environment': os.getenv('ENVIRONMENT', 'development')
    })


@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Simple calculation endpoint for testing purposes."""
    try:
        data = request.get_json()
        
        if not data or 'numbers' not in data:
            return jsonify({'error': 'Missing numbers array'}), 400
        
        numbers = data['numbers']
        operation = data.get('operation', 'sum')
        
        if not isinstance(numbers, list) or not numbers:
            return jsonify({'error': 'Numbers must be a non-empty array'}), 400
        
        # Validate all numbers are numeric
        for num in numbers:
            if not isinstance(num, (int, float)):
                return jsonify({'error': 'All elements must be numbers'}), 400
        
        # Perform calculations
        result = {
            'numbers': numbers,
            'operation': operation
        }
        
        if operation == 'sum':
            result['result'] = sum(numbers)
        elif operation == 'product':
            result['result'] = 1
            for num in numbers:
                result['result'] *= num
        elif operation == 'average':
            result['result'] = sum(numbers) / len(numbers)
        else:
            return jsonify({'error': 'Unsupported operation. Use: sum, product, average'}), 400
        
        logger.info(f"Calculated {operation} for {numbers}: {result['result']}")
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in calculate endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/info')
def app_info():
    """Return application information."""
    return jsonify({
        'name': 'GitHub Actions Demo App',
        'description': 'A simple Flask app for learning GitHub Actions',
        'endpoints': [
            {'path': '/', 'method': 'GET', 'description': 'Welcome message'},
            {'path': '/health', 'method': 'GET', 'description': 'Health check'},
            {'path': '/api/calculate', 'method': 'POST', 'description': 'Perform calculations'},
            {'path': '/api/info', 'method': 'GET', 'description': 'App information'}
        ],
        'environment_variables': {
            'PORT': os.getenv('PORT', '5000'),
            'ENVIRONMENT': os.getenv('ENVIRONMENT', 'development'),
            'DEBUG': os.getenv('DEBUG', 'False')
        }
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Get configuration from environment variables
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting GitHub Actions Demo App on port {port}")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)