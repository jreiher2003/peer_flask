import datetime
from app import db
from app.users.models import Users, Role, UserRoles, Profile


class NFLcreateBet(db.Model):
    __tablename__ = "nfl_create_bet"

    id = db.Column(db.Integer, primary_key=True)
    game_key = db.Column(db.Integer)
    bet_key = db.Column(db.Integer, unique=True)
    game_date = db.Column(db.DateTime)
    over_under = db.Column(db.String, default=" ")
    total = db.Column(db.Integer)
    amount = db.Column(db.Numeric(12,2))
    vs = db.Column(db.String)
    home_team = db.Column(db.String)
    away_team = db.Column(db.String)
    team = db.Column(db.String, default=" ")
    ps = db.Column(db.Integer)
    ml = db.Column(db.Integer)
    bet_taken = db.Column(db.Boolean, default=False)
    taken_by = db.Column(db.Integer) # other player id 
    bet_created = db.Column(db.DateTime,  default=datetime.datetime.now())
    bet_modified = db.Column(db.DateTime,  default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    bet_taken = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'))
    users = db.relationship(Users, back_populates="nfl_create_bet")
    nfl_take_bet = db.relationship("NFLtakeBet", uselist=False, back_populates="nfl_create_bet")

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

    @property 
    def opposite_team(self):
        if self.ps == None:
            return ""
        elif self.team == self.home_team:
            return self.away_team 
        else:
            return self.home_team 

    @property 
    def opposite_ps(self):
        if self.ps == None:
            return ""
        elif self.ps < 0:
            return str(self.ps).replace("-", "+")
        else:
            return "-"+str(self.ps)

    def opposite_over_under(self):
        if self.total == None:
            return ""
        elif self.over_under == "u":
            return "o"
        else:
            return "u"

    def amount_win(self):
        return float(self.amount) * .9

class NFLtakeBet(db.Model):
    __tablename__ = 'nfl_take_bet'
    id = db.Column(db.Integer, primary_key=True)
    nfl_create_bet_id = db.Column(db.Integer, db.ForeignKey('nfl_create_bet.id'))
    nfl_create_bet = db.relationship("NFLcreateBet", back_populates="nfl_take_bet")
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'))
    users = db.relationship(Users, back_populates="nfl_take_bet")
