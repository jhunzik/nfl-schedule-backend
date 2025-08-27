# NFL Game Schedule Backend - Product Requirements Document

## Overview
Backend service that fetches NFL game data from ESPN's public API and transforms it into structured game schedule information. Primary use case is providing data for an e-ink display showing today's games and weekly schedules.

## Functional Requirements

### Data Source
- ESPN API endpoint: `https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard`
- Real-time game data fetching
- Handle API rate limiting and error responses

### Data Model
Each game item must include:
- **Teams**: Home and away team names/identifiers
- **Start Time**: UTC timestamp format
- **Location**: Venue name and city
- **Type**: Game classification (pre-season, regular-season, post-season, superbowl)

### API Endpoints
- `GET /games/today` - Today's scheduled games
- `GET /games/week` - Current week's games
- `GET /games/{date}` - Games for specific date (YYYY-MM-DD)
- `GET /games/week/{week}` - Games for specific NFL week (optional)

### Data Processing
- Convert ESPN timestamps to UTC
- Map ESPN season types to our classifications:
  - Pre-season (ESPN type 1)
  - Regular season (ESPN type 2) 
  - Post-season (ESPN type 3)
  - Super Bowl (ESPN type 4)
- Extract venue information from ESPN venue data
- Normalize team names/abbreviations

### Response Format
```json
{
  "games": [
    {
      "id": "string",
      "homeTeam": "string",
      "awayTeam": "string", 
      "startTime": "2024-01-01T18:00:00Z",
      "location": {
        "venue": "string",
        "city": "string"
      },
      "type": "regular-season"
    }
  ]
}
```

## Non-Functional Requirements

### Performance
- Low-frequency usage (max 1 request/day)
- API response time < 2s (acceptable for e-ink refresh)
- Support minimal concurrent load
- Cache ESPN data for 24-hour intervals

### Reliability
- 99% uptime (sufficient for daily e-ink updates)
- Graceful ESPN API failure handling
- Simple retry logic
- Data staleness acceptable up to 24 hours

### Data Quality
- Validate all required fields present
- Handle missing/null ESPN data gracefully
- Log data inconsistencies

## Technical Requirements

### Technology Stack
- **Framework**: Python 3 with Starlette
- **HTTP Client**: `urllib` (standard library) or `requests` if needed
- **JSON Processing**: `json` (standard library)
- **Date/Time**: `datetime` and `zoneinfo` (standard library)
- **Caching**: In-memory with `dict` or `sqlite3` for persistence
- **Configuration**: `os.environ` (standard library)
- **Logging**: `logging` (standard library)
- **Testing**: `unittest` (standard library)

### Third-party Dependencies (only if standard library insufficient)
- `requests` - if `urllib` proves inadequate for ESPN API calls
- `uvicorn` - ASGI server for Starlette

### Infrastructure
- Single instance deployment sufficient
- Basic health check endpoint
- Simple logging
- Environment-based configuration

### Security
- API rate limiting
- Input validation
- CORS configuration
- No authentication required (public data)

## Implementation Notes

### ESPN API Considerations
- Check `competitions` array for game data
- Handle timezone conversion from venue timezone
- Season type mapping from `season.type`
- Extract team data from `competitions[].competitors`

### Error Handling
- ESPN API unavailable
- Malformed ESPN responses
- Network timeouts
- Invalid date parameters

### Monitoring
- ESPN API response times
- Cache hit rates
- Error rates by endpoint
- Data freshness metrics
