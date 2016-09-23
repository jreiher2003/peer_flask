import datetime
from app import db
from app.users.models import Users, Role, UserRoles, Profile


class OverUnderBet(db.Model):
    __tablename__ = "over_under_bet"

    id = db.Column(db.Integer, primary_key=True)
    game_key = db.Column(db.Integer)
    bet_key = db.Column(db.Integer, unique=True)
    over_under = db.Column(db.Float)
    amount = db.Column(db.Integer)
    bet_taken = db.Column(db.Boolean, default=False)
    taken_by = db.Column(db.Integer) # other player id 
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id,ondelete='CASCADE'))
    users = db.relationship(Users)
    bet_created = db.Column(db.DateTime(),  default=datetime.datetime.now())
    bet_modified = db.Column(db.DateTime,  default=datetime.datetime.now(),
                                       onupdate=datetime.datetime.now())
    bet_taken = db.Column(db.DateTime())

class HomeTeamBet(db.Model):
    __tablename__ = "home_team_bet"

    id = db.Column(db.Integer, primary_key=True)
    game_key = db.Column(db.Integer)
    bet_key = db.Column(db.Integer, unique=True)
    home_team = db.Column(db.String(25))
    home_ps = db.Column(db.Integer)
    home_ml = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    bet_taken = db.Column(db.Boolean)
    taken_by = db.Column(db.Integer) # other player id 
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id,ondelete='CASCADE'))
    users = db.relationship(Users)
    bet_created = db.Column(db.DateTime(),  default=datetime.datetime.now())
    bet_modified = db.Column(db.DateTime,  default=datetime.datetime.now(),
                                       onupdate=datetime.datetime.now())
    bet_taken = db.Column(db.DateTime())

class AwayTeamBet(db.Model):
    __tablename__ = "away_team_bet"

    id = db.Column(db.Integer, primary_key=True)
    game_key = db.Column(db.Integer)
    bet_key = db.Column(db.Integer, unique=True)
    away_team = db.Column(db.String(25))
    away_ps = db.Column(db.Integer)
    away_ml = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    bet_taken = db.Column(db.Boolean)
    taken_by = db.Column(db.Integer) # other player id 
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id,ondelete='CASCADE'))
    users = db.relationship(Users)
    bet_created = db.Column(db.DateTime(),  default=datetime.datetime.now())
    bet_modified = db.Column(db.DateTime,  default=datetime.datetime.now(),
                                       onupdate=datetime.datetime.now())
    bet_taken = db.Column(db.DateTime())