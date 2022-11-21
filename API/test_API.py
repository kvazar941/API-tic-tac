"""test module."""
import unittest
from flask import request
import requests
import json

from fixtures import GAME_SITUATION_WIN_CROSS

class TestAPI(unittest.TestCase):
    URL = 'http://127.0.0.1:5000/tic-tac'
    TEST_DATA = {'one': 1, 'two': 2}
    VALID_STATUS_CODE = 200


    def test_server_availability(self):
        response = requests.get(self.URL, json=self.TEST_DATA)
        self.assertEqual(response.status_code, self.VALID_STATUS_CODE)
        
    
    def test_valid_data(self):
        response = requests.get(self.URL, json=self.TEST_DATA)
        self.assertEqual(response.status_code, self.VALID_STATUS_CODE)
    
    
    def test_no_valid_data(self):
        response = requests.get(self.URL)
        self.assertNotEqual(response.status_code, self.VALID_STATUS_CODE)
    
    def test_win_cross(self):
        response = requests.get(self.URL, json=GAME_SITUATION_WIN_CROSS)
        self.assertEqual(response.status_code, self.VALID_STATUS_CODE)
        self.assertEqual(response.text[:-1], '"Victory cross!"')
        
