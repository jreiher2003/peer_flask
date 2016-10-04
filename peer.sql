DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL, 
    username VARCHAR(50) NOT NULL, 
    email VARCHAR(255) NOT NULL, 
    password VARCHAR(255) NOT NULL, 
    active BOOLEAN, 
    confirmed_at DATETIME, 
    date_created DATETIME, 
    date_modified DATETIME, 
    last_login_at DATETIME, 
    last_login_ip VARCHAR(45), 
    current_login_at DATETIME, 
    current_login_ip VARCHAR(45), 
    login_count INTEGER, 
    PRIMARY KEY (id), 
    UNIQUE (username), 
    UNIQUE (email), 
    CHECK (active IN (0, 1))
);
DROP TABLE IF EXISTS role;
CREATE TABLE IF NOT EXISTS role (
    id INTEGER NOT NULL, 
    name VARCHAR(50), 
    description VARCHAR(255), 
    PRIMARY KEY (id), 
    UNIQUE (name)
);
DROP TABLE IF EXISTS user_roles;
CREATE TABLE IF NOT EXISTS user_roles (
    id INTEGER NOT NULL, 
    user_id INTEGER, 
    role_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
    FOREIGN KEY(role_id) REFERENCES role (id) ON DELETE CASCADE
);
DROP TABLE IF EXISTS profile;
CREATE TABLE IF NOT EXISTS profile (
    id INTEGER NOT NULL, 
    avatar VARCHAR, 
    user_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);




DROP TABLE IF EXISTS nfl_bet;
CREATE TABLE IF NOT EXISTS nfl_bet (
    id INTEGER NOT NULL, 
    game_key INTEGER, 
    bet_key INTEGER, 
    game_date DATETIME, 
    over_under VARCHAR, 
    total INTEGER, 
    amount NUMERIC(12, 2), 
    vs VARCHAR, 
    home_team VARCHAR, 
    away_team VARCHAR, 
    team VARCHAR, 
    ps INTEGER, 
    ml INTEGER, 
    taken_by INTEGER, 
    bet_created DATETIME, 
    bet_modified DATETIME, 
    bet_taken DATETIME, 
    user_id INTEGER, 
    PRIMARY KEY (id), 
    UNIQUE (bet_key), 
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS schedule;
CREATE TABLE IF NOT EXISTS schedule (
    id INTEGER PRIMARY KEY, 
    Week INTEGER, 
    AwayTeamMoneyLine INTEGER, 
    StadiumID INTEGER, 
    GameKey TEXT, 
    Canceled BOOLEAN, 
    Season INTEGER, 
    HomeTeam TEXT, 
    ForecastWindSpeed INTEGER, 
    OverUnder REAL, 
    GeoLong REAL, 
    ForecastDescription INTEGER, 
    AwayTeam TEXT, 
    ForecastTempLow INTEGER, 
    PointSpread REAL, 
    ForecastWindChill INTEGER, 
    ForecastTempHigh INTEGER, 
    Date TEXT, 
    GeoLat REAL, 
    SeasonType INTEGER, 
    Channel NULL, 
    HomeTeamMoneyLine INTEGER
    );

DROP TABLE IF EXISTS standing;
CREATE TABLE IF NOT EXISTS standing (
    id INTEGER PRIMARY KEY, 
    SeasonType INTEGER, 
    Season INTEGER, 
    Conference TEXT, 
    Division TEXT, 
    Team TEXT, 
    Name TEXT, 
    Wins INTEGER, 
    Losses INTEGER, 
    Ties INTEGER, 
    Percentage NUMERIC, 
    PointsFor INTEGER, 
    PointsAgainst INTEGER, 
    NetPoints INTEGER, 
    Touchdowns INTEGER, 
    DivisionWins INTEGER, 
    DivisionLosses INTEGER, 
    ConferenceWins INTEGER, 
    ConferenceLosses INTEGER
    );

DROP TABLE IF EXISTS team;
CREATE TABLE IF NOT EXISTS team (
    id INTEGER PRIMARY KEY, 
    Key TEXT, 
    TeamID INTEGER, 
    PlayerID INTEGER, 
    City TEXT, 
    Name TEXT, 
    Conference TEXT, 
    Division TEXT, 
    FullName TEXT, 
    StadiumID INTEGER, 
    ByeWeek INTEGER, 
    AverageDraftPosition INTEGER, 
    AverageDraftPositionPPR INTEGER, 
    HeadCoach TEXT, 
    OffensiveCoordinator TEXT, 
    DefensiveCoordinator TEXT, 
    SpecialTeamsCoach TEXT, 
    OffensiveScheme TEXT, 
    DefensiveScheme TEXT, 
    UpcomingSalary INTEGER, 
    UpcomingOpponent TEXT, 
    UpcomingOpponentRank INTEGER, 
    UpcomingOpponentPositionRank INTEGER, 
    UpcomingFanDuelSalary INTEGER, 
    UpcomingDraftKingsSalary INTEGER, 
    UpcomingYahooSalary INTEGER
    );

DROP TABLE IF EXISTS stadium;
CREATE TABLE IF NOT EXISTS stadium (
    id INTEGER PRIMARY KEY, 
    StadiumID INTEGER, 
    Name TEXT, 
    City TEXT, 
    State TEXT, 
    Country TEXT, 
    Capacity INTEGER, 
    PlayingSurface TEXT, 
    GeoLat REAL, 
    GeoLong REAL
    );

DROP TABLE IF EXISTS score;
CREATE TABLE IF NOT EXISTS score (
    id INTEGER PRIMARY KEY, 
    GameKey TEXT, 
    SeasonType INTEGER, 
    Season INTEGER, 
    Week INTEGER, 
    Date TEXT, 
    AwayTeam TEXT, 
    HomeTeam TEXT, 
    AwayScore INTEGER,
    HomeScore INTEGER, 
    Channel TEXT, 
    PointSpread REAL, 
    OverUnder REAL, 
    Quarter TEXT, 
    TimeRemaining NULL, 
    Possession NULL, 
    Down NULL, 
    Distance NULL, 
    YardLine NULL, 
    YardLineTerritory NULL, 
    RedZone NULL, 
    AwayScoreQuarter1 INTEGER, 
    AwayScoreQuarter2 INTEGER, 
    AwayScoreQuarter3 INTEGER, 
    AwayScoreQuarter4 INTEGER, 
    AwayScoreOvertime INTEGER, 
    HomeScoreQuarter1 INTEGER, 
    HomeScoreQuarter2 INTEGER, 
    HomeScoreQuarter3 INTEGER, 
    HomeScoreQuarter4 INTEGER,
    HomeScoreOvertime INTEGER, 
    HasStarted BOOLEAN, 
    IsInProgress BOOLEAN, 
    IsOver BOOLEAN, 
    Has1stQuarterStarted BOOLEAN,
    Has2ndQuarterStarted BOOLEAN, 
    Has3rdQuarterStarted BOOLEAN, 
    Has4thQuarterStarted BOOLEAN, 
    IsOvertime BOOLEAN, 
    DownAndDistance NULL, 
    QuarterDescription TEXT, 
    StadiumID INTEGER, 
    LastUpdated NUMERIC, 
    GeoLat REAL, 
    GeoLong REAL, 
    ForecastTempLow INTEGER, 
    ForecastTempHigh INTEGER, 
    ForecastDescription TEXT, 
    ForecastWindChill INTEGER, 
    ForecastWindSpeed INTEGER, 
    AwayTeamMoneyLine INTEGER, 
    HomeTeamMoneyLine INTEGER, 
    Canceled BOOLEAN, 
    Closed BOOLEAN, 
    LastPlay NULL
    );

DROP TABLE IF EXISTS teamseason;
CREATE TABLE IF NOT EXISTS teamseason (
    id INTEGER PRIMARY KEY, 
    SeasonType INTEGER, 
    Season INTEGER, 
    Team TEXT, 
    Score INTEGER, 
    OpponentScore INTEGER, 
    TotalScore INTEGER, 
    Temperature INTEGER, 
    Humidity INTEGER, 
    WindSpeed INTEGER, 
    OverUnder REAL, 
    PointSpread REAL, 
    ScoreQuarter1 INTEGER, 
    ScoreQuarter2 INTEGER, 
    ScoreQuarter3 INTEGER, 
    ScoreQuarter4 INTEGER, 
    ScoreOvertime INTEGER, 
    TimeOfPossession TEXT, 
    FirstDowns INTEGER, 
    FirstDownsByRushing INTEGER, 
    FirstDownsByPassing INTEGER, 
    FirstDownsByPenalty INTEGER, 
    OffensivePlays INTEGER, 
    OffensiveYards INTEGER, 
    OffensiveYardsPerPlay NUMERIC, 
    Touchdowns INTEGER, 
    RushingAttempts INTEGER, 
    RushingYards INTEGER, 
    RushingYardsPerAttempt INTEGER, 
    RushingTouchdowns INTEGER, 
    PassingAttempts INTEGER, 
    PassingCompletions INTEGER, 
    PassingYards INTEGER, 
    PassingTouchdowns INTEGER, 
    PassingInterceptions INTEGER,
    PassingYardsPerAttempt NUMERIC, 
    PassingYardsPerCompletion NUMERIC, 
    CompletionPercentage NUMERIC, 
    PasserRating NUMERIC, 
    ThirdDownAttempts INTEGER, 
    ThirdDownConversions INTEGER, 
    ThirdDownPercentage NUMERIC, 
    FourthDownAttempts INTEGER, 
    FourthDownConversions INTEGER, 
    FourthDownPercentage NUMERIC, 
    RedZoneAttempts INTEGER, 
    RedZoneConversions INTEGER, 
    GoalToGoAttempts INTEGER, 
    GoalToGoConversions INTEGER, 
    ReturnYards INTEGER, 
    Penalties INTEGER, 
    PenaltyYards INTEGER, 
    Fumbles INTEGER, 
    FumblesLost INTEGER, 
    TimesSacked INTEGER, 
    TimesSackedYards INTEGER, 
    QuarterbackHits INTEGER, 
    TacklesForLoss INTEGER, 
    Safeties INTEGER, 
    Punts INTEGER, 
    PuntYards INTEGER, 
    PuntAverage NUMERIC, 
    Giveaways INTEGER, 
    Takeaways INTEGER, 
    TurnoverDifferential INTEGER, 
    OpponentScoreQuarter1 INTEGER, 
    OpponentScoreQuarter2 INTEGER, 
    OpponentScoreQuarter3 INTEGER, 
    OpponentScoreQuarter4 INTEGER, 
    OpponentScoreOvertime INTEGER, 
    OpponentTimeOfPossession TEXT, 
    OpponentFirstDowns INTEGER, 
    OpponentFirstDownsByRushing INTEGER, 
    OpponentFirstDownsByPassing INTEGER, 
    OpponentFirstDownsByPenalty INTEGER, 
    OpponentOffensivePlays INTEGER, 
    OpponentOffensiveYards INTEGER, 
    OpponentOffensiveYardsPerPlay NUMERIC, 
    OpponentTouchdowns INTEGER, 
    OpponentRushingAttempts INTEGER, 
    OpponentRushingYards INTEGER, 
    OpponentRushingYardsPerAttempt NUMERIC, 
    OpponentRushingTouchdowns INTEGER, 
    OpponentPassingAttempts INTEGER, 
    OpponentPassingCompletions INTEGER, 
    OpponentPassingYards INTEGER, 
    OpponentPassingTouchdowns INTEGER, 
    OpponentPassingInterceptions INTEGER, 
    OpponentPassingYardsPerAttempt NUMERIC, 
    OpponentPassingYardsPerCompletion NUMERIC, 
    OpponentCompletionPercentage INTEGER, 
    OpponentPasserRating NUMERIC, 
    OpponentThirdDownAttempts INTEGER, 
    OpponentThirdDownConversions INTEGER, 
    OpponentThirdDownPercentage NUMERIC, 
    OpponentFourthDownAttempts INTEGER, 
    OpponentFourthDownConversions INTEGER, 
    OpponentFourthDownPercentage NUMERIC, 
    OpponentRedZoneAttempts INTEGER, 
    OpponentRedZoneConversions INTEGER, 
    OpponentGoalToGoAttempts INTEGER, 
    OpponentGoalToGoConversions INTEGER, 
    OpponentReturnYards INTEGER, 
    OpponentPenalties INTEGER, 
    OpponentPenaltyYards INTEGER, 
    OpponentFumbles INTEGER, 
    OpponentFumblesLost INTEGER, 
    OpponentTimesSacked INTEGER, 
    OpponentTimesSackedYards INTEGER, 
    OpponentQuarterbackHits INTEGER, 
    OpponentTacklesForLoss INTEGER, 
    OpponentSafeties INTEGER, 
    OpponentPunts INTEGER, 
    OpponentPuntYards INTEGER, 
    OpponentPuntAverage NUMERIC, 
    OpponentGiveaways INTEGER, 
    OpponentTakeaways INTEGER, 
    OpponentTurnoverDifferential INTEGER, 
    RedZonePercentage NUMERIC, 
    GoalToGoPercentage NUMERIC, 
    QuarterbackHitsDifferential INTEGER, 
    TacklesForLossDifferential INTEGER, 
    QuarterbackSacksDifferential INTEGER, 
    TacklesForLossPercentage NUMERIC, 
    QuarterbackHitsPercentage NUMERIC, 
    TimesSackedPercentage NUMERIC, 
    OpponentRedZonePercentage NUMERIC, 
    OpponentGoalToGoPercentage NUMERIC, 
    OpponentQuarterbackHitsDifferential INTEGER,
    OpponentTacklesForLossDifferential INTEGER, 
    OpponentQuarterbackSacksDifferential INTEGER, 
    OpponentTacklesForLossPercentage NUMERIC, 
    OpponentQuarterbackHitsPercentage NUMERIC, 
    OpponentTimesSackedPercentage NUMERIC, 
    Kickoffs INTEGER, 
    KickoffsInEndZone INTEGER, 
    KickoffTouchbacks INTEGER, 
    PuntsHadBlocked INTEGER, 
    PuntNetAverage NUMERIC, 
    ExtraPointKickingAttempts INTEGER, 
    ExtraPointKickingConversions INTEGER, 
    ExtraPointsHadBlocked INTEGER, 
    ExtraPointPassingAttempts INTEGER, 
    ExtraPointPassingConversions INTEGER, 
    ExtraPointRushingAttempts INTEGER, 
    ExtraPointRushingConversions INTEGER, 
    FieldGoalAttempts INTEGER, 
    FieldGoalsMade INTEGER, 
    FieldGoalsHadBlocked INTEGER, 
    PuntReturns INTEGER, 
    PuntReturnYards INTEGER, 
    KickReturns INTEGER, 
    KickReturnYards INTEGER, 
    InterceptionReturns INTEGER, 
    InterceptionReturnYards INTEGER, 
    OpponentKickoffs INTEGER, 
    OpponentKickoffsInEndZone INTEGER, 
    OpponentKickoffTouchbacks INTEGER, 
    OpponentPuntsHadBlocked INTEGER, 
    OpponentPuntNetAverage INTEGER, 
    OpponentExtraPointKickingAttempts INTEGER, 
    OpponentExtraPointKickingConversions INTEGER, 
    OpponentExtraPointsHadBlocked INTEGER, 
    OpponentExtraPointPassingAttempts INTEGER, 
    OpponentExtraPointPassingConversions INTEGER, 
    OpponentExtraPointRushingAttempts INTEGER, 
    OpponentExtraPointRushingConversions INTEGER, 
    OpponentFieldGoalAttempts INTEGER, 
    OpponentFieldGoalsMade INTEGER, 
    OpponentFieldGoalsHadBlocked INTEGER, 
    OpponentPuntReturns INTEGER, 
    OpponentPuntReturnYards INTEGER, 
    OpponentKickReturns INTEGER, 
    OpponentKickReturnYards INTEGER, 
    OpponentInterceptionReturns INTEGER, 
    OpponentInterceptionReturnYards INTEGER, 
    SoloTackles INTEGER, 
    AssistedTackles INTEGER, 
    Sacks INTEGER, 
    SackYards INTEGER, 
    PassesDefended INTEGER, 
    FumblesForced INTEGER, 
    FumblesRecovered INTEGER, 
    FumbleReturnYards INTEGER, 
    FumbleReturnTouchdowns INTEGER, 
    InterceptionReturnTouchdowns INTEGER, 
    BlockedKicks INTEGER, 
    PuntReturnTouchdowns INTEGER, 
    PuntReturnLong INTEGER, 
    KickReturnTouchdowns INTEGER, 
    KickReturnLong INTEGER, 
    BlockedKickReturnYards INTEGER, 
    BlockedKickReturnTouchdowns INTEGER, 
    FieldGoalReturnYards INTEGER, 
    FieldGoalReturnTouchdowns INTEGER, 
    PuntNetYards INTEGER, 
    OpponentSoloTackles INTEGER, 
    OpponentAssistedTackles INTEGER, 
    OpponentSacks INTEGER, 
    OpponentSackYards INTEGER, 
    OpponentPassesDefended INTEGER, 
    OpponentFumblesForced INTEGER, 
    OpponentFumblesRecovered INTEGER, 
    OpponentFumbleReturnYards INTEGER, 
    OpponentFumbleReturnTouchdowns INTEGER, 
    OpponentInterceptionReturnTouchdowns INTEGER, 
    OpponentBlockedKicks INTEGER, 
    OpponentPuntReturnTouchdowns INTEGER, 
    OpponentPuntReturnLong INTEGER, 
    OpponentKickReturnTouchdowns INTEGER, 
    OpponentKickReturnLong INTEGER, 
    OpponentBlockedKickReturnYards INTEGER, 
    OpponentBlockedKickReturnTouchdowns INTEGER, 
    OpponentFieldGoalReturnYards INTEGER, 
    OpponentFieldGoalReturnTouchdowns INTEGER, 
    OpponentPuntNetYards INTEGER, 
    TeamName TEXT, 
    Games INTEGER, 
    PassingDropbacks INTEGER, 
    OpponentPassingDropbacks INTEGER, 
    TeamSeasonID INTEGER, 
    PointDifferential INTEGER, 
    PassingInterceptionPercentage NUMERIC, 
    PuntReturnAverage NUMERIC, 
    KickReturnAverage NUMERIC, 
    ExtraPointPercentage NUMERIC, 
    FieldGoalPercentage NUMERIC, 
    OpponentPassingInterceptionPercentage NUMERIC, 
    OpponentPuntReturnAverage NUMERIC, 
    OpponentKickReturnAverage NUMERIC, 
    OpponentExtraPointPercentage NUMERIC, 
    OpponentFieldGoalPercentage NUMERIC, 
    PenaltyYardDifferential INTEGER, 
    PuntReturnYardDifferential INTEGER, 
    KickReturnYardDifferential INTEGER, 
    TwoPointConversionReturns INTEGER, 
    OpponentTwoPointConversionReturns INTEGER
    );