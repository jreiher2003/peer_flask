from datetime import datetime
from dateutil.parser import parse
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
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
    PointSpread = db.Column(db.Integer)
    OverUnder = db.Column(db.Integer)
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

    @property 
    def away_pointspread(self):
        if self.PointSpread > 0:
            return self.PointSpread * -1
    @property 
    def home_pointspread(self):
        if self.PointSpread < 0:
            return self.PointSpread

    @property 
    def even_pointspread(self):
        if self.PointSpread == 0.0:
            return "even"

    @property 
    def away_ml(self):
        if self.AwayTeamMoneyLine > 0:
            return "+%s" % (self.AwayTeamMoneyLine)
        else:
            return self.AwayTeamMoneyLine
        
    @property 
    def home_ml(self):
        if self.HomeTeamMoneyLine > 0:
            return "+%s" % (self.HomeTeamMoneyLine)
        else:
            return self.HomeTeamMoneyLine

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
    GameKey = db.Column(db.Integer)
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
    

