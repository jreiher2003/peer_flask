import json
import datetime
from app import app, db
from forms import CreateNflBet
from flask import Blueprint, render_template, url_for
from slugify import slugify


nfl_blueprint = Blueprint("nfl", __name__, template_folder="templates")

with open('sports/Schedule.2016.json') as data_file:    
        data = json.load(data_file)
with open('sports/Standing.2016.json') as data_file1:    
        standing = json.load(data_file1)
with open('sports/Team.2016.json') as data_file2:    
        nflteam = json.load(data_file2)
with open('sports/Stadium.2016.json') as data_file3:    
        stadium = json.load(data_file3)


@nfl_blueprint.route("/nfl/home/")
@nfl_blueprint.route("/nfl/")
def nfl_home():
    return render_template("nfl_home.html")

@nfl_blueprint.route("/nfl/schedule/")
def nfl_schedule():
    t = datetime.time()
    d = datetime.date.today()
    dt = datetime.datetime.combine(d,t)
    dn = datetime.datetime.now()
    return render_template("nfl_schedule.html" , data=data, dt=dt, dn=dn)

@nfl_blueprint.route("/nfl/board/")
def nfl_public_board():
    return render_template("nfl_public_board.html")

@nfl_blueprint.route("/nfl/create/")
def nfl_create_broad():
    return "create reg"

@nfl_blueprint.route("/nfl/board/create/<path:game_key>/")
def nfl_create_bet(game_key):
    for d in data:
        if d['GameKey'] == game_key:
            nfl_game = d
    form = CreateNflBet()
    return render_template("nfl_create_bet.html" ,form=form, nfl_game=nfl_game)

@nfl_blueprint.route("/nfl/confirm/")
def nfl_confirm_bet():
    return "nfl confim"

@nfl_blueprint.route("/nfl/scores/")
def nfl_scores():
    return "nfl scores"

@nfl_blueprint.route("/nfl/standings/")
def nfl_standings():
    return render_template("nfl standings.html", standing=standing,)

@nfl_blueprint.route("/nfl/stats/")
def nfl_stats():
    return "nfl stats"

@nfl_blueprint.route("/nfl/team/<path:team>")
def nfl_team(team):

    nfl = [x for x in nflteam if slugify(x["FullName"]) == team]
    return render_template("nfl_team.html", nfl=nfl, stadium=stadium)



