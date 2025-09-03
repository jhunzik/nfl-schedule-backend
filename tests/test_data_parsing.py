import unittest
import json
from datetime import datetime, timezone

# This is a hack to get the src folder in the path
# TODO: fix this with a proper setup.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.espn_client import _parse_espn_response
from src.models import Game, Location


class TestDataParsing(unittest.TestCase):
    def setUp(self):
        with open("tests/sample_espn_response.json") as f:
            self.sample_response = json.load(f)

    def test_parse_espn_response_success(self):
        """
        Test that _parse_espn_response correctly parses a sample ESPN response.
        """
        games = _parse_espn_response(self.sample_response)
        self.assertEqual(len(games), 1)
        game = games[0]
        self.assertIsInstance(game, Game)
        self.assertEqual(game.id, "401772510")
        self.assertEqual(game.homeTeam, "Philadelphia Eagles")
        self.assertEqual(game.awayTeam, "Dallas Cowboys")
        self.assertEqual(
            game.startTime, datetime(2025, 9, 5, 0, 20, tzinfo=timezone.utc)
        )
        self.assertIsInstance(game.location, Location)
        self.assertEqual(game.location.venue, "Lincoln Financial Field")
        self.assertEqual(game.location.city, "Philadelphia")
        self.assertEqual(game.type, "regular-season")

    def test_parse_espn_response_empty(self):
        """
        Test that _parse_espn_response returns an empty list for an empty response.
        """
        games = _parse_espn_response({})
        self.assertEqual(len(games), 0)

    def test_parse_espn_response_no_events(self):
        """
        Test that _parse_espn_response returns an empty list for a response with no events.
        """
        response = {"leagues": [], "events": []}
        games = _parse_espn_response(response)
        self.assertEqual(len(games), 0)

    def test_parse_espn_response_missing_key(self):
        """
        Test that _parse_espn_response handles a response with a missing key.
        """
        response = {"events": [{}]}
        games = _parse_espn_response(response)
        self.assertEqual(len(games), 0)


if __name__ == "__main__":
    unittest.main()
