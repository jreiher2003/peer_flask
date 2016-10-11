import json
from dateutil.parser import parse as parse_date
from app import app, db, cache, block_io
from flask import request
from flask_security import login_required, roles_required, roles_accepted, current_user
from app.users.models import Users, Profile 
from app.nfl_stats.models import NFLTeam, NFLScore
from app.nfl.models import NFLBetGraded, NFLOverUnderBet, NFLSideBet, NFLMLBet
from flask import Blueprint, render_template
from .utils import all_nfl_teams, grade_query, count_pending_bets, count_graded_bets


home_blueprint = Blueprint("home", __name__, template_folder="templates")
 
@home_blueprint.route("/", methods=["GET","POST"])
def home():
    all_teams = all_nfl_teams()
    all_address = block_io.get_my_addresses()
    return render_template("home.html", all_teams=all_teams, all_address=all_address)

@home_blueprint.route("/profile/", methods=["GET", "POST"])
# @cache.cached(timeout=60*15, key_prefix="user_profile")
@roles_accepted("player", "bookie")
@login_required
def profile():
    
    all_teams = all_nfl_teams()
    num_pending = count_pending_bets()
    num_graded = count_graded_bets()
    user = Users.query.filter_by(id=current_user.id).one()
    ou = NFLOverUnderBet.query.filter((NFLOverUnderBet.user_id==user.id) | (NFLOverUnderBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).all()
    sb = NFLSideBet.query.filter((NFLSideBet.user_id==user.id) | (NFLSideBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).all()
    ml = NFLMLBet.query.filter((NFLMLBet.user_id==user.id) | (NFLMLBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).all()
    graded_sb = NFLSideBet.query.filter((NFLSideBet.user_id==user.id) | (NFLSideBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=True, paid=True).all()
    graded_ou = NFLOverUnderBet.query.filter((NFLOverUnderBet.user_id==user.id) | (NFLOverUnderBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=True, paid=True).all()
    graded_ml = NFLMLBet.query.filter((NFLMLBet.user_id==user.id) | (NFLMLBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=True, paid=True).all()
    account_info = block_io.get_address_by_label(label=user.username)
    return render_template(
        "profile.html", 
        all_teams=all_teams, 
        user=user, 
        ou=ou,
        sb=sb,
        ml=ml,
        num_pending=num_pending,
        num_graded=num_graded,
        graded_sb=graded_sb,
        graded_ou=graded_ou,
        graded_ml=graded_ml,
        account_info=account_info
        )

@home_blueprint.route("/admin/")
@roles_required("admin")
def admin():
    all_teams = all_nfl_teams()
    return render_template(
        "admin_page.html",
     all_teams=all_teams
     )

