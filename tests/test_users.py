import unittest 
from base import BaseTestCase

class TestUser(BaseTestCase):

    def test_login(self):
        response = self.client.get("/login/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get("/register/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get("/logout/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)