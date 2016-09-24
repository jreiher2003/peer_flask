import json
from flask_wtf import Form 
from wtforms import TextField, IntegerField, RadioField, HiddenField, FloatField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError

with open('sports/Team.2016.json') as data_file2:    
    nflteam = json.load(data_file2)
with open('sports/Schedule.2016.json') as data_file:    
        schedule = json.load(data_file)

def validate_teamname(form, field):
    team = [x["Key"] for x in nflteam]
    if field.data not in team:
        raise ValidationError("That is not a valid team")

def validate_gamekey(form, field):
    key = [x["GameKey"] for x in schedule]
    if field.data not in key:
        raise ValidationError("That is not a valid game key")
    
class OverUnderForm(Form):
    game_key = HiddenField("Game Key", validators=[DataRequired(), validate_gamekey])
    total = FloatField("Over/Under", validators=[NumberRange(min=25, max=70, message="Over/Under bet must be inbetween 25 and 70 for it to be valid.")])#
    amount = TextField("Bet Amount", validators=[DataRequired(), NumberRange(min=0, message="All amounts must be positive")])#
    over_under = RadioField("Pick One", choices=[("o", "Over"), ("u","Under")], validators=[DataRequired()])
    
    submit_o = SubmitField("Bet Over/Under")

class HomeTeamForm(Form):
    game_key = HiddenField("Game Key", validators=[DataRequired(), validate_gamekey])
    home_team = TextField("Home Team", validators=[DataRequired(message="Home_team data required"), validate_teamname])
    point_spread = FloatField("Point Spread", validators=[DataRequired(message="home ps data required")])#
    home_team_ml = IntegerField("Home Team ML")
    amount = TextField("Bet Amount", validators=[DataRequired(message="home team amount data required"), NumberRange(min=0, message="All amounts must be positive")])#
    submit_h = SubmitField("Bet Home Team")

class AwayTeamForm(Form):
    game_key = HiddenField("Game Key", validators=[DataRequired(), validate_gamekey])
    away_team = TextField("Away Team", validators=[DataRequired(), validate_teamname])
    point_spread = FloatField("Point Spread", validators=[DataRequired()])#
    away_team_ml = IntegerField("Away Team ML")
    amount = TextField("Bet Amount", validators=[DataRequired(), NumberRange(min=0, message="All amounts must be positive")])#
    submit_a = SubmitField("Bet Away Team")