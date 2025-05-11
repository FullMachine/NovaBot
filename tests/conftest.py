"""
Pytest configuration file.
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture
def test_db():
    """Configure test database."""
    # Here you would typically set up a test database
    # For now, we'll just use environment variables
    os.environ["DB_NAME"] = "nova_sports_test"
    yield
    # Clean up after tests if needed 