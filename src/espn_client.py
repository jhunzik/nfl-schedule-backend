"""
ESPN API client for fetching NFL game data.
"""

import urllib.request
import json
import logging
from datetime import datetime
import zoneinfo

from src.models import Game, Location
from src.config import ESPN_API_URL


def _parse_espn_response(espn_data):
    """
    Parses the ESPN API response and returns a list of Game objects.
    """
    games = []
    if not espn_data or "events" not in espn_data:
        return games

    for event in espn_data.get("events", []):
        try:
            competition = event["competitions"][0]
            home_team = next(
                c for c in competition["competitors"] if c["homeAway"] == "home"
            )
            away_team = next(
                c for c in competition["competitors"] if c["homeAway"] == "away"
            )
            venue = competition.get("venue", {})
            game_id = event["id"]
            start_time_str = event["date"]
            season_type = event["season"]["type"]

            # Timezone conversion
            start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
            start_time_utc = start_time.astimezone(zoneinfo.ZoneInfo("UTC"))

            # Season type mapping
            season_type_map = {
                1: "pre-season",
                2: "regular-season",
                3: "post-season",
                4: "superbowl",
            }
            game_type = season_type_map.get(season_type, "unknown")

            game = Game(
                id=game_id,
                homeTeam=home_team["team"]["displayName"],
                awayTeam=away_team["team"]["displayName"],
                startTime=start_time_utc,
                location=Location(
                    venue=venue.get("fullName", "Unknown"),
                    city=venue.get("address", {}).get("city", "Unknown"),
                ),
                type=game_type,
            )
            games.append(game)
        except (KeyError, IndexError) as e:
            logging.warning(f"Could not parse game event: {event}. Missing key: {e}")

    return games


def fetch_scoreboard_data():
    """
    Fetches and parses scoreboard data from the ESPN API.
    """
    try:
        with urllib.request.urlopen(ESPN_API_URL, timeout=30) as response:
            data = json.loads(response.read())
            return _parse_espn_response(data)
    except (urllib.error.URLError, TimeoutError) as e:
        # Handle network errors or timeouts
        logging.error(f"Error fetching data from ESPN API: {e}")
        return []
    except json.JSONDecodeError as e:
        # Handle invalid JSON responses
        logging.error(f"Error decoding JSON from ESPN API: {e}")
        return []
