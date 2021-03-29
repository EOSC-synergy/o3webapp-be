import unittest

from o3webapp_be.backend.back_end import app



class PtypeTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.headers = {'Accept': 'application/json'}
        app.config.update(
            TESTING=True
        )

    def tearDown(self):
        pass

    def test_app_exist(self):
        self.assertIsNotNone(app)

    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

    def test_ptype(self):
        resp = self.client.post('/plot', headers=self.headers).json

        expected_json = ["tco3_zm", "vmro3_zm", "tco3_return"]

        self.assertEqual(expected_json, resp)

if __name__ == '__main__':
    unittest.main()

