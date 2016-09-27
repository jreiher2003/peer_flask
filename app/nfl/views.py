import json
import datetime
from datetime import date
import hashlib
from dateutil.parser import parse as parse_date
from app import app, db
from app.users.models import Users, Role, UserRoles, Profile
from .models import OverUnderBet, HomeTeamBet, AwayTeamBet
from app.nfl_stats.models import NFLStandings, NFLTeam, NFLStadium, NFLSchedule, NFLScore, NFLTeamSeason
from forms import OverUnderForm, HomeTeamForm, AwayTeamForm
from flask import Blueprint, render_template, url_for, request, redirect,flash, abort
from flask_security import login_required, roles_required, current_user
from slugify import slugify
from .utils import team_rush_avg, team_pass_avg, \
opp_team_rush_avg, opp_team_pass_avg, team_off_avg, \
team_def_avg, today_date,today_and_now, make_salt, yesterday


nfl_blueprint = Blueprint("nfl", __name__, template_folder="templates")

def all_nfl_teams():
    return NFLTeam.query.all()

@nfl_blueprint.route("/nfl/home/")
@nfl_blueprint.route("/nfl/")
def nfl_home():
    all_teams = all_nfl_teams()
    return render_template("nfl_home.html", all_teams=all_teams)

@nfl_blueprint.route("/nfl/schedule/")
def nfl_schedule():
    all_teams = all_nfl_teams()
    dt = datetime.datetime.today()
    yesterday1 = yesterday()
    sch = NFLSchedule.query.filter(db.and_(NFLSchedule.SeasonType == 1), (NFLSchedule.PointSpread != None)).all()
    return render_template(
        "nfl_schedule.html", 
        all_teams=all_teams, 
        data=sch, 
        dt=dt,
        )

@nfl_blueprint.route("/nfl/board/")
def nfl_public_board():
    all_teams = all_nfl_teams()
    over_under = db.session.query(OverUnderBet).order_by("game_key").all()
    home_team = db.session.query(HomeTeamBet).order_by("game_key").all()
    away_team = db.session.query(AwayTeamBet).order_by("game_key").all()
    return render_template(
        "nfl_public_board.html", 
        all_teams=all_teams, 
        over_under=over_under, 
        home_team=home_team,
        away_team=away_team,
        )

@nfl_blueprint.route("/nfl/create/")
@login_required
def nfl_create_broad():
    all_teams = all_nfl_teams()
    return "create reg"

@nfl_blueprint.route("/nfl/board/create/<path:game_key>/over_under/", methods=["POST"])
def post_over_under(game_key):
    all_teams = all_nfl_teams()
    salt = make_salt()
    nfl_game = NFLSchedule.query.filter_by(GameKey = game_key).one()
    h_team = nfl_game.HomeTeam 
    a_team = nfl_game.AwayTeam
    form_o = OverUnderForm()
    form_a = AwayTeamForm()
    form_h = HomeTeamForm()
    if form_o.validate_on_submit():
        game_key_form = request.form["game_key"]
        print game_key_form 
        home = request.form["home"]
        print home
        away = request.form["away"]
        print away
        # if nfl_game1.HomeTeam == home and nfl_game1.AwayTeam == away:
        print nfl_game.AwayTeam 
        print nfl_game.HomeTeam 
        print nfl_game.GameKey
        over_under = request.form["over_under"]
        total = request.form["total"]
        amount = request.form["amount"]
        bet_key= ""
        bet_key += hashlib.md5(total+over_under+amount+salt).hexdigest()
        if nfl_game.AwayTeam == away and nfl_game.HomeTeam == home and nfl_game.GameKey == game_key_form:
            bet_o = OverUnderBet(game_key=game_key_form,over_under=over_under,vs=home + " vs " +away,total=total,amount=amount,bet_key=bet_key,user_id=current_user.id)
            db.session.add(bet_o)
            db.session.commit()
            return redirect(url_for('nfl.nfl_confirm_bet', bet_key=bet_key))
        else:
            return "yo problem"
        
    return render_template(
        "nfl_create_bet.html",
        form_o=form_o,
        form_h=form_h,
        form_a=form_a, 
        nfl_game=nfl_game, 
        all_teams=all_teams,
        h_team=h_team,
        a_team=a_team
        )

@nfl_blueprint.route("/nfl/board/create/<path:game_key>/home_team/", methods=["POST"])
def post_home_team(game_key):
    all_teams = all_nfl_teams()
    salt = make_salt()
    nfl_game = NFLSchedule.query.filter_by(GameKey = game_key).one()
    form_o = OverUnderForm()
    form_a = AwayTeamForm()
    form_h = HomeTeamForm()
    if form_h.validate_on_submit():
        game_key = request.form["game_key"]
        home_team = request.form["home_team"]
        home_ps = request.form["point_spread"]
        amount = request.form["amount"]
        bet_key = ""
        bet_key += hashlib.md5(game_key+home_team+home_ps+amount+salt).hexdigest()
        bet_h = HomeTeamBet(game_key=game_key,home_team=home_team,home_ps=home_ps,amount=amount,bet_key=bet_key,user_id=current_user.id)
        db.session.add(bet_h)
        db.session.commit()
        return redirect(url_for('nfl.nfl_confirm_bet', bet_key=bet_key))
    return render_template(
        "nfl_create_bet.html",
        form_o=form_o,
        form_h=form_h,
        form_a=form_a, 
        nfl_game=nfl_game, 
        all_teams=all_teams
        )
@nfl_blueprint.route("/nfl/board/create/<path:game_key>/away_team/", methods=["POST"])
def post_away_team(game_key):
    all_teams = all_nfl_teams()
    salt = make_salt()
    nfl_game = NFLSchedule.query.filter_by(GameKey = game_key).one()
    form_o = OverUnderForm()
    form_a = AwayTeamForm()
    form_h = HomeTeamForm()
    if form_a.validate_on_submit():
        game_key = request.form["game_key"]
        away_team = request.form["away_team"]
        away_ps = request.form["point_spread"]
        amount = request.form["amount"]
        bet_key = ""
        bet_key += hashlib.md5(game_key+away_team+away_ps+amount+salt).hexdigest()
        bet_h = AwayTeamBet(game_key=game_key,away_team=away_team,away_ps=away_ps,amount=amount,bet_key=bet_key,user_id=current_user.id)
        db.session.add(bet_h)
        db.session.commit()
        return redirect(url_for('nfl.nfl_confirm_bet', bet_key=bet_key))
    return render_template(
        "nfl_create_bet.html",
        form_o=form_o,
        form_h=form_h,
        form_a=form_a, 
        nfl_game=nfl_game, 
        all_teams=all_teams
        )

@nfl_blueprint.route("/nfl/board/create/<path:game_key>/", methods=["GET","POST"])
@login_required
def nfl_create_bet(game_key):
    all_teams = all_nfl_teams()
    nfl_game = NFLSchedule.query.filter_by(GameKey = game_key).one()
    h_team = nfl_game.HomeTeam 
    a_team = nfl_game.AwayTeam
    form_o = OverUnderForm()
    form_h = HomeTeamForm()
    form_a = AwayTeamForm()
    return render_template(
        "nfl_create_bet.html",
        form_o=form_o,
        form_h=form_h,
        form_a=form_a, 
        nfl_game=nfl_game, 
        all_teams=all_teams,
        h_team=h_team,
        a_team=a_team,
        )

@nfl_blueprint.route("/nfl/confirm/<path:bet_key>/", methods=["GET","POST"])
@login_required
def nfl_confirm_bet(bet_key):
    all_teams = all_nfl_teams()
    try:
        nfl_bet = OverUnderBet.query.filter_by(bet_key=bet_key).one()
    except:
        pass
    try:
        nfl_bet = HomeTeamBet.query.filter_by(bet_key=bet_key).one()
    except:
        pass
    try:
        nfl_bet = AwayTeamBet.query.filter_by(bet_key=bet_key).one()
    except:
        pass
    return render_template('nfl_confirm.html', nfl_bet=nfl_bet, all_teams=all_teams)
    
# @nfl_blueprint.route("/nfl/confirm/<path:game_key>/<path:bet_key>/", methods=["GET"])
# @login_required
# def nfl_confirm_redirect(game_key,bet_key):
#     game = [x for x in schedule if x["GameKey"] == game_key]
#     nfl_bet = NflBet.query.filter_by(bet_key=bet_key,game_key=game_key,user_id=current_user.id).one()
#     # flash("just made a bet")
#     return render_template("nfl_confirm.html", game=game, game_key=game_key, nfl_bet=nfl_bet)

@nfl_blueprint.route("/nfl/scores/")
def nfl_scores():
    all_teams = all_nfl_teams()
    return "nfl scores"

@nfl_blueprint.route("/nfl/standings/")
def nfl_standings():
    all_teams = all_nfl_teams()
    st = NFLStandings.query.all()
    return render_template("nfl standings.html", standing=st, all_teams=all_teams)

@nfl_blueprint.route("/nfl/stats/<int:sid>/")
def nfl_stats(sid):
    all_teams = all_nfl_teams()
    teamseason1 = NFLTeamSeason.query.filter_by(SeasonType=sid).all()
    return render_template("nfl_stats.html", all_teams=all_teams, teamseason=teamseason1,)

@nfl_blueprint.route("/nfl/team/home/<int:sid>/<path:key>/<path:team>/")
def nfl_team_home(sid,key,team):
    all_teams = all_nfl_teams()
    dt = today_date()
    jj = NFLTeam.query.filter_by(Key=key).one()
    tt = NFLStadium.query.filter_by(StadiumID=jj.StadiumID).one() 
    ss = NFLStandings.query.filter_by(Team=key).one()
    tss = NFLTeamSeason.query.filter_by(Team=key, SeasonType=1).one()
    ts = NFLSchedule.query.filter_by(SeasonType=sid).filter((NFLSchedule.AwayTeam==key) | (NFLSchedule.HomeTeam==key))
    team_score = NFLScore.query.filter_by(SeasonType=sid).filter((NFLScore.AwayTeam==key) | (NFLScore.HomeTeam==key))
    team_rush_rank = team_rush_avg(tss.RushingYards,tss.Team) 
    team_pass_rank = team_pass_avg(tss.PassingYards,tss.Team) 
    opp_team_rush_rank = opp_team_rush_avg(tss.OpponentRushingYards,tss.Team) 
    opp_team_pass_rank = opp_team_pass_avg(tss.OpponentPassingYards,tss.Team) 
    team_off_rank = team_off_avg(tss.OffensiveYards,tss.Team)
    team_def_rank = team_def_avg(tss.OpponentOffensiveYards,tss.Team) 
    return render_template(
        "nfl_team_home.html",
        all_teams=all_teams,
        team_rush_rank=team_rush_rank,
        team_pass_rank=team_pass_rank,
        opp_team_rush_rank=opp_team_rush_rank,
        opp_team_pass_rank=opp_team_pass_rank,
        team_off_rank=team_off_rank,
        team_def_rank=team_def_rank,
        team_score=team_score,
        dt=dt,
        tt=tt,
        jj=jj,
        ss=ss,
        tss=tss,
        ts=ts
        )

@nfl_blueprint.route("/nfl/team/schedule/<path:team>/")
def nfl_team_schedule(team):
    all_teams = all_nfl_teams()
    return "schedule"

@nfl_blueprint.route("/nfl/team/stats/<path:team>/")
def nfl_team_stats(team):
    all_teams = all_nfl_teams()
    return "stats"






