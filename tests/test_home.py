import unittest 
from base import BaseTestCase 

class TestHome(BaseTestCase):

    def test_home(self):
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        response = self.client.get("/profile/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)



