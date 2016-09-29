import datetime
from app import db
from app.users.models import Users, Role, UserRoles, Profile


class NFLBet(db.Model):
    __tablename__ = "nfl_bet"

    id = db.Column(db.Integer, primary_key=True)
    game_key = db.Column(db.Integer)
    bet_key = db.Column(db.Integer, unique=True)
    game_date = db.Column(db.DateTime)
    over_under = db.Column(db.String, default=" ")
    total = db.Column(db.Integer)
    amount = db.Column(db.Numeric(12,2))
    vs = db.Column(db.String)
    team = db.Column(db.String, default=" ")
    ps = db.Column(db.Integer)
    ml = db.Column(db.Integer)
    bet_taken = db.Column(db.Boolean, default=False)
    taken_by = db.Column(db.Integer) # other player id 
    bet_created = db.Column(db.DateTime,  default=datetime.datetime.now())
    bet_modified = db.Column(db.DateTime,  default=datetime.datetime.now(),
                                       onupdate=datetime.datetime.now())
    bet_taken = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'))
    users = db.relationship(Users, back_populates="nflbet")

    def ps_format(self):
        if self.ps == None:
            return ""
        elif self.ps > 0:
            return "+" + str(self.ps)
        else:
            return self.ps

    def total_format(self):
        return "" if self.total == None else self.total
        
    @property 
    def format_bet_created(self):
        return "{dt:%Y-%m-%d}".format(dt=self.bet_created)

# class HomeTeamBet(db.Model):
#     __tablename__ = "home_team_bet"

#     id = db.Column(db.Integer, primary_key=True)
#     game_key = db.Column(db.Integer)
#     bet_key = db.Column(db.Integer, unique=True)
#     game_date = db.Column(db.DateTime)
#     home_team = db.Column(db.String(25))
#     vs = db.Column(db.String)
#     home_ps = db.Column(db.Integer)
#     home_ml = db.Column(db.Integer)
#     amount = db.Column(db.Numeric(12,2))
#     bet_taken = db.Column(db.Boolean)
#     taken_by = db.Column(db.Integer) # other player id 
#     bet_created = db.Column(db.DateTime,  default=datetime.datetime.now())
#     bet_modified = db.Column(db.DateTime,  default=datetime.datetime.now(),
#                                        onupdate=datetime.datetime.now())
#     bet_taken = db.Column(db.DateTime)
#     user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'))
#     users = db.relationship(Users, back_populates="home_team")

#     def home_ps_format(self):
#         return "+" + str(self.home_ps) if self.home_ps > 0 else str(self.home_ps)

# class AwayTeamBet(db.Model):
#     __tablename__ = "away_team_bet"

#     id = db.Column(db.Integer, primary_key=True)
#     game_key = db.Column(db.Integer)
#     bet_key = db.Column(db.Integer, unique=True)
#     game_date = db.Column(db.DateTime)
#     away_team = db.Column(db.String(25))
#     vs = db.Column(db.String)
#     away_ps = db.Column(db.Integer)
#     away_ml = db.Column(db.Integer)
#     amount = db.Column(db.Numeric(12,2))
#     bet_taken = db.Column(db.Boolean)
#     taken_by = db.Column(db.Integer) # other player id 
#     bet_created = db.Column(db.DateTime,  default=datetime.datetime.now())
#     bet_modified = db.Column(db.DateTime,  default=datetime.datetime.now(),
#                                        onupdate=datetime.datetime.now())
#     bet_taken = db.Column(db.DateTime)
#     user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'))
#     users = db.relationship(Users, back_populates="away_team")

#     def away_ps_format(self):
#         return "+" + str(self.away_ps) if self.away_ps > 0 else str(self.away_ps)