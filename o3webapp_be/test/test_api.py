import unittest
import json
from flask import request

from o3webapp_be.backend.back_end import app

class TestApi(unittest.TestCase):

    def setUp(self):
        self.headers = {'Accept': 'application/json'}

    def test_plot_returns_list(self):
        """Test that /plot returns correct list of possible plots
        """
        with app.test_client() as client:
           response = client.post('/plot', 
                                  headers=self.headers).json
           expected_json = ["tco3_zm","vmro3_zm","tco3_return"]
           self.assertEqual(response, expected_json)

    def test_model_list_get_returns_200(self):
        """Test if GET method of the endpoint 
           /model_list/<ptype> returns 200 (success)
        """
        with app.test_client() as client:
            response = client.get('/model_list/tco3_zm')
            assert response._status_code == 200


if __name__ == '__main__':
    unittest.main()

