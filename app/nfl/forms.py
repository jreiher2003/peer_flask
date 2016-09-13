from flask_wtf import Form 
from wtforms import TextField, IntegerField, RadioField
# , choices=[('home', 'HomeTeam'), ('away', 'AwayTeam')]
class CreateNflBet(Form):
    away_team = TextField("Away Team")
    home_team = TextField("Home Team")
    point_spread = IntegerField("Point Spread")
    over_under = IntegerField("Over/Under")
    home_team_ml = IntegerField("Home Team ML")
    away_team_ml = IntegerField("Away Team ML")
    amount = IntegerField("Bet Amount")
    
