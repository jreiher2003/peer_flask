from flask_wtf import Form 
from wtforms import TextField, IntegerField, RadioField, HiddenField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

    
class OverUnderForm(Form):
    game_key = HiddenField("Game Key", validators=[DataRequired()])
    over_under = FloatField("Over/Under")#, validators=[NumberRange(min=-100, max=100, message="Over/Under bet must be inbetween -100 and 100 for it to be valid.")]
    amount = TextField("Bet Amount")#, validators=[DataRequired(), NumberRange(min=0, message="All amounts must be positive")]
    submit_o = SubmitField("Bet Over/Under")

class HomeTeamForm(Form):
    game_key = HiddenField("Game Key", validators=[DataRequired()])
    home_team = TextField("Home Team", validators=[DataRequired(message="Home_team data required")])
    point_spread = FloatField("Point Spread")#, validators=[DataRequired(message="home ps data required")]
    home_team_ml = IntegerField("Home Team ML")
    amount = TextField("Bet Amount")#, validators=[DataRequired(message="home team amount data required"), NumberRange(min=0, message="All amounts must be positive")]
    submit_h = SubmitField("Bet Home Team")

class AwayTeamForm(Form):
    game_key = HiddenField("Game Key", validators=[DataRequired()])
    away_team = TextField("Away Team", validators=[DataRequired()])
    point_spread = FloatField("Point Spread")#, validators=[DataRequired()]
    away_team_ml = IntegerField("Away Team ML")
    amount = TextField("Bet Amount")#, validators=[DataRequired(), NumberRange(min=0, message="All amounts must be positive")]
    submit_a = SubmitField("Bet Away Team")