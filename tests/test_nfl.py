import unittest 
from base import BaseTestCase 

# Create your tests here.
class TestNflCase(BaseTestCase):
    

    def test_nfl(self):
        response = self.client.get("/nfl/")
        self.assertEqual(response.status_code, 200)

    def test_nfl_home(self):
        response = self.client.get("/nfl/home/")
        self.assertEqual(response.status_code, 200)

    def test_nfl_public_board(self):
        response = self.client.get("/nfl/board/")
        self.assertEqual(response.status_code, 200)

    def test_nfl_picked_bet(self):
        response = self.client.get("/nfl/confirm/")
        self.assertEqual(response.status_code, 200)

    # def test_nfl_picked_bet(self):
    #     response = self.client.get("/nfl/board/confirm/11111111")
    #     self.assertEqual(response.status_code, 200)

    def test_nfl_create_bet(self):
        response = self.client.get("/nfl/create/")
        self.assertEqual(response.status_code, 200)