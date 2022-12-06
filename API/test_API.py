"""test API module."""
import unittest

import requests
from fixtures import GAME_SITUATION_WIN_CROSS, GAME_START_SITUATION, GAME_SITUATION_NEW_STEP


class TestAPI(unittest.TestCase):
    url_new_game = 'http://127.0.0.1:5000/new-game'
    url_new_step = 'http://127.0.0.1:5000/new-step'
    valid_status_code = 200

    def test_server_availability(self):
        response = requests.post(
            self.url_new_game,
            json=GAME_START_SITUATION,
        )
        self.assertEqual(response.status_code, self.valid_status_code)

    def test_valid_data(self):
        response = requests.post(
            self.url_new_game,
            json=GAME_START_SITUATION,
        )
        self.assertEqual(response.status_code, self.valid_status_code)

    def test_no_valid_data(self):
        response = requests.post(self.url_new_game)
        self.assertNotEqual(response.status_code, self.valid_status_code)

    def test_win_cross(self):
        response = requests.post(
            self.url_new_step,
            json=GAME_SITUATION_WIN_CROSS,
        )
        self.assertEqual(response.status_code, self.valid_status_code)
        self.assertEqual(response.text, 'Victory cross!')

    def test_new_step(self):
        response = requests.post(
            self.url_new_step,
            json=GAME_SITUATION_NEW_STEP,
        )
        self.assertEqual(response.status_code, self.valid_status_code)
        #self.assertEqual(response.text, '')
