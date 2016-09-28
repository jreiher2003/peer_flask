from flask_testing import TestCase 
from app import app, db
from app.users.models import Users,Role,UserRoles,Profile 

class BaseTestCase(TestCase):
    """A base test case."""
 
    def create_app(self):
        app.config.from_object('config.TestConfig')
        app.test_client()
        return app

    def setup(self):
        db.create_all()
        db.session.add(
            Users(
            id = 1,
            username="J3ff_",
            password="password",
            email="jeffreiher@gmail.com"))
        db.session.add(Role(id=1, name="admin"))
        db.session.add(UserRoles(id=1, user_id=1, role_id=1))
        db.session.add(Profile(id=1,avatar="jeff.jpg", user_id=1))
        db.session.add(
            Users(
            id = 2,
            username="Finn",
            password="password",
            email="finn@gmail.com"))
        db.session.add(Role(id=2, name="player"))
        db.session.add(UserRoles(id=2, user_id=2, role_id=2))
        db.session.add(Profile(id=2,avatar="finn.jpg", user_id=2))
        db.session.commit()

        db.session.add(AwayTeamBet(id=1, game_key=123, bet_key=123, away_team="BUF", vs="BUF vs @NE", away_ps=1, amount=20, user_id=1))
        db.session.add(HomeTeamBet(id=1, game_key=123, bet_key=123, home_team="NE", vs="BUF vs @NE", home_ps=-1, amount=20, user_id=2))
        db.session.add(OverUnder(id=1, game_key=123, bet_key=123, over_under="o", total=40, amount=20, vs="BUF vs @NE", user_id=1))
        db.session.commit()




    def tearDown(self):
        db.session.remove()
        db.drop_all()