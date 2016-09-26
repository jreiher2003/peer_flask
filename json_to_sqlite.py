"""Json to sqlite3 script to dump data into a data base """

import json
import sqlite3
import time

schedule = json.load(open('sports/Schedule.2016.json'))
stadium = json.load(open("sports/Stadium.2016.json"))
team = json.load(open("sports/Team.2016.json"))
standing = json.load(open("sports/Standing.2016.json"))
score = json.load(open("sports/Score.2016.json"))
teamseason = json.load(open("sports/TeamSeason.2016.json"))

def connect():
    """Connect to the sqlite database.  Returns a database connection."""
    conn = sqlite3.connect("app/peer.db")
    c = conn.cursor()
    return conn, c

def close():
    """ commit changes and close db connection """
    conn.commit()
    return conn.close()

###############################################
############## populate schedule ##############
##### create schedule ########################
###############################################
def create_schedule():
    cs = c.execute("""CREATE TABLE IF NOT EXISTS schedule (id INTEGER PRIMARY KEY, Week INTEGER, AwayTeamMoneyLine INTEGER, StadiumID INTEGER, GameKey TEXT, Canceled BOOLEAN, Season INTEGER, HomeTeam TEXT, ForecastWindSpeed INTEGER, OverUnder REAL, GeoLong REAL, ForecastDescription INTEGER, AwayTeam TEXT, ForecastTempLow INTEGER, PointSpread REAL, ForecastWindChill INTEGER, ForecastTempHigh INTEGER, Date TEXT, GeoLat REAL, SeasonType INTEGER, Channel NULL, HomeTeamMoneyLine INTEGER)""")
    print "schedule created"
    return cs

def populate_schedule():
    for item in schedule:
        c.execute("""insert into schedule (Week,AwayTeamMoneyLine,StadiumID,GameKey,Canceled,Season,HomeTeam,ForecastWindSpeed,OverUnder,GeoLong,ForecastDescription,AwayTeam,ForecastTempLow,PointSpread,ForecastWindChill,ForecastTempHigh,Date,GeoLat,SeasonType,Channel,HomeTeamMoneyLine) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", item.values())
    print "populated schedule"


###################################################
########## populate_stadium #######################
######  create_stadium ############################
###################################################
def create_stadium():
    cs = c.execute("""CREATE TABLE IF NOT EXISTS stadium (id INTEGER PRIMARY KEY, StadiumID INTEGER, Name TEXT, City TEXT, State TEXT, Country TEXT, Capacity INTEGER, PlayingSurface TEXT, GeoLat REAL, GeoLong REAL)""")
    print "create stadium"
    return cs 

def populate_stadium():
    columns = list(stadium[0].keys())
    query = "({0}) values ({1})".format(",".join(columns),",?" * len(columns))
    for item in stadium:
        c.execute("""insert into stadium (City,StadiumID,Capacity,Name,PlayingSurface,Country,GeoLong,State,GeoLat) values (?,?,?,?,?,?,?,?,?)""", item.values())
    print "stadium table populated"


###################################################
###### create Team table ##########################
###### populate team ##############################
###################################################
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

###########################################################
############## create standing table ######################
######### populate standing ###############################
###########################################################
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

######################################################
########## create score ##############################
########## populate score table ######################
######################################################
def create_score():
    cs = c.execute("""CREATE TABLE IF NOT EXISTS score (id INTEGER PRIMARY KEY, GameKey TEXT, SeasonType INTEGER, Season INTEGER, Week INTEGER, Date TEXT, AwayTeam TEXT, HomeTeam TEXT, AwayScore INTEGER, HomeScore INTEGER, Channel TEXT, PointSpread REAL, OverUnder REAL, Quarter TEXT, TimeRemaining NULL, Possession NULL, Down NULL, Distance NULL, YardLine NULL, YardLineTerritory NULL, RedZone NULL, AwayScoreQuarter1 INTEGER, AwayScoreQuarter2 INTEGER, AwayScoreQuarter3 INTEGER, AwayScoreQuarter4 INTEGER, AwayScoreOvertime INTEGER, HomeScoreQuarter1 INTEGER, HomeScoreQuarter2 INTEGER, HomeScoreQuarter3 INTEGER, HomeScoreQuarter4 INTEGER,
        HomeScoreOvertime INTEGER, HasStarted BOOLEAN, IsInProgress BOOLEAN, IsOver BOOLEAN, Has1stQuarterStarted BOOLEAN,Has2ndQuarterStarted BOOLEAN, Has3rdQuarterStarted BOOLEAN, Has4thQuarterStarted BOOLEAN, IsOvertime BOOLEAN, DownAndDistance NULL, QuarterDescription TEXT, StadiumID INTEGER, LastUpdated NUMERIC, GeoLat REAL, GeoLong REAL, ForecastTempLow INTEGER, ForecastTempHigh INTEGER, ForecastDescription TEXT, ForecastWindChill INTEGER, ForecastWindSpeed INTEGER, AwayTeamMoneyLine INTEGER, HomeTeamMoneyLine INTEGER, Canceled BOOLEAN, Closed BOOLEAN, LastPlay NULL)""")
    print "create score table"
    return cs
        
def populate_score():
    columns = list(score[0].keys())
    query = "({0}) values ({1})".format(",".join(columns),",?" * len(columns))
    for item in score:
        c.execute("""insert into score (TimeRemaining,HomeScoreQuarter1,HomeScoreQuarter2,HomeScoreQuarter3,HomeScoreQuarter4,Distance,OverUnder,Has4thQuarterStarted,AwayTeam,ForecastTempLow,PointSpread,GeoLong,Closed,QuarterDescription,YardLineTerritory,Channel,Week,Down,Has2ndQuarterStarted,GameKey,Has3rdQuarterStarted,ForecastWindSpeed,AwayScoreOvertime,Season,SeasonType,ForecastDescription,Has1stQuarterStarted,ForecastWindChill,Date,ForecastTempHigh,IsOvertime,RedZone,Possession,IsInProgress,HomeScoreOvertime,DownAndDistance,HasStarted,AwayScoreQuarter4,AwayScoreQuarter1,AwayScoreQuarter3,AwayScoreQuarter2,AwayTeamMoneyLine,Quarter,IsOver,StadiumID,GeoLat,AwayScore,HomeTeam,LastPlay,LastUpdated,HomeScore,Canceled,HomeTeamMoneyLine,YardLine) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", item.values())
    print "populate score table"

#############################################################
############ create teamseason ##############################
############ populate teamseason table ######################
#############################################################
def create_teamseason():
    cts = c.execute("""CREATE TABLE IF NOT EXISTS teamseason (id INTEGER PRIMARY KEY, SeasonType INTEGER, Season INTEGER, Team TEXT, Score INTEGER, OpponentScore INTEGER, TotalScore INTEGER, Temperature INTEGER, Humidity INTEGER, WindSpeed INTEGER, OverUnder REAL, PointSpread REAL, ScoreQuarter1 INTEGER, ScoreQuarter2 INTEGER, ScoreQuarter3 INTEGER, ScoreQuarter4 INTEGER, ScoreOvertime INTEGER, TimeOfPossession TEXT, FirstDowns INTEGER, FirstDownsByRushing INTEGER, FirstDownsByPassing INTEGER, FirstDownsByPenalty INTEGER, OffensivePlays INTEGER, OffensiveYards INTEGER, OffensiveYardsPerPlay NUMERIC, Touchdowns INTEGER, RushingAttempts INTEGER, RushingYards INTEGER, RushingYardsPerAttempt INTEGER, RushingTouchdowns INTEGER, PassingAttempts INTEGER, PassingCompletions INTEGER, PassingYards INTEGER, PassingTouchdowns INTEGER, PassingInterceptions INTEGER,
        PassingYardsPerAttempt NUMERIC, PassingYardsPerCompletion NUMERIC, CompletionPercentage NUMERIC, PasserRating NUMERIC, ThirdDownAttempts INTEGER, ThirdDownConversions INTEGER, ThirdDownPercentage NUMERIC, FourthDownAttempts INTEGER, FourthDownConversions INTEGER, FourthDownPercentage NUMERIC, RedZoneAttempts INTEGER, RedZoneConversions INTEGER, GoalToGoAttempts INTEGER, GoalToGoConversions INTEGER, ReturnYards INTEGER, Penalties INTEGER, PenaltyYards INTEGER, Fumbles INTEGER, FumblesLost INTEGER, TimesSacked INTEGER, TimesSackedYards INTEGER, QuarterbackHits INTEGER, TacklesForLoss INTEGER, Safeties INTEGER, Punts INTEGER, PuntYards INTEGER, PuntAverage NUMERIC, Giveaways INTEGER, Takeaways INTEGER, TurnoverDifferential INTEGER, OpponentScoreQuarter1 INTEGER, OpponentScoreQuarter2 INTEGER, OpponentScoreQuarter3 INTEGER, OpponentScoreQuarter4 INTEGER, OpponentScoreOvertime INTEGER, OpponentTimeOfPossession TEXT, OpponentFirstDowns INTEGER, OpponentFirstDownsByRushing INTEGER, OpponentFirstDownsByPassing INTEGER, OpponentFirstDownsByPenalty INTEGER, OpponentOffensivePlays INTEGER, OpponentOffensiveYards INTEGER, OpponentOffensiveYardsPerPlay NUMERIC, OpponentTouchdowns INTEGER, OpponentRushingAttempts INTEGER, OpponentRushingYards INTEGER, OpponentRushingYardsPerAttempt NUMERIC, OpponentRushingTouchdowns INTEGER, OpponentPassingAttempts INTEGER, OpponentPassingCompletions INTEGER, OpponentPassingYards INTEGER, OpponentPassingTouchdowns INTEGER, OpponentPassingInterceptions INTEGER, OpponentPassingYardsPerAttempt NUMERIC, OpponentPassingYardsPerCompletion NUMERIC, OpponentCompletionPercentage INTEGER, OpponentPasserRating NUMERIC, OpponentThirdDownAttempts INTEGER, OpponentThirdDownConversions INTEGER, OpponentThirdDownPercentage NUMERIC, OpponentFourthDownAttempts INTEGER, OpponentFourthDownConversions INTEGER, OpponentFourthDownPercentage NUMERIC, OpponentRedZoneAttempts INTEGER, OpponentRedZoneConversions INTEGER, OpponentGoalToGoAttempts INTEGER, OpponentGoalToGoConversions INTEGER, OpponentReturnYards INTEGER, OpponentPenalties INTEGER, OpponentPenaltyYards INTEGER, OpponentFumbles INTEGER, OpponentFumblesLost INTEGER, OpponentTimesSacked INTEGER, OpponentTimesSackedYards INTEGER, OpponentQuarterbackHits INTEGER, OpponentTacklesForLoss INTEGER, OpponentSafeties INTEGER, OpponentPunts INTEGER, OpponentPuntYards INTEGER, OpponentPuntAverage NUMERIC, OpponentGiveaways INTEGER, OpponentTakeaways INTEGER, OpponentTurnoverDifferential INTEGER, RedZonePercentage NUMERIC, GoalToGoPercentage NUMERIC, QuarterbackHitsDifferential INTEGER, TacklesForLossDifferential INTEGER, QuarterbackSacksDifferential INTEGER, TacklesForLossPercentage NUMERIC, QuarterbackHitsPercentage NUMERIC, TimesSackedPercentage NUMERIC, OpponentRedZonePercentage NUMERIC, OpponentGoalToGoPercentage NUMERIC, OpponentQuarterbackHitsDifferential INTEGER,
            OpponentTacklesForLossDifferential INTEGER, OpponentQuarterbackSacksDifferential INTEGER, OpponentTacklesForLossPercentage NUMERIC, OpponentQuarterbackHitsPercentage NUMERIC, OpponentTimesSackedPercentage NUMERIC, Kickoffs INTEGER, KickoffsInEndZone INTEGER, KickoffTouchbacks INTEGER, PuntsHadBlocked INTEGER, PuntNetAverage NUMERIC, ExtraPointKickingAttempts INTEGER, ExtraPointKickingConversions INTEGER, ExtraPointsHadBlocked INTEGER, ExtraPointPassingAttempts INTEGER, ExtraPointPassingConversions INTEGER, ExtraPointRushingAttempts INTEGER, ExtraPointRushingConversions INTEGER, FieldGoalAttempts INTEGER, FieldGoalsMade INTEGER, FieldGoalsHadBlocked INTEGER, PuntReturns INTEGER, PuntReturnYards INTEGER, KickReturns INTEGER, KickReturnYards INTEGER, InterceptionReturns INTEGER, InterceptionReturnYards INTEGER, OpponentKickoffs INTEGER, OpponentKickoffsInEndZone INTEGER, OpponentKickoffTouchbacks INTEGER, OpponentPuntsHadBlocked INTEGER, OpponentPuntNetAverage INTEGER, OpponentExtraPointKickingAttempts INTEGER, OpponentExtraPointKickingConversions INTEGER, OpponentExtraPointsHadBlocked INTEGER, OpponentExtraPointPassingAttempts INTEGER, OpponentExtraPointPassingConversions INTEGER, 
                OpponentExtraPointRushingAttempts INTEGER, OpponentExtraPointRushingConversions INTEGER, OpponentFieldGoalAttempts INTEGER, OpponentFieldGoalsMade INTEGER, OpponentFieldGoalsHadBlocked INTEGER, OpponentPuntReturns INTEGER, OpponentPuntReturnYards INTEGER, OpponentKickReturns INTEGER, OpponentKickReturnYards INTEGER, OpponentInterceptionReturns INTEGER, OpponentInterceptionReturnYards INTEGER, SoloTackles INTEGER, AssistedTackles INTEGER, Sacks INTEGER, SackYards INTEGER, PassesDefended INTEGER, FumblesForced INTEGER, FumblesRecovered INTEGER, FumbleReturnYards INTEGER, FumbleReturnTouchdowns INTEGER, InterceptionReturnTouchdowns INTEGER, BlockedKicks INTEGER, PuntReturnTouchdowns INTEGER, PuntReturnLong INTEGER, KickReturnTouchdowns INTEGER, KickReturnLong INTEGER, BlockedKickReturnYards INTEGER, BlockedKickReturnTouchdowns INTEGER, FieldGoalReturnYards INTEGER, FieldGoalReturnTouchdowns INTEGER, PuntNetYards INTEGER, OpponentSoloTackles INTEGER, OpponentAssistedTackles INTEGER, OpponentSacks INTEGER, OpponentSackYards INTEGER, OpponentPassesDefended INTEGER, OpponentFumblesForced INTEGER, OpponentFumblesRecovered INTEGER, OpponentFumbleReturnYards INTEGER, OpponentFumbleReturnTouchdowns INTEGER, OpponentInterceptionReturnTouchdowns INTEGER, OpponentBlockedKicks INTEGER, OpponentPuntReturnTouchdowns INTEGER, OpponentPuntReturnLong INTEGER, OpponentKickReturnTouchdowns INTEGER, OpponentKickReturnLong INTEGER, OpponentBlockedKickReturnYards INTEGER, OpponentBlockedKickReturnTouchdowns INTEGER, OpponentFieldGoalReturnYards INTEGER, OpponentFieldGoalReturnTouchdowns INTEGER, OpponentPuntNetYards INTEGER, TeamName TEXT, Games INTEGER, PassingDropbacks INTEGER, OpponentPassingDropbacks INTEGER, TeamSeasonID INTEGER, PointDifferential INTEGER, PassingInterceptionPercentage NUMERIC, PuntReturnAverage NUMERIC, KickReturnAverage NUMERIC, ExtraPointPercentage NUMERIC, FieldGoalPercentage NUMERIC, OpponentPassingInterceptionPercentage NUMERIC, OpponentPuntReturnAverage NUMERIC, OpponentKickReturnAverage NUMERIC, OpponentExtraPointPercentage NUMERIC, OpponentFieldGoalPercentage NUMERIC, PenaltyYardDifferential INTEGER, PuntReturnYardDifferential INTEGER, KickReturnYardDifferential INTEGER, TwoPointConversionReturns INTEGER, OpponentTwoPointConversionReturns INTEGER)""")
    print "create teamseason table"
    return cts

def populate_teamseason():
    columns = list(teamseason[0].keys())
    query = "({0}) values ({1})".format(",".join(columns),",?" * len(columns))
    # print query
    for item in teamseason:
        c.execute("""insert into teamseason (OpponentPuntReturnLong,RushingTouchdowns,OpponentSafeties,OpponentQuarterbackHitsDifferential,FieldGoalPercentage,WindSpeed,ExtraPointRushingConversions,OpponentPuntYards,FumblesLost,OpponentExtraPointsHadBlocked,PuntNetAverage,ExtraPointKickingConversions,PointDifferential,OpponentPassingYardsPerCompletion,PassingInterceptions,OpponentPuntReturns,PassingYards,OpponentGoalToGoConversions,OpponentFourthDownConversions,OpponentPassingInterceptionPercentage,GoalToGoPercentage,BlockedKicks,ReturnYards,OpponentKickReturnLong,OpponentFieldGoalsHadBlocked,OpponentSackYards,CompletionPercentage,Fumbles,ThirdDownAttempts,OpponentPunts,RedZoneConversions,OpponentKickReturnYards,PassesDefended,OpponentTimesSacked,TeamName,OpponentThirdDownPercentage,Penalties,OpponentFieldGoalAttempts,Safeties,OpponentRedZoneConversions,OpponentBlockedKickReturnYards,OpponentPenaltyYards,OpponentThirdDownAttempts,OpponentBlockedKickReturnTouchdowns,Touchdowns,TimesSackedPercentage,FirstDowns,Kickoffs,OpponentTurnoverDifferential,InterceptionReturns,TimesSacked,ExtraPointPassingConversions,PenaltyYards,QuarterbackHitsDifferential,PassingInterceptionPercentage,ScoreQuarter4,ScoreQuarter3,ScoreQuarter2,OpponentRushingTouchdowns,OpponentPassingInterceptions,OpponentGoalToGoAttempts,OpponentFourthDownAttempts,RedZonePercentage,RushingAttempts,Season,PuntReturns,FieldGoalReturnYards,OpponentReturnYards,GoalToGoConversions,OpponentFirstDownsByRushing,Punts,FumbleReturnTouchdowns,TotalScore,OpponentPassingAttempts,TurnoverDifferential,PuntReturnTouchdowns,OpponentFumblesLost,OpponentExtraPointKickingAttempts,PuntYards,OpponentTacklesForLossPercentage,Team,KickReturnYards,ExtraPointsHadBlocked,FumblesRecovered,TacklesForLoss,OpponentTimesSackedYards,OpponentAssistedTackles,OpponentFourthDownPercentage,OpponentSoloTackles,BlockedKickReturnTouchdowns,ExtraPointPercentage,ExtraPointKickingAttempts,OpponentQuarterbackSacksDifferential,FieldGoalsHadBlocked,OpponentFieldGoalReturnTouchdowns,FieldGoalReturnTouchdowns,PassingYardsPerAttempt,OpponentKickReturnTouchdowns,OpponentExtraPointRushingAttempts,OpponentExtraPointKickingConversions,KickReturnYardDifferential,KickReturnLong,KickReturnAverage,Temperature,PassingYardsPerCompletion,OpponentTimesSackedPercentage,OpponentPuntAverage,RushingYardsPerAttempt,QuarterbackHits,OverUnder,PassingDropbacks,KickReturns,OpponentQuarterbackHits,OpponentFirstDownsByPenalty,OpponentExtraPointPercentage,PuntsHadBlocked,OpponentCompletionPercentage,OpponentRushingAttempts,SeasonType,TwoPointConversionReturns,OpponentInterceptionReturnTouchdowns,OffensiveYards,PuntAverage,RushingYards,ExtraPointPassingAttempts,PuntNetYards,PassingCompletions,OpponentFumbles,TacklesForLossDifferential,KickReturnTouchdowns,OpponentPuntReturnAverage,PuntReturnAverage,TacklesForLossPercentage,FourthDownConversions,OpponentRedZoneAttempts,OpponentBlockedKicks,OpponentQuarterbackHitsPercentage,OpponentKickReturns,TeamSeasonID,OpponentPassingDropbacks,OpponentKickoffTouchbacks,OpponentGoalToGoPercentage,OpponentFumblesForced,PuntReturnLong,OpponentRushingYards,OpponentKickoffs,OpponentTouchdowns,OpponentTakeaways,FirstDownsByRushing,OpponentThirdDownConversions,OpponentInterceptionReturnYards,OpponentRushingYardsPerAttempt,OpponentKickoffsInEndZone,OpponentOffensiveYardsPerPlay,OpponentPuntNetYards,OpponentExtraPointRushingConversions,KickoffTouchbacks,FieldGoalsMade,InterceptionReturnTouchdowns,OpponentPassingCompletions,OpponentPassingTouchdowns,GoalToGoAttempts,OpponentPassesDefended,OpponentTimeOfPossession,PuntReturnYards,PassingTouchdowns,FieldGoalAttempts,OpponentTacklesForLossDifferential,OpponentFieldGoalPercentage,FumblesForced,OpponentPasserRating,OpponentScoreQuarter2,OpponentScoreQuarter3,OpponentScoreQuarter1,FirstDownsByPenalty,TimesSackedYards,OpponentScoreQuarter4,ExtraPointRushingAttempts,AssistedTackles,Giveaways,OpponentExtraPointPassingConversions,FourthDownPercentage,Score,PointSpread,OpponentScoreOvertime,FirstDownsByPassing,TimeOfPossession,ThirdDownPercentage,OpponentExtraPointPassingAttempts,OpponentPuntsHadBlocked,OpponentPassingYardsPerAttempt,InterceptionReturnYards,Takeaways,OffensivePlays,OpponentFirstDownsByPassing,ScoreQuarter1,PuntReturnYardDifferential,OpponentKickReturnAverage,OpponentPuntReturnTouchdowns,OpponentInterceptionReturns,ThirdDownConversions,PenaltyYardDifferential,OpponentFumbleReturnTouchdowns,QuarterbackSacksDifferential,Sacks,FumbleReturnYards,OpponentPenalties,OpponentGiveaways,OpponentTwoPointConversionReturns,ScoreOvertime,Humidity,SackYards,RedZoneAttempts,Games,PasserRating,OpponentPassingYards,OpponentPuntNetAverage,OpponentSacks,OpponentFumblesRecovered,OpponentOffensivePlays,OffensiveYardsPerPlay,OpponentTacklesForLoss,SoloTackles,OpponentRedZonePercentage,PassingAttempts,OpponentFumbleReturnYards,OpponentScore,KickoffsInEndZone,OpponentPuntReturnYards,OpponentFirstDowns,OpponentFieldGoalsMade,FourthDownAttempts,OpponentFieldGoalReturnYards,OpponentOffensiveYards,QuarterbackHitsPercentage,BlockedKickReturnYards) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", item.values())
    print "team season populated"

if __name__ == "__main__":
#     # drop exsisting tables to repopulate
    conn, c = connect()
    c.execute("drop table if exists schedule")
    c.execute("drop table if exists stadium")
    c.execute("drop table if exists team")
    c.execute("drop table if exists standing")
    c.execute("drop table if exists score")
    c.execute("drop table if exists teamseason")

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

    create_teamseason()
    populate_teamseason()

    close()
