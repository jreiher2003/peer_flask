import json
from dateutil.parser import parse as parse_date
from app import app, db 
from flask import request
from flask_security import login_required, roles_required, current_user
from app.users.models import Users 
from app.nfl_stats.models import NFLTeam,NFLScore
from app.nfl.models import NFLcreateBet,NFLBetGraded

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


@home_blueprint.route("/", methods=["GET","POST"])
def home():
    all_teams = all_nfl_teams()
    return render_template("home.html", all_teams=all_teams)

@home_blueprint.route("/profile/")
@login_required
def profile():
    all_teams = all_nfl_teams()
    graded_bets()
    user = Users.query.filter_by(id=current_user.id).one()
    pending_bets = NFLcreateBet.query.filter((NFLcreateBet.user_id==user.id) | (NFLcreateBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).all()
    
    return render_template("profile.html", user=user, pending_bets=pending_bets, all_teams=all_teams)

@home_blueprint.route("/admin/")
@roles_required("admin")
def admin():
    all_teams = all_nfl_teams()
    return "Admin page"

