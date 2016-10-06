import json
from dateutil.parser import parse as parse_date
from app import app, db 
from flask import request
from flask_security import login_required, roles_required, current_user
from app.users.models import Users 
from app.nfl_stats.models import NFLTeam,NFLScore
from app.nfl.models import NFLcreateBet,NFLBetGraded,NFLtakeBet

from flask import Blueprint, render_template

home_blueprint = Blueprint("home", __name__, template_folder="templates")

def all_nfl_teams():
    return NFLTeam.query.all()

def graded_bets():
    score = db.session.query(NFLScore).filter_by(SeasonType=1).all()
    NFLBetGraded.__table__.drop(db.engine)
    NFLBetGraded.__table__.create(db.engine)
    for x in score:
        grade = NFLBetGraded(game_key=x.GameKey,week = x.Week,game_date=parse_date(x.Date),home_team=x.HomeTeam,home_score=x.HomeScore,away_team=x.AwayTeam,away_score=x.AwayScore,total_score=(x.AwayScore+x.HomeScore),over_under=x.OverUnder,ps=x.PointSpread,cover_total=x.cover_total(),cover_side=x.cover_line())
        db.session.add(grade)
        db.session.commit()

def grade_cb():
    graded_bets()
    graded1 = NFLBetGraded.query.all()
    cb1 = NFLcreateBet.query.all()
    cb = [r for r in cb1]
    grd = [r for r in graded1]
    for g in grd:
        for c in cb:
            if g.game_key == c.game_key:
                if c.over_under == "u" or c.over_under == "o":
                    if c.over_under == g.cover_total:
                        c.win = True
                        c.lose = False
                        c.bet_graded = True
                    else:
                        c.lose = True
                        c.win = False
                        c.bet_graded = True

                if c.ps != None:
                    if c.team == g.cover_side:
                        c.win = True
                        c.lose = False
                        c.bet_graded = True
                    else:
                        c.lose = True
                        c.win = False 
                        c.bet_graded = True
    db.session.add(c)
    db.session.commit()

def grade_tb():
    graded_bets()
    graded1 = NFLBetGraded.query.all()
    cb1 = NFLtakeBet.query.all()
    cb = [r for r in cb1]
    grd = [r for r in graded1]
    for g in grd:
        for c in cb:
            if g.game_key == c.game_key:
                if c.over_under == "u" or c.over_under == "o":
                    if c.over_under == g.cover_total:
                        c.win = True
                        c.lose = False
                        c.bet_graded = True
                    else:
                        c.lose = True
                        c.win = False
                        c.bet_graded = True
                if c.ps != None:
                    if c.team == g.cover_side:
                        c.win = True
                        c.lose = False
                        c.bet_graded = True
                    else:
                        c.lose = True
                        c.win = False 
                        c.bet_graded = True
    db.session.add(c)
    db.session.commit()


@home_blueprint.route("/", methods=["GET","POST"])
def home():
    all_teams = all_nfl_teams()
    return render_template("home.html", all_teams=all_teams)

@home_blueprint.route("/profile/")
@login_required
def profile():
    all_teams = all_nfl_teams()
    grade_cb()
    grade_tb()
    user = Users.query.filter_by(id=current_user.id).one()
    pending_bets = NFLcreateBet.query.filter((NFLcreateBet.user_id==user.id) | (NFLcreateBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).all()
    count_wins1 = NFLcreateBet.query.filter_by(user_id=current_user.id,win=True).count()
    count_losses1 = NFLcreateBet.query.filter_by(user_id=current_user.id,win=False).count()
    # count_wins = NFLtakeBet.query.filter_by(user_id=current_user.id,win=True).count()
    # count_losses = NFLtakeBet.query.filter_by(user_id=current_user.id,win=False).count()
    user.profile.wins = count_wins1
    user.profile.losses = count_losses1
    # user.profile.wins = count_wins
    # user.profile.losses = count_losses
    db.session.add(user)
    db.session.commit()
    return render_template("profile.html", user=user, pending_bets=pending_bets, all_teams=all_teams)

@home_blueprint.route("/admin/")
@roles_required("admin")
def admin():
    all_teams = all_nfl_teams()
    return "Admin page"

