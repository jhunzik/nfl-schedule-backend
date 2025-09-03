import unittest
from unittest.mock import patch, MagicMock
import urllib.error
import logging

# This is a hack to get the src folder in the path
# TODO: fix this with a proper setup.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.espn_client import fetch_scoreboard_data
from src.models import Game

class TestEspnClient(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    @patch('urllib.request.urlopen')
    def test_fetch_scoreboard_data_success(self, mock_urlopen):
        """
        Test that fetch_scoreboard_data returns a list of Game objects on a successful API call.
        """
        # Create a mock response
        mock_response = MagicMock()
        with open("tests/sample_espn_response.json") as f:
            sample_response_json = f.read()
        mock_response.read.return_value = sample_response_json.encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Call the function
        games = fetch_scoreboard_data()

        # Assert that the function returns the correct data
        self.assertIsInstance(games, list)
        self.assertEqual(len(games), 1)
        self.assertIsInstance(games[0], Game)


    @patch('urllib.request.urlopen')
    def test_fetch_scoreboard_data_network_error(self, mock_urlopen):
        """
        Test that fetch_scoreboard_data returns an empty list on a network error.
        """
        mock_urlopen.side_effect = urllib.error.URLError("testing network error")

        data = fetch_scoreboard_data()
        self.assertEqual(data, [])

    @patch('urllib.request.urlopen')
    def test_fetch_scoreboard_data_json_error(self, mock_urlopen):
        """
        Test that fetch_scoreboard_data returns an empty list on a JSON decoding error.
        """
        mock_response = MagicMock()
        mock_response.read.return_value = b"not json"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        data = fetch_scoreboard_data()
        self.assertEqual(data, [])

    @patch('urllib.request.urlopen')
    def test_fetch_scoreboard_data_timeout(self, mock_urlopen):
        """
        Test that fetch_scoreboard_data returns an empty list on a timeout.
        """
        mock_urlopen.side_effect = TimeoutError("testing timeout")

        data = fetch_scoreboard_data()
        self.assertEqual(data, [])

if __name__ == '__main__':
    unittest.main()
