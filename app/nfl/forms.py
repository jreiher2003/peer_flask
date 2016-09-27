import json
from flask_wtf import Form 
from wtforms import TextField, IntegerField, RadioField, HiddenField, FloatField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from app import db
from app.nfl_stats.models import NFLStandings, NFLTeam, NFLStadium, NFLSchedule, NFLScore, NFLTeamSeason


def validate_teamname(form, field):
    team = db.session.query(NFLTeam.Key).all()
    tl = [i[0] for i in team]
    if field.data not in tl:
        raise ValidationError("That is not a valid team")

def validate_gamekey(form, field):
    key = db.session.query(NFLSchedule.GameKey).all()
    kl = [i[0] for i in key]
    if field.data not in kl:
        raise ValidationError("That is not a valid game key")
    
class OverUnderForm(Form):
    game_key = HiddenField("Game Key", validators=[DataRequired(), validate_gamekey])
    home = HiddenField("home",validators=[DataRequired()])
    away = HiddenField("away",validators=[DataRequired()])
    total = FloatField("Over/Under", validators=[NumberRange(min=25, max=70, message="Over/Under bet must be inbetween 25 and 70 for it to be valid.")])#
    amount = TextField("Bet Amount", validators=[DataRequired(), NumberRange(min=0, message="All amounts must be positive")])#
    over_under = RadioField("Pick One", choices=[("o", "Over"), ("u","Under")], validators=[DataRequired(message="You need to pick one")])
    submit_o = SubmitField("Bet Over/Under")

class HomeTeamForm(Form):
    game_key = HiddenField("Game Key", validators=[DataRequired(), validate_gamekey])
    home = HiddenField("home",validators=[DataRequired()])
    away = HiddenField("away",validators=[DataRequired()])
    home_team = TextField("Home Team", validators=[DataRequired(message="Home_team data required"), validate_teamname])
    point_spread = FloatField("Point Spread", validators=[DataRequired(message="home ps data required")])#
    home_team_ml = IntegerField("Home Team ML")
    amount = TextField("Bet Amount", validators=[DataRequired(message="home team amount data required"), NumberRange(min=0, message="All amounts must be positive")])#
    submit_h = SubmitField("Bet Home Team")

class AwayTeamForm(Form):
    game_key = HiddenField("Game Key", validators=[DataRequired(), validate_gamekey])
    home = HiddenField("home",validators=[DataRequired()])
    away = HiddenField("away",validators=[DataRequired()])
    away_team = TextField("Away Team", validators=[DataRequired(), validate_teamname])
    point_spread = FloatField("Point Spread", validators=[DataRequired()])#
    away_team_ml = IntegerField("Away Team ML")
    amount = TextField("Bet Amount", validators=[DataRequired(), NumberRange(min=0, message="All amounts must be positive")])#
    submit_a = SubmitField("Bet Away Team")