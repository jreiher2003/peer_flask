import json
import datetime
import random
from string import hexdigits
from app import db
from app.nfl_stats.models import NFLStandings, NFLTeam, NFLStadium, NFLSchedule, NFLScore, NFLTeamSeason

def make_salt(length=10):
    return "".join(random.choice(hexdigits) for x in xrange(length))

def today_date():
    t = datetime.time()
    d = datetime.date.today()
    return datetime.datetime.combine(d,t)

def today_and_now():
    return datetime.datetime.now()

def yesterday():
    return datetime.datetime.now() - datetime.timedelta(days=1)

## OFFENSIVE STATS by TEAM
def team_rush_avg(rush_yds, team):
    q = db.session.query(NFLTeamSeason.RushingYards,NFLTeamSeason.Team).filter_by(SeasonType=1).order_by('RushingYards desc').all()
    team_ = []
    for y,t in q:
        team_.append((y,t)) 
    return team_.index((rush_yds, team)) + 1
    

def team_pass_avg(pass_yds, team):
    q = db.session.query(NFLTeamSeason.PassingYards,NFLTeamSeason.Team).filter_by(SeasonType=1).order_by('PassingYards desc').all()
    team_ = []
    for y,t in q:
        team_.append((y,t))
    return team_.index((pass_yds, team)) + 1
    

def opp_team_rush_avg(rush_yds, team):
    q = db.session.query(NFLTeamSeason.OpponentRushingYards,NFLTeamSeason.Team).filter_by(SeasonType=1).order_by('OpponentRushingYards asc').all()
    team_ = []
    for y,t in q:
        team_.append((y,t))
    return team_.index((rush_yds, team)) + 1

def opp_team_pass_avg(pass_yds, team):
    q = db.session.query(NFLTeamSeason.OpponentPassingYards,NFLTeamSeason.Team).filter_by(SeasonType=1).order_by('OpponentPassingYards asc').all()
    team_ = []
    for y,t in q:
        team_.append((y,t))
    return team_.index((pass_yds, team)) + 1

def team_off_avg(pass_yds, team):
    q = db.session.query(NFLTeamSeason.OffensiveYards,NFLTeamSeason.Team).filter_by(SeasonType=1).order_by('OffensiveYards desc').all()
    team_ = []
    for y,t in q:
        team_.append((y,t))
    return team_.index((pass_yds, team)) + 1

def team_def_avg(pass_yds, team):
    q = db.session.query(NFLTeamSeason.OpponentOffensiveYards,NFLTeamSeason.Team).filter_by(SeasonType=1).order_by('OpponentOffensiveYards asc').all()
    team_ = []
    for y,t in q:
        team_.append((y,t))
    return team_.index((pass_yds, team)) + 1

# NFL OFFENSIVE STATS ##################################################
# def nfl_off_yds(col_to_sort):
#     return sorted(teamseason, key=lambda k: int(k[col_to_sort]), reverse=True)
    
             