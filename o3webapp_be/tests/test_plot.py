import unittest

from o3webapp_be.back_end import app

import requests


class PlotterTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config.update(
            TESTING=True)
        self.headers = {'Accept': 'application/json'}
        self.request_json = {"pType": "tco3_zm", "models": [
            {"model": "CCMI-1_ACCESS-refC2", "style": {"color": "#000000", "highlighted": "0"}},
            {"model": "CCMI-1_CCCma-CMAM-refC2", "style": {"color": "#ff0000", "highlighted": "0"}},
            {"model": "CCMI-1_CHASER-MIROC-ESM-refC2", "style": {"color": "#ff0000", "highlighted": "0"}},
            {"model": "SBUV_GSFC_merged-SAT-ozone", "style": {"color": "#ff0000", "highlighted": "0"}}],
                             "begin": "1970", "end": "2100", "month": ["1", "2", "3"], "lat_min": "-90", "lat_max": "0",
                             "output": "json"}

    def test_tco3zm_status_code(self):
        resp = self.client.post('plot/tco3_zm', headers=self.headers, json=self.request_json)

        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
