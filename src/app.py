import logging
import datetime
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import json

from src.espn_client import fetch_scoreboard_data


class CustomJSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            default=lambda o: o.isoformat()
            if isinstance(o, datetime.datetime)
            else o.__dict__,
        ).encode("utf-8")


async def health_check(request):
    """
    Health check endpoint.
    """
    logging.info("Health check endpoint was called.")
    return JSONResponse({"status": "ok"})


def _get_today() -> datetime.date:
    return datetime.datetime.utcnow().date()


async def games_today(request):
    """
    Returns today's games.
    """
    today = _get_today()
    all_games = fetch_scoreboard_data()
    today_games = []
    for game in all_games:
        if game.startTime.date() == today:
            today_games.append(game)

    if not today_games:
        logging.warning("No games scheduled for today.")
        return CustomJSONResponse({"message": "No games scheduled for today."})

    return CustomJSONResponse({"games": today_games})


routes = [
    Route("/health", health_check),
    Route("/games/today", games_today),
]

app = Starlette(debug=True, routes=routes)
