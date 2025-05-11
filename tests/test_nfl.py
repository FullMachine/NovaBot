"""
Tests for NFL endpoints.
"""
import pytest
from fastapi.testclient import TestClient

def test_get_player_stats(client):
    """Test getting player statistics."""
    response = client.get("/api/v1/nfl/players/patrick-mahomes")
    assert response.status_code == 404  # Will be 404 until we implement data collection

def test_get_team_stats(client):
    """Test getting team statistics."""
    response = client.get("/api/v1/nfl/teams/KC")
    assert response.status_code == 404  # Will be 404 until we implement data collection

def test_get_game_stats(client):
    """Test getting game statistics."""
    response = client.get("/api/v1/nfl/games/2023_KC_SF")
    assert response.status_code == 404  # Will be 404 until we implement data collection

def test_get_standings(client):
    """Test getting standings."""
    response = client.get("/api/v1/nfl/standings")
    assert response.status_code == 404  # Will be 404 until we implement data collection

def test_search_players(client):
    """Test searching for players."""
    response = client.get("/api/v1/nfl/players/search/Mahomes")
    assert response.status_code == 404  # Will be 404 until we implement search

def test_search_teams(client):
    """Test searching for teams."""
    response = client.get("/api/v1/nfl/teams/search/Chiefs")
    assert response.status_code == 404  # Will be 404 until we implement search

def test_player_not_found():
    """Test getting non-existent player."""
    response = client.get("/api/v1/nfl/players/nonexistent-player")
    assert response.status_code == 404

def test_team_not_found():
    """Test getting non-existent team."""
    response = client.get("/api/v1/nfl/teams/nonexistent-team")
    assert response.status_code == 404

def test_game_not_found():
    """Test getting non-existent game."""
    response = client.get("/api/v1/nfl/games/nonexistent-game")
    assert response.status_code == 404 