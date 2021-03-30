import unittest

import requests

from o3webapp_be.back_end import app



class PtypeTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.headers = {'Accept': 'application/json'}
        app.config.update(
            TESTING=True
        )

    def test_model_info_status_code(self):
        resp = self.client.get('/models/CCMI-1_ACCESS-refC2')

        self.assertEqual(200, resp.status_code)
