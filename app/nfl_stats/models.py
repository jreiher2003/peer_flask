from __future__ import division
from datetime import datetime
from dateutil.parser import parse
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.sql import func
from app import db

class NFLSchedule(db.Model):
    __tablename__ = "schedule"

    id = db.Column(db.Integer, primary_key=True)
    GameKey = db.Column(db.String)
    SeasonType = db.Column(db.Integer)
    Season = db.Column(db.Integer)
    Week = db.Column(db.Integer)
    Date = db.Column(db.String)
    AwayTeam = db.Column(db.String)
    HomeTeam = db.Column(db.String)
    PointSpread = db.Column(db.Float)
    OverUnder = db.Column(db.Float)
    StadiumID = db.Column(db.Integer)
    Canceled = db.Column(db.Boolean)
    GeoLat = db.Column(db.Float)
    GeoLong = db.Column(db.Float)
    ForecastTempLow = db.Column(db.Integer)
    ForecastTempHigh = db.Column(db.Integer)
    ForecastDescription = db.Column(db.String)
    ForecastWindChill = db.Column(db.Integer)
    ForecastWindSpeed = db.Column(db.Integer)
    AwayTeamMoneyLine = db.Column(db.Integer)
    HomeTeamMoneyLine = db.Column(db.Integer)
    Channel = db.Column(db.String)

    @property 
    def OverUnder_(self):
        if self.OverUnder == None: return "N/A"
        else: return self.OverUnder

    @property 
    def away_pointspread(self):
        if self.PointSpread == None: return "N/A"
        elif self.PointSpread > 0: return self.PointSpread * -1
        else: return self.PointSpread 

    @property 
    def home_pointspread(self):
        if self.PointSpread == None: return "N/A"
        elif self.PointSpread < 0: return self.PointSpread
        else: return self.PointSpread * -1

    @property 
    def even_pointspread(self):
        if self.PointSpread == 0.0: return "even"

    @property 
    def away_ml(self):
        if self.AwayTeamMoneyLine == None: return "N/A"
        elif self.AwayTeamMoneyLine > 0: return "+%s" % (self.AwayTeamMoneyLine)
        else: return self.AwayTeamMoneyLine
        
    @property 
    def home_ml(self):
        if self.HomeTeamMoneyLine == None: return "N/A"
        elif self.HomeTeamMoneyLine > 0: return "+%s" % (self.HomeTeamMoneyLine)
        else: return self.HomeTeamMoneyLine

    @hybrid_property 
    def d_date(self):
        # "9/8/2016 8:30:00 PM"
        return datetime.strptime(self.Date, '%m/%d/%Y %I:%M:%f %p')





class NFLStandings(db.Model):
    __tablename__ = "standing"

    id = db.Column(db.Integer, primary_key=True)
    SeasonType = db.Column(db.Integer)
    Season = db.Column(db.Integer)
    Conference = db.Column(db.String)
    Division = db.Column(db.String)
    Team = db.Column(db.String)
    Name = db.Column(db.String)
    Wins = db.Column(db.Integer)
    Losses = db.Column(db.Integer)
    Ties = db.Column(db.Integer)
    Percentage = db.Column(db.Integer)
    PointsFor = db.Column(db.Integer)
    PointsAgainst = db.Column(db.Integer)
    NetPoints = db.Column(db.Integer)
    Touchdowns = db.Column(db.Integer)
    DivisionWins = db.Column(db.Integer)
    DivisionLosses = db.Column(db.Integer)
    ConferenceWins = db.Column(db.Integer)
    ConferenceLosses = db.Column(db.Integer)

    

class NFLTeam(db.Model):
    __tablename__ = "team"

    id = db.Column(db.Integer, primary_key=True)
    Key = db.Column(db.String)
    TeamID = db.Column(db.Integer)
    PlayerID = db.Column(db.Integer)
    City = db.Column(db.String)
    Name = db.Column(db.String)
    Conference = db.Column(db.String)
    Division = db.Column(db.String)
    FullName = db.Column(db.String)
    StadiumID = db.Column(db.Integer)
    ByeWeek = db.Column(db.Integer)
    HeadCoach = db.Column(db.String)
    OffensiveCoordinator = db.Column(db.String)
    DefensiveCoordinator = db.Column(db.String)
    SpecialTeamsCoach = db.Column(db.String)
    OffensiveScheme = db.Column(db.String)
    DefensiveScheme = db.Column(db.String)
    UpcomingOpponent = db.Column(db.String)
    PrimaryColor = db.Column(db.String)
    SecondaryColor = db.Column(db.String)
    TertiaryColor = db.Column(db.String)
    QuaternaryColor = db.Column(db.String)
    WikipediaLogoUrl = db.Column(db.String)
    WikipediaWordMarkUrl = db.Column(db.String)

    UpcomingSalary = db.Column(db.Integer)
    UpcomingOpponent = db.Column(db.String)
    UpcomingOpponentRank = db.Column(db.Integer)
    UpcomingOpponentPositionRank = db.Column(db.Integer)
    UpcomingFanDuelSalary = db.Column(db.Integer)
    UpcomingDraftKingsSalary = db.Column(db.Integer)
    UpcomingYahooSalary = db.Column(db.Integer)
    AverageDraftPosition = db.Column(db.Integer)
    AverageDraftPositionPPR = db.Column(db.Integer)


class NFLStadium(db.Model):
    __tablename__ = "stadium"

    id = db.Column(db.Integer, primary_key=True)
    StadiumID = db.Column(db.Integer)
    Name = db.Column(db.String)
    City = db.Column(db.String)
    State = db.Column(db.String)
    Country = db.Column(db.String)
    Capacity = db.Column(db.Integer)
    PlayingSurface = db.Column(db.String)
    GeoLat = db.Column(db.Float)
    GeoLong = db.Column(db.Float)

class NFLScore(db.Model):
    __tablename__ = "score"

    id = db.Column(db.Integer, primary_key=True)
    GameKey = db.Column(db.String)
    SeasonType = db.Column(db.Integer)
    Season = db.Column(db.Integer)
    Week = db.Column(db.Integer)
    Date = db.Column(db.String)
    AwayTeam = db.Column(db.String)
    HomeTeam = db.Column(db.String)
    AwayScore = db.Column(db.Integer)
    HomeScore = db.Column(db.Integer)
    PointSpread = db.Column(db.Integer)
    OverUnder = db.Column(db.Integer)
    AwayScoreQuarter1 = db.Column(db.Integer)
    AwayScoreQuarter2 = db.Column(db.Integer)
    AwayScoreQuarter3 = db.Column(db.Integer)
    AwayScoreQuarter4 = db.Column(db.Integer)
    AwayScoreOvertime = db.Column(db.Integer)
    HomeScoreQuarter1 = db.Column(db.Integer)
    HomeScoreQuarter2 = db.Column(db.Integer)
    HomeScoreQuarter3 = db.Column(db.Integer)
    HomeScoreQuarter4 = db.Column(db.Integer)
    HomeScoreOvertime = db.Column(db.Integer)
    HasStarted = db.Column(db.Boolean)
    IsOver = db.Column(db.Boolean)
    IsOvertime = db.Column(db.Boolean)
    QuarterDescription = db.Column(db.String)
    StadiumID = db.Column(db.Integer)
    LastUpdated = db.Column(db.String)
    GeoLat = db.Column(db.Float)
    GeoLong = db.Column(db.Float)
    ForecastTempLow = db.Column(db.Integer)
    ForecastTempHigh = db.Column(db.Integer)
    ForecastDescription = db.Column(db.String)
    ForecastWindChill = db.Column(db.Integer)
    ForecastWindSpeed = db.Column(db.Integer)
    AwayTeamMoneyLine = db.Column(db.Integer)
    HomeTeamMoneyLine = db.Column(db.Integer)

    TimeRemaining = db.Column(db.String)
    Possession = db.Column(db.String)
    Down = db.Column(db.String)
    Distance = db.Column(db.String)
    YardLine = db.Column(db.String)
    YardLineTerritory = db.Column(db.String)
    RedZone = db.Column(db.String)
    DownAndDistance = db.Column(db.String)
    Channel = db.Column(db.String)
    Has1stQuarterStarted = db.Column(db.Boolean)
    Has2ndQuarterStarted = db.Column(db.Boolean)
    Has3rdQuarterStarted = db.Column(db.Boolean)
    Has4thQuarterStarted = db.Column(db.Boolean)
    Closed = db.Column(db.Boolean)
    LastPlay = db.Column(db.String)
    Quarter = db.Column(db.String)
    IsInProgress = db.Column(db.Boolean)
    Canceled = db.Column(db.Boolean)

    def cover_line(self):
        """this covers 0.0 ps's"""
        if self.PointSpread <= 0:
            if (self.HomeScore + self.PointSpread) == self.AwayScore:return "Push"
            elif (self.HomeScore + self.PointSpread) > self.AwayScore:return self.HomeTeam
            else:return self.AwayTeam
        if self.PointSpread > 0:
            if (self.AwayScore + (self.PointSpread*-1)) == self.HomeScore:return "Push"
            elif (self.AwayScore + (self.PointSpread*-1)) > self.HomeScore:return self.AwayTeam
            else:return self.HomeTeam

    def cover_total(self):
        if self.AwayScore + self.HomeScore == self.OverUnder: return "Push"
        elif self.AwayScore + self.HomeScore > self.OverUnder: return "o"
        else: return "u"

    def cover_ml(self):
        if self.AwayScore == self.HomeScore: return "Push"
        elif self.AwayScore > self.HomeScore: return self.AwayTeam
        else: return self.HomeTeam 
    

    # nfl_bet_graded = db.relationship("NFLBetGraded", uselist=False, back_populates="nfl_score")
    

class NFLTeamSeason(db.Model):
    __tablename__ = "teamseason" 

    id = db.Column(db.Integer, primary_key=True)
    SeasonType = db.Column(db.Integer)
    Season = db.Column(db.Integer)

    Team = db.Column(db.String)
    Score = db.Column(db.Integer)
    OpponentScore = db.Column(db.Integer)
    TotalScore = db.Column(db.Integer)
    OverUnder = db.Column(db.Float)
    PointSpread = db.Column(db.Integer)

    ScoreQuarter1 = db.Column(db.Integer)
    ScoreQuarter2 = db.Column(db.Integer)
    ScoreQuarter3 = db.Column(db.Integer)
    ScoreQuarter4 = db.Column(db.Integer)
    ScoreOvertime = db.Column(db.Integer)

    TimeOfPossession = db.Column(db.String)

    FirstDowns = db.Column(db.Integer)
    FirstDownsByRushing = db.Column(db.Integer)
    FirstDownsByPassing = db.Column(db.Integer)
    FirstDownsByPenalty = db.Column(db.Integer)

    OffensivePlays = db.Column(db.Integer)
    OffensiveYards = db.Column(db.Integer)
    OffensiveYardsPerPlay = db.Column(db.Float)

    Touchdowns = db.Column(db.Integer)

    RushingAttempts = db.Column(db.Integer)
    RushingYards = db.Column(db.Integer)
    RushingYardsPerAttempt = db.Column(db.Integer)
    RushingTouchdowns = db.Column(db.Integer)

    PassingAttempts = db.Column(db.Integer)
    PassingCompletions = db.Column(db.Integer)
    PassingYards = db.Column(db.Integer)
    PassingTouchdowns = db.Column(db.Integer)
    PassingInterceptions = db.Column(db.Integer)
    PassingYardsPerAttempt = db.Column(db.Float)
    PassingYardsPerCompletion = db.Column(db.Float)
    CompletionPercentage = db.Column(db.Float)
    PasserRating = db.Column(db.Float)

    ThirdDownAttempts = db.Column(db.Integer)
    ThirdDownConversions = db.Column(db.Integer)
    ThirdDownPercentage = db.Column(db.Float)
    FourthDownAttempts = db.Column(db.Integer)
    FourthDownConversions = db.Column(db.Integer)
    FourthDownPercentage = db.Column(db.Float)

    RedZoneAttempts = db.Column(db.Integer)
    RedZoneConversions = db.Column(db.Integer)
    GoalToGoAttempts = db.Column(db.Integer)
    GoalToGoConversions = db.Column(db.Integer)

    ReturnYards = db.Column(db.Integer)

    Penalties = db.Column(db.Integer)
    PenaltyYards = db.Column(db.Integer)

    Fumbles = db.Column(db.Integer)
    FumblesLost = db.Column(db.Integer)

    TimesSacked = db.Column(db.Integer)
    TimesSackedYards = db.Column(db.Integer)

    QuarterbackHits = db.Column(db.Integer)
    TacklesForLoss = db.Column(db.Integer)
    Safeties = db.Column(db.Integer)

    Punts = db.Column(db.Integer)
    PuntYards = db.Column(db.Integer)
    PuntAverage = db.Column(db.Float)

    Giveaways = db.Column(db.Integer)
    Takeaways = db.Column(db.Integer)
    TurnoverDifferential = db.Column(db.Integer)

    OpponentScoreQuarter1 = db.Column(db.Integer)
    OpponentScoreQuarter2 = db.Column(db.Integer)
    OpponentScoreQuarter3 = db.Column(db.Integer)
    OpponentScoreQuarter4 = db.Column(db.Integer)
    OpponentScoreOvertime = db.Column(db.Integer)
    OpponentTimeOfPossession = db.Column(db.String)
    OpponentFirstDowns = db.Column(db.Integer)
    OpponentFirstDownsByRushing = db.Column(db.Integer)
    OpponentFirstDownsByPassing = db.Column(db.Integer)
    OpponentFirstDownsByPenalty = db.Column(db.Integer)
    OpponentOffensivePlays = db.Column(db.Integer)
    OpponentOffensiveYards = db.Column(db.Integer)
    OpponentOffensiveYardsPerPlay = db.Column(db.Float)
    OpponentTouchdowns = db.Column(db.Integer)
    OpponentRushingAttempts = db.Column(db.Integer)
    OpponentRushingYards = db.Column(db.Integer)
    OpponentRushingYardsPerAttempt = db.Column(db.Float)
    OpponentRushingTouchdowns = db.Column(db.Integer)
    OpponentPassingAttempts = db.Column(db.Integer)
    OpponentPassingCompletions = db.Column(db.Integer)
    OpponentPassingYards = db.Column(db.Integer)
    OpponentPassingTouchdowns = db.Column(db.Integer)
    OpponentPassingInterceptions = db.Column(db.Integer)
    OpponentPassingYardsPerAttempt = db.Column(db.Float)
    OpponentPassingYardsPerCompletion = db.Column(db.Float)
    OpponentCompletionPercentage = db.Column(db.Float)
    OpponentPasserRating = db.Column(db.Float)
    OpponentThirdDownAttempts = db.Column(db.Integer)
    OpponentThirdDownConversions = db.Column(db.Integer)
    OpponentThirdDownPercentage = db.Column(db.Float)
    OpponentFourthDownAttempts = db.Column(db.Integer)
    OpponentFourthDownConversions = db.Column(db.Integer)
    OpponentFourthDownPercentage = db.Column(db.Float)
    OpponentRedZoneAttempts = db.Column(db.Integer)
    OpponentRedZoneConversions = db.Column(db.Integer)
    OpponentGoalToGoAttempts = db.Column(db.Integer)
    OpponentGoalToGoConversions = db.Column(db.Integer)
    OpponentReturnYards = db.Column(db.Integer)
    OpponentPenalties = db.Column(db.Integer)
    OpponentPenaltyYards = db.Column(db.Integer)
    OpponentFumbles = db.Column(db.Integer)
    OpponentFumblesLost = db.Column(db.Integer)
    OpponentTimesSacked = db.Column(db.Integer)
    OpponentTimesSackedYards = db.Column(db.Integer)
    OpponentQuarterbackHits = db.Column(db.Integer)
    OpponentTacklesForLoss = db.Column(db.Integer)
    OpponentSafeties = db.Column(db.Integer)
    OpponentPunts = db.Column(db.Integer)
    OpponentPuntYards = db.Column(db.Integer)
    OpponentPuntAverage = db.Column(db.Float)
    OpponentGiveaways = db.Column(db.Integer)
    OpponentTakeaways = db.Column(db.Integer)
    OpponentTurnoverDifferential = db.Column(db.Integer)

    RedZonePercentage = db.Column(db.Float)
    GoalToGoPercentage = db.Column(db.Float)
    QuarterbackHitsDifferential = db.Column(db.Integer)
    TacklesForLossDifferential = db.Column(db.Integer)
    QuarterbackSacksDifferential = db.Column(db.Integer)
    TacklesForLossPercentage = db.Column(db.Float)
    QuarterbackHitsPercentage = db.Column(db.Float)
    TimesSackedPercentage = db.Column(db.Float)

    OpponentRedZonePercentage = db.Column(db.Integer)
    OpponentGoalToGoPercentage = db.Column(db.Integer)
    OpponentQuarterbackHitsDifferential = db.Column(db.Integer)
    OpponentTacklesForLossDifferential = db.Column(db.Integer)
    OpponentQuarterbackSacksDifferential = db.Column(db.Integer)
    OpponentTacklesForLossPercentage = db.Column(db.Float)
    OpponentQuarterbackHitsPercentage = db.Column(db.Float)
    OpponentTimesSackedPercentage = db.Column(db.Float)

    Kickoffs = db.Column(db.Integer)
    KickoffsInEndZone = db.Column(db.Integer)
    KickoffTouchbacks = db.Column(db.Integer)
    PuntsHadBlocked = db.Column(db.Integer)
    PuntNetAverage = db.Column(db.Float)
    ExtraPointKickingAttempts = db.Column(db.Integer)
    ExtraPointKickingConversions = db.Column(db.Integer)
    ExtraPointsHadBlocked = db.Column(db.Integer)
    ExtraPointPassingAttempts = db.Column(db.Integer)
    ExtraPointPassingConversions = db.Column(db.Integer)
    ExtraPointRushingAttempts = db.Column(db.Integer)
    ExtraPointRushingConversions = db.Column(db.Integer)
    FieldGoalAttempts = db.Column(db.Integer)
    FieldGoalsMade = db.Column(db.Integer)
    FieldGoalsHadBlocked = db.Column(db.Integer)
    PuntReturns = db.Column(db.Integer)
    PuntReturnYards = db.Column(db.Integer)
    KickReturns = db.Column(db.Integer)
    KickReturnYards = db.Column(db.Integer)

    InterceptionReturns = db.Column(db.Integer)
    InterceptionReturnYards = db.Column(db.Integer)

    OpponentKickoffs = db.Column(db.Integer)
    OpponentKickoffsInEndZone = db.Column(db.Integer)
    OpponentKickoffTouchbacks = db.Column(db.Integer)
    OpponentPuntsHadBlocked = db.Column(db.Integer)
    OpponentPuntNetAverage = db.Column(db.Float)
    OpponentExtraPointKickingAttempts = db.Column(db.Integer)
    OpponentExtraPointKickingConversions = db.Column(db.Integer)
    OpponentExtraPointsHadBlocked = db.Column(db.Integer)
    OpponentExtraPointPassingAttempts = db.Column(db.Integer)
    OpponentExtraPointPassingConversions = db.Column(db.Integer)
    OpponentExtraPointRushingAttempts = db.Column(db.Integer)
    OpponentExtraPointRushingConversions = db.Column(db.Integer)
    OpponentFieldGoalAttempts = db.Column(db.Integer)
    OpponentFieldGoalsMade = db.Column(db.Integer)
    OpponentFieldGoalsHadBlocked = db.Column(db.Integer)
    OpponentPuntReturns = db.Column(db.Integer)
    OpponentPuntReturnYards = db.Column(db.Integer)
    OpponentKickReturns = db.Column(db.Integer)
    OpponentKickReturnYards = db.Column(db.Integer)

    OpponentInterceptionReturns = db.Column(db.Integer)
    OpponentInterceptionReturnYards = db.Column(db.Integer)

    SoloTackles = db.Column(db.Integer)
    AssistedTackles = db.Column(db.Integer)
    Sacks = db.Column(db.Integer)
    SackYards = db.Column(db.Integer)
    PassesDefended = db.Column(db.Integer)
    FumblesForced = db.Column(db.Integer)
    FumblesRecovered = db.Column(db.Integer)
    FumbleReturnYards = db.Column(db.Integer)
    FumbleReturnTouchdowns = db.Column(db.Integer)
    InterceptionReturnTouchdowns = db.Column(db.Integer)

    BlockedKicks = db.Column(db.Integer)
    BlockedKickReturnYards = db.Column(db.Integer)
    BlockedKickReturnTouchdowns = db.Column(db.Integer)
    
    PuntReturnTouchdowns = db.Column(db.Integer)
    PuntReturnLong = db.Column(db.Integer)
    KickReturnTouchdowns = db.Column(db.Integer)
    KickReturnLong = db.Column(db.Integer)
    FieldGoalReturnYards = db.Column(db.Integer)
    FieldGoalReturnTouchdowns = db.Column(db.Integer)
    PuntNetYards = db.Column(db.Integer)

    OpponentSoloTackles = db.Column(db.Integer)
    OpponentAssistedTackles = db.Column(db.Integer)
    OpponentSacks = db.Column(db.Integer)
    OpponentSackYards = db.Column(db.Integer)
    OpponentPassesDefended = db.Column(db.Integer)
    OpponentFumblesForced = db.Column(db.Integer)
    OpponentFumblesRecovered = db.Column(db.Integer)
    OpponentFumbleReturnYards = db.Column(db.Integer)
    OpponentFumbleReturnTouchdowns = db.Column(db.Integer)
    OpponentInterceptionReturnTouchdowns = db.Column(db.Integer)
    OpponentBlockedKicks = db.Column(db.Integer)
    OpponentPuntReturnTouchdowns = db.Column(db.Integer)
    OpponentPuntReturnLong = db.Column(db.Integer)
    OpponentKickReturnTouchdowns = db.Column(db.Integer)
    OpponentKickReturnLong = db.Column(db.Integer)
    OpponentBlockedKickReturnYards = db.Column(db.Integer)
    OpponentBlockedKickReturnTouchdowns = db.Column(db.Integer)
    OpponentFieldGoalReturnYards = db.Column(db.Integer)
    OpponentFieldGoalReturnTouchdowns = db.Column(db.Integer)
    OpponentPuntNetYards = db.Column(db.Integer)

    TeamName = db.Column(db.String)
    Games = db.Column(db.Integer)
    PassingDropbacks = db.Column(db.Integer)
    OpponentPassingDropbacks = db.Column(db.Integer)
    TeamSeasonID = db.Column(db.Integer)
    PointDifferential = db.Column(db.Integer)
    PassingInterceptionPercentage = db.Column(db.Integer)
    PuntReturnAverage = db.Column(db.Integer)
    KickReturnAverage = db.Column(db.Integer)
    ExtraPointPercentage = db.Column(db.Float)
    FieldGoalPercentage = db.Column(db.Integer)

    OpponentPassingInterceptionPercentage = db.Column(db.Float)
    OpponentPuntReturnAverage = db.Column(db.Float)
    OpponentKickReturnAverage = db.Column(db.Float)
    OpponentExtraPointPercentage = db.Column(db.Float)
    OpponentFieldGoalPercentage = db.Column(db.Float)

    PenaltyYardDifferential = db.Column(db.Integer)
    PuntReturnYardDifferential = db.Column(db.Integer)
    KickReturnYardDifferential = db.Column(db.Integer)
    TwoPointConversionReturns = db.Column(db.Integer)
    OpponentTwoPointConversionReturns = db.Column(db.Integer)

    WindSpeed = db.Column(db.Integer)
    Temperature = db.Column(db.Integer)
    Humidity = db.Column(db.Integer)

    ######################################################
    ####### total offensive ##############################
    ######################################################
    @property 
    def passing_per_game(self):
        return round((self.PassingYards / self.Games),1)

    @property 
    def rushing_yards_per_game(self):
        return round((self.RushingYards / self.Games),1)

    @property 
    def offensive_yards_per_game(self):
        return round((self.OffensiveYards / self.Games),1)

    @property 
    def score_per_game(self):
        return round((self.Score / self.Games),1)

    @property 
    def opponent_passing_per_game(self):
        return round((self.OpponentPassingYards / self.Games),1)

    @property 
    def opponent_rushing_yards_per_game(self):
        return round((self.OpponentRushingYards / self.Games),1)

    @property 
    def opponent_offensive_yards_per_game(self):
        return round((self.OpponentOffensiveYards / self.Games),1)

    @property 
    def opponent_score_per_game(self):
        return round((self.OpponentScore / self.Games),1)

    ##############################################################
    ########### total passing offense \ defence ##################
    ##############################################################
    @property 
    def net_passing_yrd_per_game(self):
        return round((self.PassingYards / self.Games),1)

    @property 
    def opponent_net_passing_yrd_per_game(self):
        return round((self.OpponentPassingYards / self.Games),1)

    ##############################################################
    ########## total rushing offense/defence #####################
    ##############################################################
    @property 
    def net_rushing_yrd_per_game(self):
        return round((self.RushingYards/self.Games),1)

    @property 
    def opponent_net_rushing_yrd_per_game(self):
        return round((self.OpponentRushingYards/self.Games),1)


    ##############################################################
    ############### total receiving offence/defence ##############
    ##############################################################
    @property 
    def net_receiving_yrd(self):
        return round((self.PassingYards+self.OpponentSackYards),1)

    @property 
    def avg_yrd_per_catch(self):
        return round(((self.PassingYards+self.OpponentSackYards)/self.PassingCompletions),1)

    @property 
    def receiving_yrd_per_game(self):
        return round(((self.PassingYards+self.OpponentSackYards)/self.Games),1)

    @property 
    def opponent_net_receiving_yrd(self):
        return round((self.OpponentPassingYards+self.SackYards),1)

    @property 
    def opponent_avg_yrd_per_catch(self):
        return round(((self.OpponentPassingYards+self.SackYards)/self.OpponentPassingCompletions),1)

    @property 
    def opponent_receiving_yrd_per_game(self):
        return round(((self.OpponentPassingYards+self.SackYards)/self.Games),1)

