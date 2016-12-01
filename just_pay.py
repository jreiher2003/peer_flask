"""Json to postgres script to dump data and update data into a data base 
m      h       dom             mon     dow          command
Minute Hour    Day of Month    Month   Day of week  <command>
0 * * * * will execute every minute of every day all the time 
crontab -e crontab file 
min
crontab -l list all cron jobs
var/log/syslog -- sudo grep CRON syslog  look at all cronjobs 
"""
import os
import pwd
import grp
import json
import psycopg2
import time
import urllib
import urllib2
import zipfile 
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.parser import parse as parse_date
from app import app, db, cache
from sqlalchemy import exc
from app.users.models import Users, Role, UserRoles, Profile, BitcoinWallet
from app.nfl.models import NFLBetGraded, NFLOverUnderBet, NFLSideBet, NFLMLBet, Base
from app.nfl_stats.models import NFLScore, NFLTeam, NFLStadium, NFLSchedule, NFLStandings, NFLTeamSeason
from app.home.utils import kitchen_sink


def download():
    sports = urllib.URLopener()
    sports.retrieve(os.environ["FD_URL"], "file.zip")
    if os.environ["APP_SETTINGS"] == "config.DevelopmentConfig":
        print "Development download starting now..."
        root = os.getcwd()
        path = root + "/file.zip"
        print path
        zipfile.ZipFile("file.zip").extractall("sports")
        os.remove("file.zip")
    elif os.environ["APP_SETTINGS"] == "config.ProductionConfig":
        print "Production Download starting now..."
        zipfile.ZipFile("file.zip").extractall("sports")
        os.remove("file.zip")
###############################################
############## populate schedule ##############
##### create schedule ########################
###############################################
def create_roles():
    role1 = Role(id=1,name="admin", description="Admin of site")
    role2 = Role(id=2,name="player", description="basic user of site")
    role3 = Role(id=3,name="bookie", description="More privileges then basic user")
    db.session.add_all([role1,role2,role3])
    db.session.commit() 
    print "create roles table"

def populate_schedule():
    NFLSchedule.__table__.drop(db.engine)
    NFLSchedule.__table__.create(db.engine)
    for i in schedule:
        nn = NFLSchedule(Week=i["Week"],AwayTeamMoneyLine=i["AwayTeamMoneyLine"],StadiumID=i["StadiumID"],GameKey=i["GameKey"],Canceled=i["Canceled"],Season=i["Season"],HomeTeam=i["HomeTeam"],ForecastWindSpeed=i["ForecastWindSpeed"],OverUnder=i["OverUnder"],GeoLong=i["GeoLong"],ForecastDescription=i["ForecastDescription"],AwayTeam=i["AwayTeam"],ForecastTempLow=i["ForecastTempLow"],PointSpread=i["PointSpread"],ForecastWindChill=i["ForecastWindChill"],ForecastTempHigh=i["ForecastTempHigh"],Date=i["Date"],GeoLat=i["GeoLat"],SeasonType=i["SeasonType"],Channel=i["Channel"],HomeTeamMoneyLine=i["HomeTeamMoneyLine"])
        db.session.add(nn)
        db.session.commit()
    print "populated schedule"
###################################################
########## populate_stadium #######################
######  create_stadium ############################
###################################################
def populate_stadium():
    NFLStadium.__table__.drop(db.engine)
    NFLStadium.__table__.create(db.engine)
    for i in stadium:
        st = NFLStadium(City=i["City"],StadiumID=i["StadiumID"],Capacity=i["Capacity"],Name=i["Name"],PlayingSurface=i["PlayingSurface"],Country=i["Country"],GeoLong=i["GeoLong"],State=i["State"],GeoLat=i["GeoLat"])
        db.session.add(st)
        db.session.commit()
    print "stadium table populated"
###################################################
###### create Team table ##########################
###### populate team ##############################
###################################################
def populate_team():
    NFLTeam.__table__.drop(db.engine)
    NFLTeam.__table__.create(db.engine)
    for i in team:
        t = NFLTeam(Conference=i["Conference"],City=i["City"],WikipediaLogoUrl=i["WikipediaLogoUrl"],DefensiveScheme=i["DefensiveScheme"],PlayerID=i["PlayerID"],ByeWeek=i["ByeWeek"],UpcomingSalary=i["UpcomingSalary"],SecondaryColor=i["SecondaryColor"],UpcomingOpponentRank=i["UpcomingOpponentRank"],UpcomingYahooSalary=i["UpcomingYahooSalary"],QuaternaryColor=i["QuaternaryColor"],Division=i["Division"],UpcomingDraftKingsSalary=i["UpcomingDraftKingsSalary"],DefensiveCoordinator=i["DefensiveCoordinator"],AverageDraftPositionPPR=i["AverageDraftPositionPPR"],Key=i["Key"],SpecialTeamsCoach=i["SpecialTeamsCoach"],Name=i["Name"],UpcomingOpponent=i["UpcomingOpponent"],TertiaryColor=i["TertiaryColor"],AverageDraftPosition=i["AverageDraftPosition"],UpcomingOpponentPositionRank=i["UpcomingOpponentPositionRank"],StadiumID=i["StadiumID"],OffensiveCoordinator=i["OffensiveCoordinator"],OffensiveScheme=i["OffensiveScheme"],TeamID=i["TeamID"],UpcomingFanDuelSalary=i["UpcomingFanDuelSalary"],HeadCoach=i["HeadCoach"],PrimaryColor=i["PrimaryColor"],WikipediaWordMarkUrl=i["WikipediaWordMarkUrl"],FullName=i["FullName"])
        db.session.add(t)
        db.session.commit()
    print "populate team table"
###########################################################
############## create standing table ######################
######### populate standing ###############################
###########################################################
def populate_standing():
    NFLStandings.__table__.drop(db.engine)
    NFLStandings.__table__.create(db.engine)
    for i in standing:
        tt = NFLStandings(Conference=i["Conference"],Division=i["Division"],PointsAgainst=i["PointsAgainst"],NetPoints=i["NetPoints"],Name=i["Name"],Wins=i["Wins"],Season=i["Season"],Touchdowns=i["Touchdowns"],Losses=i["Losses"],PointsFor=i["PointsFor"],ConferenceWins=i["ConferenceWins"],DivisionLosses=i["DivisionLosses"],Team=i["Team"],Ties=i["Ties"],Percentage=i["Percentage"],DivisionWins=i["DivisionWins"],SeasonType=i["SeasonType"],ConferenceLosses=i["ConferenceLosses"])
        db.session.add(tt)
        db.session.commit()
    print "populate standing table"
######################################################
########## create score ##############################
########## populate score table ######################
######################################################
def populate_score():
    NFLScore.__table__.drop(db.engine)
    NFLScore.__table__.create(db.engine)
    for i in score:
        tt = NFLScore(TimeRemaining=i["TimeRemaining"],HomeScoreQuarter1=i["HomeScoreQuarter1"],HomeScoreQuarter2=i["HomeScoreQuarter2"],HomeScoreQuarter3=i["HomeScoreQuarter3"],HomeScoreQuarter4=i["HomeScoreQuarter4"],Distance=i["Distance"],OverUnder=i["OverUnder"],Has4thQuarterStarted=i["Has4thQuarterStarted"],AwayTeam=i["AwayTeam"],ForecastTempLow=i["ForecastTempLow"],PointSpread=i["PointSpread"],GeoLong=i["GeoLong"],Closed=i["Closed"],QuarterDescription=i["QuarterDescription"],YardLineTerritory=i["YardLineTerritory"],Channel=i["Channel"],Week=i["Week"],Down=i["Down"],Has2ndQuarterStarted=i["Has2ndQuarterStarted"],GameKey=i["GameKey"],Has3rdQuarterStarted=i["Has3rdQuarterStarted"],ForecastWindSpeed=i["ForecastWindSpeed"],AwayScoreOvertime=i["AwayScoreOvertime"],Season=i["Season"],SeasonType=i["SeasonType"],ForecastDescription=i["ForecastDescription"],Has1stQuarterStarted=i["Has1stQuarterStarted"],ForecastWindChill=i["ForecastWindChill"],Date=i["Date"],ForecastTempHigh=i["ForecastTempHigh"],IsOvertime=i["IsOvertime"],RedZone=i["RedZone"],Possession=i["Possession"],IsInProgress=i["IsInProgress"],HomeScoreOvertime=i["HomeScoreOvertime"],DownAndDistance=i["DownAndDistance"],HasStarted=i["HasStarted"],AwayScoreQuarter4=i["AwayScoreQuarter4"],AwayScoreQuarter1=i["AwayScoreQuarter1"],AwayScoreQuarter3=i["AwayScoreQuarter3"],AwayScoreQuarter2=i["AwayScoreQuarter2"],AwayTeamMoneyLine=i["AwayTeamMoneyLine"],Quarter=i["Quarter"],IsOver=i["IsOver"],StadiumID=i["StadiumID"],GeoLat=i["GeoLat"],AwayScore=i["AwayScore"],HomeTeam=i["HomeTeam"],LastPlay=i["LastPlay"],LastUpdated=i["LastUpdated"],HomeScore=i["HomeScore"],Canceled=i["Canceled"],HomeTeamMoneyLine=i["HomeTeamMoneyLine"],YardLine=i["YardLine"])
        db.session.add(tt)
        db.session.commit()
    print "populate score table"

#############################################################
############ create teamseason ##############################
############ populate teamseason table ######################
#############################################################
def populate_teamseason():
    NFLTeamSeason.__table__.drop(db.engine)
    NFLTeamSeason.__table__.create(db.engine)
    for i in teamseason:
        dd = NFLTeamSeason(OpponentPuntReturnLong=i["OpponentPuntReturnLong"],RushingTouchdowns=i["RushingTouchdowns"],OpponentSafeties=i["OpponentSafeties"],OpponentQuarterbackHitsDifferential=i["OpponentQuarterbackHitsDifferential"],FieldGoalPercentage=i["FieldGoalPercentage"],WindSpeed=i["WindSpeed"],ExtraPointRushingConversions=i["ExtraPointRushingConversions"],OpponentPuntYards=i["OpponentPuntYards"],FumblesLost=i["FumblesLost"],OpponentExtraPointsHadBlocked=i["OpponentExtraPointsHadBlocked"],PuntNetAverage=i["PuntNetAverage"],ExtraPointKickingConversions=i["ExtraPointKickingConversions"],PointDifferential=i["PointDifferential"],OpponentPassingYardsPerCompletion=i["OpponentPassingYardsPerCompletion"],PassingInterceptions=i["PassingInterceptions"],OpponentPuntReturns=i["OpponentPuntReturns"],PassingYards=i["PassingYards"],OpponentGoalToGoConversions=i["OpponentGoalToGoConversions"],OpponentFourthDownConversions=i["OpponentFourthDownConversions"],OpponentPassingInterceptionPercentage=i["OpponentPassingInterceptionPercentage"],GoalToGoPercentage=i["GoalToGoPercentage"],BlockedKicks=i["BlockedKicks"],ReturnYards=i["ReturnYards"],OpponentKickReturnLong=i["OpponentKickReturnLong"],OpponentFieldGoalsHadBlocked=i["OpponentFieldGoalsHadBlocked"],OpponentSackYards=i["OpponentSackYards"],CompletionPercentage=i["CompletionPercentage"],Fumbles=i["Fumbles"],ThirdDownAttempts=i["ThirdDownAttempts"],OpponentPunts=i["OpponentPunts"],RedZoneConversions=i["RedZoneConversions"],OpponentKickReturnYards=i["OpponentKickReturnYards"],PassesDefended=i["PassesDefended"],OpponentTimesSacked=i["OpponentTimesSacked"],TeamName=i["TeamName"],OpponentThirdDownPercentage=i["OpponentThirdDownPercentage"],Penalties=i["Penalties"],OpponentFieldGoalAttempts=i["OpponentFieldGoalAttempts"],Safeties=i["Safeties"],OpponentRedZoneConversions=i["OpponentRedZoneConversions"],OpponentBlockedKickReturnYards=i["OpponentBlockedKickReturnYards"],OpponentPenaltyYards=i["OpponentPenaltyYards"],OpponentThirdDownAttempts=i["OpponentThirdDownAttempts"],OpponentBlockedKickReturnTouchdowns=i["OpponentBlockedKickReturnTouchdowns"],Touchdowns=i["Touchdowns"],TimesSackedPercentage=i["TimesSackedPercentage"],FirstDowns=i["FirstDowns"],Kickoffs=i["Kickoffs"],OpponentTurnoverDifferential=i["OpponentTurnoverDifferential"],InterceptionReturns=i["InterceptionReturns"],TimesSacked=i["TimesSacked"],ExtraPointPassingConversions=i["ExtraPointPassingConversions"],PenaltyYards=i["PenaltyYards"],QuarterbackHitsDifferential=i["QuarterbackHitsDifferential"],PassingInterceptionPercentage=i["PassingInterceptionPercentage"],ScoreQuarter4=i["ScoreQuarter4"],ScoreQuarter3=i["ScoreQuarter3"],ScoreQuarter2=i["ScoreQuarter2"],OpponentRushingTouchdowns=i["OpponentRushingTouchdowns"],OpponentPassingInterceptions=i["OpponentPassingInterceptions"],OpponentGoalToGoAttempts=i["OpponentGoalToGoAttempts"],OpponentFourthDownAttempts=i["OpponentFourthDownAttempts"],RedZonePercentage=i["RedZonePercentage"],RushingAttempts=i["RushingAttempts"],Season=i["Season"],PuntReturns=i["PuntReturns"],FieldGoalReturnYards=i["FieldGoalReturnYards"],OpponentReturnYards=i["OpponentReturnYards"],GoalToGoConversions=i["GoalToGoConversions"],OpponentFirstDownsByRushing=i["OpponentFirstDownsByRushing"],Punts=i["Punts"],FumbleReturnTouchdowns=i["FumbleReturnTouchdowns"],TotalScore=i["TotalScore"],OpponentPassingAttempts=i["OpponentPassingAttempts"],TurnoverDifferential=i["TurnoverDifferential"],PuntReturnTouchdowns=i["PuntReturnTouchdowns"],OpponentFumblesLost=i["OpponentFumblesLost"],OpponentExtraPointKickingAttempts=i["OpponentExtraPointKickingAttempts"],PuntYards=i["PuntYards"],OpponentTacklesForLossPercentage=i["OpponentTacklesForLossPercentage"],Team=i["Team"],KickReturnYards=i["KickReturnYards"],ExtraPointsHadBlocked=i["ExtraPointsHadBlocked"],FumblesRecovered=i["FumblesRecovered"],TacklesForLoss=i["TacklesForLoss"],OpponentTimesSackedYards=i["OpponentTimesSackedYards"],OpponentAssistedTackles=i["OpponentAssistedTackles"],OpponentFourthDownPercentage=i["OpponentFourthDownPercentage"],OpponentSoloTackles=i["OpponentSoloTackles"],BlockedKickReturnTouchdowns=i["BlockedKickReturnTouchdowns"],ExtraPointPercentage=i["ExtraPointPercentage"],ExtraPointKickingAttempts=i["ExtraPointKickingAttempts"],OpponentQuarterbackSacksDifferential=i["OpponentQuarterbackSacksDifferential"],FieldGoalsHadBlocked=i["FieldGoalsHadBlocked"],OpponentFieldGoalReturnTouchdowns=i["OpponentFieldGoalReturnTouchdowns"],FieldGoalReturnTouchdowns=i["FieldGoalReturnTouchdowns"],PassingYardsPerAttempt=i["PassingYardsPerAttempt"],OpponentKickReturnTouchdowns=i["OpponentKickReturnTouchdowns"],OpponentExtraPointRushingAttempts=i["OpponentExtraPointRushingAttempts"],OpponentExtraPointKickingConversions=i["OpponentExtraPointKickingConversions"],KickReturnYardDifferential=i["KickReturnYardDifferential"],KickReturnLong=i["KickReturnLong"],KickReturnAverage=i["KickReturnAverage"],Temperature=i["Temperature"],PassingYardsPerCompletion=i["PassingYardsPerCompletion"],OpponentTimesSackedPercentage=i["OpponentTimesSackedPercentage"],OpponentPuntAverage=i["OpponentPuntAverage"],RushingYardsPerAttempt=i["RushingYardsPerAttempt"],QuarterbackHits=i["QuarterbackHits"],OverUnder=i["OverUnder"],PassingDropbacks=i["PassingDropbacks"],KickReturns=i["KickReturns"],OpponentQuarterbackHits=i["OpponentQuarterbackHits"],OpponentFirstDownsByPenalty=i["OpponentFirstDownsByPenalty"],OpponentExtraPointPercentage=i["OpponentExtraPointPercentage"],PuntsHadBlocked=i["PuntsHadBlocked"],OpponentCompletionPercentage=i["OpponentCompletionPercentage"],OpponentRushingAttempts=i["OpponentRushingAttempts"],SeasonType=i["SeasonType"],TwoPointConversionReturns=i["TwoPointConversionReturns"],OpponentInterceptionReturnTouchdowns=i["OpponentInterceptionReturnTouchdowns"],OffensiveYards=i["OffensiveYards"],PuntAverage=i["PuntAverage"],RushingYards=i["RushingYards"],ExtraPointPassingAttempts=i["ExtraPointPassingAttempts"],PuntNetYards=i["PuntNetYards"],PassingCompletions=i["PassingCompletions"],OpponentFumbles=i["OpponentFumbles"],TacklesForLossDifferential=i["TacklesForLossDifferential"],KickReturnTouchdowns=i["KickReturnTouchdowns"],OpponentPuntReturnAverage=i["OpponentPuntReturnAverage"],PuntReturnAverage=i["PuntReturnAverage"],TacklesForLossPercentage=i["TacklesForLossPercentage"],FourthDownConversions=i["FourthDownConversions"],OpponentRedZoneAttempts=i["OpponentRedZoneAttempts"],OpponentBlockedKicks=i["OpponentBlockedKicks"],OpponentQuarterbackHitsPercentage=i["OpponentQuarterbackHitsPercentage"],OpponentKickReturns=i["OpponentKickReturns"],TeamSeasonID=i["TeamSeasonID"],OpponentPassingDropbacks=i["OpponentPassingDropbacks"],OpponentKickoffTouchbacks=i["OpponentKickoffTouchbacks"],OpponentGoalToGoPercentage=i["OpponentGoalToGoPercentage"],OpponentFumblesForced=i["OpponentFumblesForced"],PuntReturnLong=i["PuntReturnLong"],OpponentRushingYards=i["OpponentRushingYards"],OpponentKickoffs=i["OpponentKickoffs"],OpponentTouchdowns=i["OpponentTouchdowns"],OpponentTakeaways=i["OpponentTakeaways"],FirstDownsByRushing=i["FirstDownsByRushing"],OpponentThirdDownConversions=i["OpponentThirdDownConversions"],OpponentInterceptionReturnYards=i["OpponentInterceptionReturnYards"],OpponentRushingYardsPerAttempt=i["OpponentRushingYardsPerAttempt"],OpponentKickoffsInEndZone=i["OpponentKickoffsInEndZone"],OpponentOffensiveYardsPerPlay=i["OpponentOffensiveYardsPerPlay"],OpponentPuntNetYards=i["OpponentPuntNetYards"],OpponentExtraPointRushingConversions=i["OpponentExtraPointRushingConversions"],KickoffTouchbacks=i["KickoffTouchbacks"],FieldGoalsMade=i["FieldGoalsMade"],InterceptionReturnTouchdowns=i["InterceptionReturnTouchdowns"],OpponentPassingCompletions=i["OpponentPassingCompletions"],OpponentPassingTouchdowns=i["OpponentPassingTouchdowns"],GoalToGoAttempts=i["GoalToGoAttempts"],OpponentPassesDefended=i["OpponentPassesDefended"],OpponentTimeOfPossession=i["OpponentTimeOfPossession"],PuntReturnYards=i["PuntReturnYards"],PassingTouchdowns=i["PassingTouchdowns"],FieldGoalAttempts=i["FieldGoalAttempts"],OpponentTacklesForLossDifferential=i["OpponentTacklesForLossDifferential"],OpponentFieldGoalPercentage=i["OpponentFieldGoalPercentage"],FumblesForced=i["FumblesForced"],OpponentPasserRating=i["OpponentPasserRating"],OpponentScoreQuarter2=i["OpponentScoreQuarter2"],OpponentScoreQuarter3=i["OpponentScoreQuarter3"],OpponentScoreQuarter1=i["OpponentScoreQuarter1"],FirstDownsByPenalty=i["FirstDownsByPenalty"],TimesSackedYards=i["TimesSackedYards"],OpponentScoreQuarter4=i["OpponentScoreQuarter4"],ExtraPointRushingAttempts=i["ExtraPointRushingAttempts"],AssistedTackles=i["AssistedTackles"],Giveaways=i["Giveaways"],OpponentExtraPointPassingConversions=i["OpponentExtraPointPassingConversions"],FourthDownPercentage=i["FourthDownPercentage"],Score=i["Score"],PointSpread=i["PointSpread"],OpponentScoreOvertime=i["OpponentScoreOvertime"],FirstDownsByPassing=i["FirstDownsByPassing"],TimeOfPossession=i["TimeOfPossession"],ThirdDownPercentage=i["ThirdDownPercentage"],OpponentExtraPointPassingAttempts=i["OpponentExtraPointPassingAttempts"],OpponentPuntsHadBlocked=i["OpponentPuntsHadBlocked"],OpponentPassingYardsPerAttempt=i["OpponentPassingYardsPerAttempt"],InterceptionReturnYards=i["InterceptionReturnYards"],Takeaways=i["Takeaways"],OffensivePlays=i["OffensivePlays"],OpponentFirstDownsByPassing=i["OpponentFirstDownsByPassing"],ScoreQuarter1=i["ScoreQuarter1"],PuntReturnYardDifferential=i["PuntReturnYardDifferential"],OpponentKickReturnAverage=i["OpponentKickReturnAverage"],OpponentPuntReturnTouchdowns=i["OpponentPuntReturnTouchdowns"],OpponentInterceptionReturns=i["OpponentInterceptionReturns"],ThirdDownConversions=i["ThirdDownConversions"],PenaltyYardDifferential=i["PenaltyYardDifferential"],OpponentFumbleReturnTouchdowns=i["OpponentFumbleReturnTouchdowns"],QuarterbackSacksDifferential=i["QuarterbackSacksDifferential"],Sacks=i["Sacks"],FumbleReturnYards=i["FumbleReturnYards"],OpponentPenalties=i["OpponentPenalties"],OpponentGiveaways=i["OpponentGiveaways"],OpponentTwoPointConversionReturns=i["OpponentTwoPointConversionReturns"],ScoreOvertime=i["ScoreOvertime"],Humidity=i["Humidity"],SackYards=i["SackYards"],RedZoneAttempts=i["RedZoneAttempts"],Games=i["Games"],PasserRating=i["PasserRating"],OpponentPassingYards=i["OpponentPassingYards"],OpponentPuntNetAverage=i["OpponentPuntNetAverage"],OpponentSacks=i["OpponentSacks"],OpponentFumblesRecovered=i["OpponentFumblesRecovered"],OpponentOffensivePlays=i["OpponentOffensivePlays"],OffensiveYardsPerPlay=i["OffensiveYardsPerPlay"],OpponentTacklesForLoss=i["OpponentTacklesForLoss"],SoloTackles=i["SoloTackles"],OpponentRedZonePercentage=i["OpponentRedZonePercentage"],PassingAttempts=i["PassingAttempts"],OpponentFumbleReturnYards=i["OpponentFumbleReturnYards"],OpponentScore=i["OpponentScore"],KickoffsInEndZone=i["KickoffsInEndZone"],OpponentPuntReturnYards=i["OpponentPuntReturnYards"],OpponentFirstDowns=i["OpponentFirstDowns"],OpponentFieldGoalsMade=i["OpponentFieldGoalsMade"],FourthDownAttempts=i["FourthDownAttempts"],OpponentFieldGoalReturnYards=i["OpponentFieldGoalReturnYards"],OpponentOffensiveYards=i["OpponentOffensiveYards"],QuarterbackHitsPercentage=i["QuarterbackHitsPercentage"],BlockedKickReturnYards=i["BlockedKickReturnYards"])
        db.session.add(dd)
        db.session.commit()
    print "team season populated"

def graded_bets():
    """ this function populates NFLBetGraded db with latest score data that is available. Tell which team or side covered, which total over or under coverd and which team won the money line bets for each game played. 
     """
    NFLBetGraded.__table__.drop(db.engine)
    NFLBetGraded.__table__.create(db.engine)
    score1 = db.session.query(NFLScore).filter_by(SeasonType=1).all()
    score = list(score1)
    for x in score:
        grade = NFLBetGraded(game_key=x.GameKey,week = x.Week,game_date=parse_date(x.Date),home_team=x.HomeTeam,home_score=x.HomeScore,away_team=x.AwayTeam,away_score=x.AwayScore,total_score=(x.AwayScore+x.HomeScore),over_under=x.OverUnder,ps=x.PointSpread,cover_total=x.cover_total(),cover_side=x.cover_line(),cover_ml=x.cover_ml())
        db.session.add(grade)
        db.session.commit()
    print "graded bets table populated"


if __name__ == "__main__":
    # db.drop_all()
    # db.create_all()
    # create_roles()
    print "######################### start download cron job #######################"
    print('The time is: %s\r\n' % datetime.now())
    # myip = urllib2.urlopen("http://myip.dnsdynamic.org/").read()
    # print "your IP Address is: ",  myip
    # download()
    # print "just downloaded file please wait 20 sec...\r\n"
    # time.sleep(20)

    schedule = json.load(open('sports/Schedule.2016.json'))
    stadium = json.load(open("sports/Stadium.2016.json"))
    team = json.load(open("sports/Team.2016.json"))
    standing = json.load(open("sports/Standing.2016.json"))
    score = json.load(open("sports/Score.2016.json"))
    teamseason = json.load(open("sports/TeamSeason.2016.json"))
    print "json load .json files please wait 5 sec...."
    time.sleep(5)
    populate_schedule()
    populate_stadium()
    populate_team()
    populate_standing()
    populate_score()
    populate_teamseason()
    print "just populated stat tables with new info please wait 5 sec...\r\n"
    time.sleep(5)
    graded_bets()
    print "just graded bets, please wait 15 sec...\r\n"
    time.sleep(15)
    kitchen_sink()
    cache.clear()
    print "Done...\r\n"
    print "####################### end download cron job ############################"
    print "\r\n\r\n\r\n"

