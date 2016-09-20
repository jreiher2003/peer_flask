from flask_wtf import Form 
from wtforms import TextField, IntegerField, RadioField, HiddenField
# , choices=[('home', 'HomeTeam'), ('away', 'AwayTeam')]
class CreateNflBet(Form):
    game_key = HiddenField("Game Key")
    bet_key = HiddenField("Bet Key")
    away_team = TextField("Away Team")
    home_team = TextField("Home Team")
    over_under = IntegerField("Over/Under")
    point_spread = IntegerField("Point Spread")
    home_team_ml = IntegerField("Home Team ML")
    away_team_ml = IntegerField("Away Team ML")
    amount = IntegerField("Bet Amount")
    
