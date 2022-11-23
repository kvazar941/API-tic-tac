"""test API module."""
import unittest

import requests
from fixtures import GAME_SITUATION_WIN_CROSS, GAME_START_SITUATION


class TestAPI(unittest.TestCase):
    url = 'http://127.0.0.1:5000'
    valid_status_code = 200

    def test_server_availability(self):
        response = requests.get(self.url, json=GAME_START_SITUATION)
        self.assertEqual(response.status_code, self.valid_status_code)

    def test_valid_data(self):
        response = requests.get(self.url, json=GAME_START_SITUATION)
        self.assertEqual(response.status_code, self.valid_status_code)

    def test_no_valid_data(self):
        response = requests.get(self.url)
        self.assertNotEqual(response.status_code, self.valid_status_code)

    def test_win_cross(self):
        response = requests.get(self.url, json=GAME_SITUATION_WIN_CROSS)
        self.assertEqual(response.status_code, self.valid_status_code)
        self.assertEqual(response.text[:-1], '"Victory cross!"')
