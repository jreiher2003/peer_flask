"""
If in Base you see bet_taken, bet_graded, and paid but Win is Null or None then the game was graded at a Push.
win=True is win for user_id, win=False is win for taken_by.  
 """

import datetime
from app import db
from app.users.models import Users, Role, UserRoles, Profile


class Base(db.Model):
    __tablename__ = "base"
    id = db.Column(db.Integer, primary_key=True)
    game_key = db.Column(db.String)
    bet_key = db.Column(db.String, unique=True) 
    game_date = db.Column(db.DateTime)
    vs = db.Column(db.String)
    home_team = db.Column(db.String)
    away_team = db.Column(db.String)
    win = db.Column(db.Boolean)
    amount = db.Column(db.Numeric(precision=8,scale=5))
    bet_taken = db.Column(db.Boolean, default=False)
    bet_graded = db.Column(db.Boolean, default=False)
    paid = db.Column(db.Boolean, default=False)
    bet_created = db.Column(db.DateTime,  default=datetime.datetime.utcnow)
    bet_modified = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
   
    @property
    def ps_format(self):
        if self.ps == None: return ""
        elif self.ps == 0: return "even"
        elif self.ps > 0: return "+" + str(self.ps)
        else: return self.ps

    @property
    def total_format(self):
        return "" if self.total == None else self.total

    @property
    def format_bet_created(self):
        return "{dt:%Y-%m-%d}".format(dt=self.bet_created)

    @property
    def opposite_team(self):
        if self.ps == None: return ""
        elif self.team == self.home_team: return self.away_team 
        else: return self.home_team 

    @property 
    def opposite_ps(self):
        if self.ps == None: return ""
        elif self.ps == 0.0: return "even"
        elif self.ps < 0: return str(self.ps).replace("-", "+")
        else: return "-"+str(self.ps)

    @property    
    def opposite_over_under(self):
        if self.total == None: return ""
        elif self.over_under == "u": return "o"
        else: return "u"

    @property 
    def opposite_ml(self):
        return "write class method"

    @property    
    def amount_win(self):
        return round(float(self.amount) * .9, 5)

    @property 
    def admin_win(self):
        return self.amount * .1

    @property 
    def ml_win(self):
        if self.ml > 0:
            return self.amount * self.ml / 100.0
        elif self.ml < 0:
            return (self.amount / ((self.ml*-1) / 100.0))

class NFLOverUnderBet(Base):
    __tablename__ = "nfl_ou_bet"

    id = db.Column(db.Integer, db.ForeignKey(Base.id), primary_key=True)
    over_under = db.Column(db.String)
    total = db.Column(db.Float)
    taken_by = db.Column(db.Integer) # other player id 
    taken_username = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'), index=True)
    users = db.relationship(Users, back_populates="nfl_ou_bet")

class NFLSideBet(Base):
    __tablename__ = "nfl_side_bet"

    id = db.Column(db.Integer, db.ForeignKey(Base.id), primary_key=True)
    team = db.Column(db.String)
    ps = db.Column(db.Float, default=0.0)
    taken_by = db.Column(db.Integer) # other player id 
    taken_username = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'), index=True)
    users = db.relationship(Users, back_populates="nfl_side_bet")

class NFLMLBet(Base):
    __tablename__ = "nfl_ml_bet"

    id = db.Column(db.Integer, db.ForeignKey(Base.id), primary_key=True)
    team = db.Column(db.String)
    ml = db.Column(db.Integer)
    taken_by = db.Column(db.Integer) # other player id
    taken_username = db.Column(db.String) 
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'), index=True)
    users = db.relationship(Users, back_populates="nfl_ml_bet")
   
class NFLBetGraded(db.Model):
    __tablename__ = 'nfl_bet_graded'

    id = db.Column(db.Integer, primary_key=True)
    game_key = db.Column(db.String)
    week = db.Column(db.String)
    game_date = db.column(db.DateTime)
    home_team = db.Column(db.String)
    away_team = db.Column(db.String)
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    total_score = db.Column(db.Integer)
    over_under = db.Column(db.Float)
    ps = db.Column(db.Float)
    cover_total = db.Column(db.String)
    cover_side = db.Column(db.String)
    cover_ml = db.Column(db.String)



