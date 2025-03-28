"""
Common fixtures for tests.
"""

import pytest
import json
from main import app
from models import db


@pytest.fixture
def client():
    """Create a test client for the app."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            print(124)
            yield client
            # db.session.remove()
            print("hello")
            db.drop_all()

def check_response(response, expected_status=None, expected_data=None, allow_empty=False):
    """Enhanced helper function to check API responses.
    
    Args:
        response: The response object from the API call
        expected_status: Single status code or list of acceptable status codes
        expected_data: Dictionary of expected data in the response
        allow_empty: Whether to allow empty responses
    
    Returns:
        The parsed JSON data from the response
    
    Raises:
        AssertionError: If the response doesn't match expected values
    """
    # Check status code
    if expected_status is not None:
        if isinstance(expected_status, list):
            assert response.status_code in expected_status, \
                f"Expected status in {expected_status}, got {response.status_code}: {response.data}"
        else:
            assert response.status_code == expected_status, \
                f"Expected status {expected_status}, got {response.status_code}: {response.data}"
    
    # Handle empty responses
    if not response.data and allow_empty:
        return {}
    
    # Parse and validate JSON
    try:
        data = json.loads(response.data)
        
        if expected_data:
            for key, value in expected_data.items():
                if key not in data:
                    matching_keys = [k for k in data.keys() if k.lower() == key.lower()]
                    if matching_keys:
                        # Found case-insensitive match
                        actual_key = matching_keys[0]
                        if value is not None:
                            assert data[actual_key] == value, \
                                f"Expected '{actual_key}' to be {value}, got {data[actual_key]}"
                    else:
                        assert False, f"Expected key '{key}' not found in response: {data}"
                elif value is not None:
                    assert data[key] == value, \
                        f"Expected '{key}' to be {value}, got {data[key]}"
        
        return data
    except json.JSONDecodeError:
        # For non-JSON responses, return the raw data
        return response.data

@pytest.fixture
def api_checker():
    """Fixture to provide the check_response function."""
    return check_response
