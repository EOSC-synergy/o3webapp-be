import unittest

import coverage

from o3webapp_be.back_end import app

class DownloadTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config.update(
            TESTING=True)
        self.request_json = {"pType": "tco3_zm",
                             "models": [{"model": "CCMI-1_ACCESS-refC2",
                                         "style": {
                                             "color": "",
                                             "highlighted": ""
                                         }
                                         },
                                        {"model": "CCMI-1_CCCma-CMAM-refC2",
                                         "style": {
                                             "color": "",
                                             "highlighted": ""
                                         }
                                         }
                                        ],
                             "begin": "1959",
                             "end": "2100",
                             "month": ["7", "9"],
                             "lat_min": "-10",
                             "lat_max": "10",
                             "output": "json"}

    def test_pdf_status_code(self):
        resp = self.client.post('/download/pdf', json=self.request_json)

        self.assertEqual(resp.status_code, 200)

    def test_pdf_exist(self):
        resp = self.client.post('/download/pdf', json=self.request_json)

        self.assertIsNotNone(resp.data)

    # TODO: test if downloaded pdf file is ok
    def test_pdf(self):
        pass

if __name__ == '__main__':
    unittest.main()
