import json
from dateutil.parser import parse
from flask_wtf import Form 
from wtforms import TextField, IntegerField, RadioField, HiddenField, FloatField, SubmitField, BooleanField
import datetime
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from app import db
from app.nfl_stats.models import NFLStandings, NFLTeam, NFLStadium, NFLSchedule, NFLScore, NFLTeamSeason

def validate_teamname(form, field):
    team = ['ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC', 'LA', 'MIA', 'MIN', 'NE', 'NO', 'NYG', 'NYJ', 'OAK', 'PHI', 'PIT', 'SD', 'SEA', 'SF', 'TB', 'TEN', 'WAS']
    if field.data not in team:
        raise ValidationError("That is not a valid team")

def validate_gamekey(form, field):
    dt = datetime.datetime.today()
    key = db.session.query(NFLSchedule.GameKey,NFLSchedule.Date).all()
    kl = [i[0] for i in key if parse(i[1]) >= dt]
    if field.data not in kl:
        raise ValidationError("That is not a valid game key")

def validate_pointspread(form, field):
    if field.data is None:
        raise ValidationError("That is not a valid number.")
    if field.data < -21:
        raise ValidationError("That is not a valid number. It is less than -21.")
    if field.data > 21:
        raise ValidationError("That is not a valid number. It is more than 21.")
    
class OverUnderForm(Form):
    game_key = HiddenField("Game Key", validators=[DataRequired(), validate_gamekey])
    home_ = HiddenField("home",validators=[DataRequired(), validate_teamname])
    away_ = HiddenField("away",validators=[DataRequired(), validate_teamname])
    total = FloatField("Over/Under", validators=[NumberRange(min=25, max=70, message="Over/Under bet must be inbetween 25 and 70 for it to be valid.")])#
    amount = TextField("Bet Amount", validators=[DataRequired(), NumberRange(min=0, message="All amounts must be positive")])#
    over_under = RadioField("Pick One", choices=[("o", "Over"), ("u","Under")], validators=[DataRequired(message="You need to pick one")])
    submit_o = SubmitField("Bet Over/Under")

class HomeTeamForm(Form):
    game_key = HiddenField("Game Key", validators=[DataRequired(), validate_gamekey])
    home_ = HiddenField("home",validators=[DataRequired(), validate_teamname])
    away_ = HiddenField("away",validators=[DataRequired(), validate_teamname])
    home_team = TextField("Home Team", validators=[DataRequired(message="Home_team data required"), validate_teamname])
    point_spread = FloatField("Point Spread", validators=[validate_pointspread])#validate_pointspread
    home_team_ml = IntegerField("Home Team ML")
    amount = TextField("Bet Amount", validators=[DataRequired(message="home team amount data required"), NumberRange(min=0, message="All amounts must be positive")])#
    submit_h = SubmitField("Bet Home Team")

class AwayTeamForm(Form):
    game_key = HiddenField("Game Key", validators=[DataRequired(), validate_gamekey])
    home_ = HiddenField("home",validators=[DataRequired(), validate_teamname])
    away_ = HiddenField("away",validators=[DataRequired(), validate_teamname])
    away_team = TextField("Away Team", validators=[DataRequired(), validate_teamname])
    point_spread = FloatField("Point Spread", validators=[validate_pointspread])#validate_pointspread
    away_team_ml = IntegerField("Away Team ML")
    amount = TextField("Bet Amount", validators=[DataRequired(), NumberRange(min=0, message="All amounts must be positive")])#
    submit_a = SubmitField("Bet Away Team")