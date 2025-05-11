"""
Tests for API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "NBA Data Analytics API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "active"

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_get_players():
    """Test players list endpoint."""
    response = client.get("/players/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_player_not_found():
    """Test player detail endpoint with invalid ID."""
    response = client.get("/players/invalid_id")
    assert response.status_code == 404

def test_get_teams():
    """Test teams list endpoint."""
    response = client.get("/teams/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_team_not_found():
    """Test team detail endpoint with invalid ID."""
    response = client.get("/teams/invalid_id")
    assert response.status_code == 404

def test_get_games():
    """Test games list endpoint."""
    response = client.get("/games/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_today_games():
    """Test today's games endpoint."""
    response = client.get("/games/today")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_live_games():
    """Test live games endpoint."""
    response = client.get("/games/live")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_game_not_found():
    """Test game detail endpoint with invalid ID."""
    response = client.get("/games/invalid_id")
    assert response.status_code == 404

def test_invalid_endpoint(client):
    """Test accessing an invalid endpoint."""
    response = client.get("/invalid")
    assert response.status_code == 404 