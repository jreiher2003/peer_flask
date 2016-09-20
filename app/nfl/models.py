import datetime
from app import db
from app.users.models import Users, Role, UserRoles, Profile

class NflBet(db.Model):
    __tablename__ = "nflbet"

    id = db.Column(db.Integer, primary_key=True)
    game_key = db.Column(db.Integer)
    over_under = db.Column(db.Integer)
    home_team = db.Column(db.String(25))
    home_ml = db.Column(db.Integer)
    home_ps = db.Column(db.Integer)
    away_team = db.Column(db.String(25))
    away_ml = db.Column(db.Integer)
    away_ps = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id,ondelete='CASCADE'))
    users = db.relationship(Users)
    date_created = db.Column(db.DateTime(),  default=datetime.datetime.now())
    date_modified = db.Column(db.DateTime,  default=datetime.datetime.now(),
                                       onupdate=datetime.datetime.now())

    def __repr__(self):
        return "<gamekey-{}".format(self.game_key)