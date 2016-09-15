import json
import datetime
from app import app, db
from forms import CreateNflBet
from flask import Blueprint, render_template, url_for
from slugify import slugify
from .utils import team_rush_avg, team_pass_avg, opp_team_rush_avg, opp_team_pass_avg, team_off_avg, team_def_avg


nfl_blueprint = Blueprint("nfl", __name__, template_folder="templates")

with open('sports/Schedule.2016.json') as data_file:    
        data = json.load(data_file)
with open('sports/Standing.2016.json') as data_file1:    
        standing = json.load(data_file1)
with open('sports/Team.2016.json') as data_file2:    
        nflteam = json.load(data_file2)
with open('sports/Stadium.2016.json') as data_file3:    
        stadium = json.load(data_file3)
with open('sports/TeamSeason.2016.json') as data_file4:    
        teamseason = json.load(data_file4)


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

@nfl_blueprint.route("/nfl/team/home/<path:team>/")
def nfl_team_home(team):
    
    all_teams = nflteam
    nfl_team = [x for x in nflteam if slugify(x["FullName"]) == team]
    nfl_team_key = [x["Key"] for x in nfl_team][0]
    team_season_team = [x for x in teamseason if x["Team"] == nfl_team_key] 
    team_rush_rank = [team_rush_avg(x["RushingYards"],x["Team"]) for x in team_season_team if x["SeasonType"] == 1][0]
    team_pass_rank = [team_pass_avg(x["PassingYards"],x["Team"]) for x in team_season_team if x["SeasonType"] == 1][0]
    opp_team_rush_rank = [opp_team_rush_avg(x["OpponentRushingYards"],x["Team"]) for x in team_season_team if x["SeasonType"] == 1][0]
    opp_team_pass_rank = [opp_team_pass_avg(x["OpponentPassingYards"],x["Team"]) for x in team_season_team if x["SeasonType"] == 1][0]
    team_off_rank = [team_off_avg(x["OffensiveYards"],x["Team"]) for x in team_season_team if x["SeasonType"] == 1][0]
    team_def_rank = [team_def_avg(x["OpponentOffensiveYards"],x["Team"]) for x in team_season_team if x["SeasonType"] == 1][0]
    nflfull = [x["FullName"] for x in nfl_team][0]
    sID = [x["StadiumID"] for x in nfl_team][0]
    team_stadium = [y for y in stadium if y["StadiumID"] == sID]
    team_standing = [z for z in standing if z["Name"] == nflfull]
    return render_template(
        "nfl_team.html",
        nfl_team=nfl_team,
        nfl_stadium_standing=zip(nfl_team,team_stadium,team_standing),
        all_teams=all_teams,
        team_season_team=team_season_team,
        team_rush_rank=team_rush_rank,
        team_pass_rank=team_pass_rank,
        opp_team_rush_rank=opp_team_rush_rank,
        opp_team_pass_rank=opp_team_pass_rank,
        team_off_rank=team_off_rank,
        team_def_rank=team_def_rank
        )

@nfl_blueprint.route("/nfl/team/schedule/<path:team>/")
def nfl_team_schedule(team):
    return "schedule"

@nfl_blueprint.route("/nfl/team/stats/<path:team>/")
def nfl_team_stats(team):
    return "stats"








