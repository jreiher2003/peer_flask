import json
import datetime
import random
from string import hexdigits

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

def make_salt(length=10):
    return "".join(random.choice(hexdigits) for x in xrange(length))

def today_date():
    t = datetime.time()
    d = datetime.date.today()
    return datetime.datetime.combine(d,t)

def today_and_now():
    return datetime.datetime.now()

## OFFENSIVE STATS by TEAM
def team_rush_avg(rush_yds, team):
    team_rush_avg = []
    for x in teamseason:
        if x["SeasonType"] == 1:
            team_rush_avg.append((x["RushingYards"],x["Team"]))
    team_rush_avg =  sorted(team_rush_avg, key=lambda x: x[0], reverse=True) 
    rank = team_rush_avg.index((rush_yds, team)) + 1
    return rank

def team_pass_avg(pass_yds, team):
    team_pass_avg = []
    for x in teamseason:
        if x["SeasonType"] == 1:
            team_pass_avg.append((x["PassingYards"],x["Team"]))
    team_pass_avg =  sorted(team_pass_avg, key=lambda x: x[0], reverse=True) 
    rank = team_pass_avg.index((pass_yds, team)) + 1
    return rank

def opp_team_rush_avg(rush_yds, team):
    oppteam_rush_avg = []
    for x in teamseason:
        if x["SeasonType"] == 1:
            oppteam_rush_avg.append((x["OpponentRushingYards"],x["Team"]))
    oppteam_rush_avg =  sorted(oppteam_rush_avg, key=lambda x: x[0]) 
    rank = oppteam_rush_avg.index((rush_yds, team)) + 1
    return rank

def opp_team_pass_avg(pass_yds, team):
    oppteam_pass_avg = []
    for x in teamseason:
        if x["SeasonType"] == 1:
            oppteam_pass_avg.append((x["OpponentPassingYards"],x["Team"]))
    oppteam_pass_avg =  sorted(oppteam_pass_avg, key=lambda x: x[0]) 
    rank = oppteam_pass_avg.index((pass_yds, team)) + 1
    return rank

def team_off_avg(pass_yds, team):
    team_pass_avg = []
    for x in teamseason:
        if x["SeasonType"] == 1:
            team_pass_avg.append((x["OffensiveYards"],x["Team"]))
    team_pass_avg =  sorted(team_pass_avg, key=lambda x: x[0], reverse=True) 
    rank = team_pass_avg.index((pass_yds, team)) + 1
    return rank

def team_def_avg(pass_yds, team):
    team_pass_avg = []
    for x in teamseason:
        if x["SeasonType"] == 1:
            team_pass_avg.append((x["OpponentOffensiveYards"],x["Team"]))
    team_pass_avg =  sorted(team_pass_avg, key=lambda x: x[0]) 
    rank = team_pass_avg.index((pass_yds, team)) + 1
    return rank

# NFL OFFENSIVE STATS ##################################################
def nfl_off_yds(col_to_sort):
    return sorted(teamseason, key=lambda k: int(k[col_to_sort]), reverse=True)
    
             