# Nova Sports Data API Documentation

## Overview
The Nova Sports Data API provides comprehensive sports data across multiple leagues and sports. This API is designed to be fast, reliable, and easy to use.

## Authentication
Currently, the API uses internal authentication as we're collecting and serving our own data.

## Base URL
```
http://localhost:8000/api/v1
```

## Available Endpoints

### NFL
- `GET /nfl/players/{player_id}` - Get player statistics
- `GET /nfl/teams/{team_id}` - Get team statistics
- `GET /nfl/games/{game_id}` - Get game statistics
- `GET /nfl/standings` - Get current standings
- `GET /nfl/players/search/{name}` - Search players by name
- `GET /nfl/teams/search/{name}` - Search teams by name

### NBA
- `GET /nba/players/{player_id}` - Get player statistics
- `GET /nba/teams/{team_id}` - Get team statistics
- `GET /nba/games/{game_id}` - Get game statistics
- `GET /nba/standings` - Get current standings
- `GET /nba/players/search/{name}` - Search players by name
- `GET /nba/teams/search/{name}` - Search teams by name

### Soccer
- `GET /soccer/{league}/teams/{team_id}` - Get team statistics
- `GET /soccer/{league}/players/{player_id}` - Get player statistics
- `GET /soccer/{league}/matches/{match_id}` - Get match statistics
- `GET /soccer/{league}/standings` - Get league standings

### Baseball
- `GET /baseball/{league}/teams/{team_id}` - Get team statistics
- `GET /baseball/{league}/players/{player_id}` - Get player statistics
- `GET /baseball/{league}/games/{game_id}` - Get game statistics
- `GET /baseball/{league}/standings` - Get league standings

### Racing
- `GET /racing/{series}/drivers/{driver_id}` - Get driver statistics
- `GET /racing/{series}/teams/{team_id}` - Get team statistics
- `GET /racing/{series}/races/{race_id}` - Get race results
- `GET /racing/{series}/standings` - Get championship standings

### Esports
- `GET /esports/{game}/players/{player_id}` - Get player statistics
- `GET /esports/{game}/teams/{team_id}` - Get team statistics
- `GET /esports/{game}/matches/{match_id}` - Get match statistics
- `GET /esports/{game}/tournaments` - Get tournament information

### Tennis
- `GET /tennis/{tour}/players/{player_id}` - Get player statistics
- `GET /tennis/{tour}/tournaments/{tournament_id}` - Get tournament information
- `GET /tennis/{tour}/matches/{match_id}` - Get match statistics
- `GET /tennis/{tour}/rankings` - Get current rankings

## Response Formats
All responses are returned in JSON format. Successful responses will have a 200 status code.

### Error Codes
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error

## Rate Limiting
Each endpoint has specific rate limits defined in the configuration. These are enforced to ensure API stability.

## Data Freshness
- Player/Team statistics: Updated daily
- Game/Match results: Updated in near real-time
- Standings: Updated after each game/match
- Rankings: Updated weekly

## Support
For API support or questions, please contact the development team. 