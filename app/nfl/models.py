import datetime
from app import db
from app.users.models import Users, Role, UserRoles, Profile


class Base(db.Model):
    __tablename__ = "base"
    id = db.Column(db.Integer, primary_key=True)
    game_key = db.Column(db.Integer)
    bet_key = db.Column(db.Integer, unique=True) 
    game_date = db.Column(db.DateTime)
    vs = db.Column(db.String)
    home_team = db.Column(db.String)
    away_team = db.Column(db.String)
    win = db.Column(db.Boolean)
    lose = db.Column(db.Boolean)
    amount = db.Column(db.Integer)
    bet_taken = db.Column(db.Boolean, default=False)
    bet_graded = db.Column(db.Boolean, default=False)
    taken_by = db.Column(db.Integer) # other player id 
    paid = db.Column(db.Boolean, default=False)
    bet_created = db.Column(db.DateTime,  default=datetime.datetime.utcnow)
    bet_modified = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
   

    def ps_format(self):
        if self.ps == None: return ""
        elif self.ps > 0: return "+" + str(self.ps)
        else: return self.ps

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
        elif self.ps < 0: return str(self.ps).replace("-", "+")
        else: return "-"+str(self.ps)

    def opposite_over_under(self):
        if self.total == None: return ""
        elif self.over_under == "u": return "o"
        else: return "u"

    def amount_win(self):
        return round(float(self.amount) * .9,2)


class NFLcreateOverUnderBet(Base):
    __tablename__ = "nfl_create_ou_bet"

    id = db.Column(db.Integer, db.ForeignKey(Base.id), primary_key=True)
    over_under = db.Column(db.String)
    total = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'))
    users = db.relationship(Users, back_populates="nfl_create_ou_bet")

class NFLcreateSideBet(Base):
    __tablename__ = "nfl_create_side_bet"

    id = db.Column(db.Integer, db.ForeignKey(Base.id), primary_key=True)
    team = db.Column(db.String)
    ps = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'))
    users = db.relationship(Users, back_populates="nfl_create_side_bet")

class NFLcreateMLBet(Base):
    __tablename__ = "nfl_create_ml_bet"

    id = db.Column(db.Integer, db.ForeignKey(Base.id), primary_key=True)
    team = db.Column(db.String)
    ml = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'))
    users = db.relationship(Users, back_populates="nfl_create_ml_bet")
   

class NFLBetGraded(db.Model):
    __tablename__ = 'nfl_bet_graded'

    id = db.Column(db.Integer, primary_key=True)
    game_key = db.Column(db.Integer)
    week = db.Column(db.String)
    game_date = db.column(db.DateTime)
    home_team = db.Column(db.String)
    away_team = db.Column(db.String)
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    total_score = db.Column(db.Integer)
    over_under = db.Column(db.Integer)
    ps = db.Column(db.Integer)
    cover_total = db.Column(db.String)
    cover_side = db.Column(db.String)
    # user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'))



