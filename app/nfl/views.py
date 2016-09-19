import json
import datetime
from app import app, db
from forms import CreateNflBet
from flask import Blueprint, render_template, url_for
from slugify import slugify
from .utils import team_rush_avg, team_pass_avg, \
opp_team_rush_avg, opp_team_pass_avg, team_off_avg, \
team_def_avg, today_date,today_and_now, nfl_off_yds


nfl_blueprint = Blueprint("nfl", __name__, template_folder="templates")

with open('sports/Schedule.2016.json') as data_file:    
        schedule = json.load(data_file)
with open('sports/Standing.2016.json') as data_file1:    
        standing = json.load(data_file1)
with open('sports/Team.2016.json') as data_file2:    
        nflteam = json.load(data_file2)
with open('sports/Stadium.2016.json') as data_file3:    
        stadium = json.load(data_file3)
with open('sports/TeamSeason.2016.json') as data_file4:    
        teamseason = json.load(data_file4)
with open('sports/TeamGame.2016.json') as data_file5:    
        teamgame = json.load(data_file5)
with open('sports/Score.2016.json') as data_file6:    
        score = json.load(data_file6)


@nfl_blueprint.route("/nfl/home/")
@nfl_blueprint.route("/nfl/")
def nfl_home():
    all_teams = nflteam
    return render_template("nfl_home.html", all_teams=all_teams)

@nfl_blueprint.route("/nfl/schedule/")
def nfl_schedule():
    all_teams = nflteam
    dt = today_date()
    dn = today_and_now()
    return render_template(
        "nfl_schedule.html", 
        all_teams=all_teams, 
        data=schedule, 
        dt=dt, 
        dn=dn, 
        teamgame=teamgame
        )

@nfl_blueprint.route("/nfl/board/")
def nfl_public_board():
    all_teams = nflteam
    return render_template("nfl_public_board.html", all_teams=all_teams)

@nfl_blueprint.route("/nfl/create/")
def nfl_create_broad():
    all_teams = nflteam
    return "create reg"

@nfl_blueprint.route("/nfl/board/create/<path:game_key>/", methods=["GET","POST"])
def nfl_create_bet(game_key):
    all_teams = nflteam
    form = CreateNflBet()
    nfl_game = [d for d in schedule if d['GameKey'] == game_key][0]
    return render_template(
        "nfl_create_bet.html",
        form=form, 
        nfl_game=nfl_game, 
        all_teams=all_teams
        )

@nfl_blueprint.route("/nfl/confirm/")
def nfl_confirm_bet():
    all_teams = nflteam
    return "nfl confim"

@nfl_blueprint.route("/nfl/scores/")
def nfl_scores():
    all_teams = nflteam
    return "nfl scores"

@nfl_blueprint.route("/nfl/standings/")
def nfl_standings():
    all_teams = nflteam
    return render_template("nfl standings.html", standing=standing, all_teams=all_teams)

@nfl_blueprint.route("/nfl/stats/<int:sid>/")
def nfl_stats(sid):
    all_teams = nflteam
    teamseason1 = [x for x in teamseason if x["SeasonType"] == sid]
    return render_template("nfl_stats.html", all_teams=all_teams, teamseason=teamseason1,)

@nfl_blueprint.route("/nfl/team/home/<int:sid>/<path:team>/")
def nfl_team_home(sid,team):
    dt = today_date()
    all_teams = nflteam
    nfl_team = [x for x in nflteam if slugify(x["FullName"]) == team]
    nfl_team_key = [x["Key"] for x in nfl_team][0]
    team_season_stats = [x for x in teamseason if x["Team"] == nfl_team_key]
    team_season_stats1 = [x for x in team_season_stats if x["SeasonType"] == sid]

    team_schedule1 = [x for x in schedule if x["AwayTeam"] == nfl_team_key or x["HomeTeam"] == nfl_team_key]
    team_schedule = [x for x in team_schedule1 if x["SeasonType"] == sid]
    team_score1 = [x for x in score if x["SeasonType"] == sid]
    team_score = [x for x in team_score1 if x["AwayTeam"] == nfl_team_key or x["HomeTeam"] == nfl_team_key]

    team_rush_rank = [team_rush_avg(x["RushingYards"],x["Team"]) for x in team_season_stats if x["SeasonType"] == 1][0]
    team_pass_rank = [team_pass_avg(x["PassingYards"],x["Team"]) for x in team_season_stats if x["SeasonType"] == 1][0]
    opp_team_rush_rank = [opp_team_rush_avg(x["OpponentRushingYards"],x["Team"]) for x in team_season_stats if x["SeasonType"] == 1][0]
    opp_team_pass_rank = [opp_team_pass_avg(x["OpponentPassingYards"],x["Team"]) for x in team_season_stats if x["SeasonType"] == 1][0]
    team_off_rank = [team_off_avg(x["OffensiveYards"],x["Team"]) for x in team_season_stats if x["SeasonType"] == 1][0]
    team_def_rank = [team_def_avg(x["OpponentOffensiveYards"],x["Team"]) for x in team_season_stats if x["SeasonType"] == 1][0]

    nflfull = [x["FullName"] for x in nfl_team][0]
    sID = [x["StadiumID"] for x in nfl_team][0]
    team_stadium = [y for y in stadium if y["StadiumID"] == sID]
    team_standing = [z for z in standing if z["Name"] == nflfull]
    return render_template(
        "nfl_team_home.html",
        nfl_team=nfl_team,
        nfl_stadium_standing=zip(nfl_team,team_stadium,team_standing),
        all_teams=all_teams,
        team_season_stats=team_season_stats1,
        team_rush_rank=team_rush_rank,
        team_pass_rank=team_pass_rank,
        opp_team_rush_rank=opp_team_rush_rank,
        opp_team_pass_rank=opp_team_pass_rank,
        team_off_rank=team_off_rank,
        team_def_rank=team_def_rank,
        team_schedule=team_schedule,
        team_score=team_score,
        team_schedule_team_score=zip(team_schedule,team_score),
        dt=dt,
        team=team
        )

@nfl_blueprint.route("/nfl/team/schedule/<path:team>/")
def nfl_team_schedule(team):
    all_teams = nflteam
    return "schedule"

@nfl_blueprint.route("/nfl/team/stats/<path:team>/")
def nfl_team_stats(team):
    all_teams = nflteam
    return "stats"








