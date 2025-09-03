import unittest
from unittest.mock import patch
from starlette.testclient import TestClient
from datetime import datetime, timezone

# This is a hack to get the src folder in the path
# TODO: fix this with a proper setup.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.app import app
from src.models import Game, Location

class TestApi(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch('src.app._get_today')
    @patch('src.app.fetch_scoreboard_data')
    def test_games_today_success(self, mock_fetch_scoreboard_data, mock_get_today):
        """
        Test that /games/today returns today's games on a successful API call.
        """
        # Configure the mock to control the current date
        mock_get_today.return_value = datetime(2025, 9, 2, 12, 0, 0, tzinfo=timezone.utc).date()

        # Create a mock response with a game for today
        mock_games = [
            Game(
                id="123",
                homeTeam="Team A",
                awayTeam="Team B",
                startTime=datetime(2025, 9, 2, 18, 0, 0, tzinfo=timezone.utc),
                location=Location(venue="Venue A", city="City A"),
                type="regular-season"
            )
        ]
        mock_fetch_scoreboard_data.return_value = mock_games

        # Call the endpoint
        response = self.client.get("/games/today")

        # Assert that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["games"]), 1)
        self.assertEqual(response.json()["games"][0]["id"], "123")

    @patch('src.app.fetch_scoreboard_data')
    def test_games_today_no_games(self, mock_fetch_scoreboard_data):
        """
        Test that /games/today returns an empty list when there are no games today.
        """
        # Create a mock response
        mock_fetch_scoreboard_data.return_value = []

        # Call the endpoint
        response = self.client.get("/games/today")

        # Assert that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "No games scheduled for today.")

    @patch('src.app.fetch_scoreboard_data')
    def test_games_today_games_not_today(self, mock_fetch_scoreboard_data):
        """
        Test that /games/today returns an empty list when there are games, but not for today.
        """
        # Create a mock response
        mock_games = [
            Game(
                id="123",
                homeTeam="Team A",
                awayTeam="Team B",
                startTime=datetime(2025, 1, 1, 1, 1, 1, tzinfo=timezone.utc),
                location=Location(venue="Venue A", city="City A"),
                type="regular-season"
            )
        ]
        mock_fetch_scoreboard_data.return_value = mock_games

        # Call the endpoint
        response = self.client.get("/games/today")

        # Assert that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "No games scheduled for today.")

if __name__ == '__main__':
    unittest.main()
