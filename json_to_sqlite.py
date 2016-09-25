"""Json to sqlite3 script to dump data into a data base """

import json
import sqlite3
import time

schedule = json.load(open('sports/Schedule.2016.json'))
stadium = json.load(open("sports/Stadium.2016.json"))
team = json.load(open("sports/Team.2016.json"))
standing = json.load(open("sports/Standing.2016.json"))
score = json.load(open("sports/Score.2016.json"))

def connect():
    """Connect to the sqlite database.  Returns a database connection."""
    conn = sqlite3.connect("nfl_odds.db")
    c = conn.cursor()
    return conn, c

def close():
    """ commit changes and close db connection """
    conn.commit()
    return conn.close()

##### create schedule ########################
def create_schedule():
    cs = c.execute("""CREATE TABLE IF NOT EXISTS schedule (id INTEGER PRIMARY KEY, Week INTEGER, AwayTeamMoneyLine INTEGER, StadiumID INTEGER, GameKey TEXT, Canceled BOOLEAN, Season INTEGER, HomeTeam TEXT, ForecastWindSpeed INTEGER, OverUnder NUMERIC, GeoLong REAL, ForecastDescription INTEGER, AwayTeam TEXT, ForecastTempLow INTEGER, PointSpread NUMERIC, ForecastWindChill INTEGER, ForecastTempHigh INTEGER, Date NUMERIC, GeoLat REAL, SeasonType INTEGER, Channel NULL, HomeTeamMoneyLine TEXT)""")
    print "schedule created"
    return cs

############## populate schedule ##############
def populate_schedule():
    for item in schedule:
        c.execute("""insert into schedule (Week,AwayTeamMoneyLine,StadiumID,GameKey,Canceled,Season,HomeTeam,ForecastWindSpeed,OverUnder,GeoLong,ForecastDescription,AwayTeam,ForecastTempLow,PointSpread,ForecastWindChill,ForecastTempHigh,Date,GeoLat,SeasonType,Channel,HomeTeamMoneyLine) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", item.values())
    print "populated schedule"

######  create_stadium #########
def create_stadium():
    cs = c.execute("""CREATE TABLE IF NOT EXISTS stadium (id INTEGER PRIMARY KEY, StadiumID INTEGER, Name TEXT, City TEXT, State TEXT, Country TEXT, Capacity INTEGER, PlayingSurface TEXT, GeoLat REAL, GeoLong REAL)""")
    print "create stadium"
    return cs 

# ######## populate_stadium #####
def populate_stadium():
    columns = list(stadium[0].keys())
    query = "({0}) values ({1})".format(",".join(columns),",?" * len(columns))
    for item in stadium:
        c.execute("""insert into stadium (City,StadiumID,Capacity,Name,PlayingSurface,Country,GeoLong,State,GeoLat) values (?,?,?,?,?,?,?,?,?)""", item.values())
    print "stadium table populated"

###### create Team table ########
def create_team():
    ct = c.execute("""CREATE TABLE IF NOT EXISTS team (id INTEGER PRIMARY KEY, Key TEXT, TeamID INTEGER, PlayerID INTEGER, City TEXT, Name TEXT, Conference TEXT, Division TEXT, FullName TEXT, StadiumID INTEGER, ByeWeek INTEGER, AverageDraftPosition INTEGER, AverageDraftPositionPPR INTEGER, HeadCoach TEXT, OffensiveCoordinator TEXT, DefensiveCoordinator TEXT, SpecialTeamsCoach TEXT, OffensiveScheme TEXT, DefensiveScheme TEXT, UpcomingSalary INTEGER, UpcomingOpponent TEXT, UpcomingOpponentRank INTEGER, UpcomingOpponentPositionRank INTEGER, UpcomingFanDuelSalary INTEGER, UpcomingDraftKingsSalary INTEGER, UpcomingYahooSalary INTEGER)""")
    print "create team table"
    return ct

def populate_team():
    columns = list(team[0].keys())
    query = "({0}) values ({1})".format(",".join(columns),",?" * len(columns))
    for item in team:
        c.execute("""insert into team (Conference,City,DefensiveScheme,PlayerID,ByeWeek,UpcomingSalary,UpcomingOpponentRank,UpcomingYahooSalary,Division,UpcomingDraftKingsSalary,DefensiveCoordinator,AverageDraftPositionPPR,Key,SpecialTeamsCoach,Name,UpcomingOpponent,AverageDraftPosition,UpcomingOpponentPositionRank,StadiumID,OffensiveCoordinator,OffensiveScheme,TeamID,UpcomingFanDuelSalary,HeadCoach,FullName) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",item.values())
    print "populate team table"

def create_standing():
    cs = c.execute("""CREATE TABLE IF NOT EXISTS standing (id INTEGER PRIMARY KEY, SeasonType INTEGER, Season INTEGER, Conference TEXT, Division TEXT, Team TEXT, Name TEXT, Wins INTEGER, Losses INTEGER, Ties INTEGER, Percentage NUMERIC, PointsFor INTEGER, PointsAgainst INTEGER, NetPoints INTEGER, Touchdowns INTEGER, DivisionWins INTEGER, DivisionLosses INTEGER, ConferenceWins INTEGER, ConferenceLosses INTEGER)""")
    print "create standing table"
    return cs
    
def populate_standing():
    columns = list(standing[0].keys())
    query = "({0}) values ({1})".format(",".join(columns),",?" * len(columns))
    for item in standing:
        c.execute("""insert into standing (Conference,Division,PointsAgainst,NetPoints,Name,Wins,Season,Touchdowns,Losses,PointsFor,ConferenceWins,DivisionLosses,Team,Ties,Percentage,DivisionWins,SeasonType,ConferenceLosses) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", item.values())
    print "populate standing table"
    
def create_score():
    cs = c.execute("""CREATE TABLE IF NOT EXISTS score (id INTEGER PRIMARY KEY, GameKey TEXT, SeasonType INTEGER, Season INTEGER, Week INTEGER, Date NUMERIC, AwayTeam TEXT, HomeTeam TEXT, AwayScore INTEGER, HomeScore INTEGER, Channel TEXT, PointSpread INTEGER, OverUnder NUMERIC, Quarter TEXT, TimeRemaining NULL, Possession NULL, Down NULL, Distance NULL, YardLine NULL, YardLineTerritory NULL, RedZone NULL, AwayScoreQuarter1 INTEGER, AwayScoreQuarter2 INTEGER, AwayScoreQuarter3 INTEGER, AwayScoreQuarter4 INTEGER, AwayScoreOvertime INTEGER, HomeScoreQuarter1 INTEGER, HomeScoreQuarter2 INTEGER, HomeScoreQuarter3 INTEGER, HomeScoreQuarter4 INTEGER,
        HomeScoreOvertime INTEGER, HasStarted BOOLEAN, IsInProgress BOOLEAN, IsOver BOOLEAN, Has1stQuarterStarted BOOLEAN,Has2ndQuarterStarted BOOLEAN, Has3rdQuarterStarted BOOLEAN, Has4thQuarterStarted BOOLEAN, IsOvertime BOOLEAN, DownAndDistance NULL, QuarterDescription TEXT, StadiumID INTEGER, LastUpdated NUMERIC, GeoLat REAL, GeoLong REAL, ForecastTempLow INTEGER, ForecastTempHigh INTEGER, ForecastDescription TEXT, ForecastWindChill INTEGER, ForecastWindSpeed INTEGER, AwayTeamMoneyLine INTEGER, HomeTeamMoneyLine INTEGER, Canceled BOOLEAN, Closed BOOLEAN, LastPlay NULL)""")
    print "create score table"
    return cs
        
def populate_score():
    columns = list(score[0].keys())
    query = "({0}) values ({1})".format(",".join(columns),",?" * len(columns))
    for item in score:
        c.execute("""insert into score (TimeRemaining,HomeScoreQuarter1,HomeScoreQuarter2,HomeScoreQuarter3,HomeScoreQuarter4,Distance,OverUnder,Has4thQuarterStarted,AwayTeam,ForecastTempLow,PointSpread,GeoLong,Closed,QuarterDescription,YardLineTerritory,Channel,Week,Down,Has2ndQuarterStarted,GameKey,Has3rdQuarterStarted,ForecastWindSpeed,AwayScoreOvertime,Season,SeasonType,ForecastDescription,Has1stQuarterStarted,ForecastWindChill,Date,ForecastTempHigh,IsOvertime,RedZone,Possession,IsInProgress,HomeScoreOvertime,DownAndDistance,HasStarted,AwayScoreQuarter4,AwayScoreQuarter1,AwayScoreQuarter3,AwayScoreQuarter2,AwayTeamMoneyLine,Quarter,IsOver,StadiumID,GeoLat,AwayScore,HomeTeam,LastPlay,LastUpdated,HomeScore,Canceled,HomeTeamMoneyLine,YardLine) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", item.values())
    print "populate score table"

    

if __name__ == "__main__":
#     # drop exsisting tables to repopulate
    conn, c = connect()
    c.execute("drop table if exists schedule")
    c.execute("drop table if exists stadium")
    c.execute("drop table if exists team")
    c.execute("drop table if exists standing")
    c.execute("drop table if exists score")

    create_schedule()
    populate_schedule()

    create_stadium()
    populate_stadium()
    
    create_team()
    populate_team()

    create_standing()
    populate_standing()

    create_score()
    populate_score()

    close()
