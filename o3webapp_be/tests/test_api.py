import unittest
import json
from flask import request

from o3webapp_be.back_end import app

class TestApi(unittest.TestCase):

    def setUp(self):
        self.headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json'}

    def test_model_list_get_returns_302(self):
        """Test if GET method of the endpoint 
           /model_list/<ptype> returns 302 (look at another URL)
        """
        with app.test_client() as client:
            response = client.get('/model_list/tco3_zm')
            # 302 = Tells the client to look at (browse to) another URL
            assert response._status_code == 302
