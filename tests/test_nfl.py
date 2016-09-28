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

    def test_nfl_schedule(self):
        response = self.client.get("/nfl/schedule/")
        self.assertEqual(response.status_code, 200)

    def test_nfl_stats(self):
        response = self.client.get("/nfl/stats/1/")
        self.assertEqual(response.status_code, 200)

    def test_nfl_home_team(self):
        response = self.client.get("/nfl/team/home/1/BAL/baltimore-ravens/")
        self.assertEqual(response.status_code, 200)