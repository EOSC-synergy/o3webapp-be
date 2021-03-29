import unittest

from o3webapp_be.backend.back_end import app

class LoginTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config.update(
            TESTING=True)

    def test_login_status_code(self):
        resp = self.client