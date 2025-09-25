"""
Unit tests for the GitHub Actions demo application.
"""

import pytest
import json
import sys
import os

# Add the src directory to the path so we can import the app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """Test the home endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'message' in data
    assert 'version' in data
    assert 'status' in data
    assert data['status'] == 'healthy'


def test_health_check_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'github-actions-demo'
    assert 'environment' in data


def test_app_info_endpoint(client):
    """Test the app info endpoint."""
    response = client.get('/api/info')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['name'] == 'GitHub Actions Demo App'
    assert 'endpoints' in data
    assert 'environment_variables' in data
    assert len(data['endpoints']) >= 4


def test_calculate_sum(client):
    """Test the calculate endpoint with sum operation."""
    payload = {
        'numbers': [1, 2, 3, 4, 5],
        'operation': 'sum'
    }
    
    response = client.post('/api/calculate', 
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['result'] == 15
    assert data['operation'] == 'sum'
    assert data['numbers'] == [1, 2, 3, 4, 5]


def test_calculate_product(client):
    """Test the calculate endpoint with product operation."""
    payload = {
        'numbers': [2, 3, 4],
        'operation': 'product'
    }
    
    response = client.post('/api/calculate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['result'] == 24
    assert data['operation'] == 'product'


def test_calculate_average(client):
    """Test the calculate endpoint with average operation."""
    payload = {
        'numbers': [10, 20, 30],
        'operation': 'average'
    }
    
    response = client.post('/api/calculate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['result'] == 20.0
    assert data['operation'] == 'average'


def test_calculate_default_sum(client):
    """Test the calculate endpoint with default sum operation."""
    payload = {
        'numbers': [1, 2, 3]
    }
    
    response = client.post('/api/calculate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['result'] == 6
    assert data['operation'] == 'sum'


def test_calculate_missing_numbers(client):
    """Test the calculate endpoint with missing numbers."""
    payload = {'operation': 'sum'}
    
    response = client.post('/api/calculate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Missing numbers array' in data['error']


def test_calculate_empty_numbers(client):
    """Test the calculate endpoint with empty numbers array."""
    payload = {
        'numbers': [],
        'operation': 'sum'
    }
    
    response = client.post('/api/calculate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_calculate_invalid_numbers(client):
    """Test the calculate endpoint with invalid numbers."""
    payload = {
        'numbers': [1, 'invalid', 3],
        'operation': 'sum'
    }
    
    response = client.post('/api/calculate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'must be numbers' in data['error']


def test_calculate_unsupported_operation(client):
    """Test the calculate endpoint with unsupported operation."""
    payload = {
        'numbers': [1, 2, 3],
        'operation': 'unsupported'
    }
    
    response = client.post('/api/calculate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Unsupported operation' in data['error']


def test_404_error(client):
    """Test 404 error handling."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data
    assert 'not found' in data['error'].lower()


def test_calculate_with_floats(client):
    """Test the calculate endpoint with float numbers."""
    payload = {
        'numbers': [1.5, 2.5, 3.0],
        'operation': 'sum'
    }
    
    response = client.post('/api/calculate',
                          data=json.dumps(payload),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['result'] == 7.0