"""test module."""
import unittest
from flask import request
import requests
import json

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
        self.assertEqual(response.text, '"valid data"\n')
    
    
    def test_no_valid_data(self):
        response = requests.get(self.URL)
        self.assertNotEqual(response.status_code, self.VALID_STATUS_CODE)
        
