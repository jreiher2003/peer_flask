from flask_wtf import Form 
from wtforms import TextField, IntegerField, RadioField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class CreateNflBet(Form):
    game_key = HiddenField("Game Key")
    bet_key = HiddenField("Bet Key")
    away_team = TextField("Away Team")
    home_team = TextField("Home Team")
    over_under = IntegerField("Over/Under", validators=[NumberRange(min=-100, max=100, message="Over/Under bet must be inbetween -100 and 100 for it to be valid.")])
    point_spread = IntegerField("Point Spread")
    home_team_ml = IntegerField("Home Team ML")
    away_team_ml = IntegerField("Away Team ML")
    amount = IntegerField("Bet Amount", validators=[DataRequired(), NumberRange(min=0, message="All amounts must be positive")])
    
