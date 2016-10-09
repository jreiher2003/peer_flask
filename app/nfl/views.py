import json
import datetime
from datetime import date
import hashlib
from dateutil.parser import parse as parse_date
from app import app, db
from sqlalchemy import exc
from app.users.models import Users, Role, UserRoles, Profile
from .models import NFLOverUnderBet, NFLSideBet, NFLMLBet, Base
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
    teams = NFLTeam.query.all()
    return list(teams)

@nfl_blueprint.route("/nfl/home/")
@nfl_blueprint.route("/nfl/")
def nfl_home():
    all_teams = all_nfl_teams()
    return render_template("nfl_home.html", all_teams=all_teams)

@nfl_blueprint.route("/nfl/standings/")
def nfl_standings():
    all_teams = all_nfl_teams()
    st = NFLStandings.query.all()
    return render_template("nfl_standings/nfl standings.html", standing=st, all_teams=all_teams)

@nfl_blueprint.route("/nfl/schedule/")
def nfl_schedule():
    all_teams = all_nfl_teams()
    dt = datetime.datetime.now()
    sch = NFLSchedule.query.filter(NFLSchedule.SeasonType == 1, NFLSchedule.PointSpread != None).all()
    return render_template(
        "nfl_schedule.html", 
        all_teams=all_teams, 
        data=sch, 
        dt=dt,
        )

@nfl_blueprint.route("/nfl/stats/<int:sid>/")
def nfl_stats(sid):
    all_teams = all_nfl_teams()
    teamseason1 = NFLTeamSeason.query.filter_by(SeasonType=sid).all()
    return render_template(
        "nfl_stats.html", 
        all_teams=all_teams, 
        teamseason=teamseason1,
        )

@nfl_blueprint.route("/nfl/board/")
def nfl_public_board():
    all_teams = all_nfl_teams()
    dt = datetime.datetime.now()
    tb = NFLOverUnderBet.query.filter_by(bet_taken=False).all()
    sb = NFLSideBet.query.filter_by(bet_taken=False).all()
    ml = NFLMLBet.query.filter_by(bet_taken=False).all()
    return render_template(
        "nfl_public_board.html", 
        all_teams=all_teams, 
        dt=dt, 
        tb=tb,
        sb=sb,
        ml=ml
        )

@nfl_blueprint.route("/nfl/board/create/<path:game_key>/", methods=["GET","POST"])
@login_required
def nfl_create_bet(game_key):
    all_teams = all_nfl_teams()
    salt = make_salt()
    profile1 = Profile.query.filter_by(user_id=current_user.id).one()
    nfl_game = NFLSchedule.query.filter_by(GameKey = game_key).one()
    h_team = nfl_game.HomeTeam 
    a_team = nfl_game.AwayTeam
    form_o = OverUnderForm()
    form_h = HomeTeamForm()
    form_a = AwayTeamForm()
    if form_o.validate_on_submit():
        game_key_form = request.form["game_key"]
        home = request.form["home_"]
        away = request.form["away_"]
        over_under = request.form["over_under"]
        total = request.form["total"]
        amount = request.form["amount"]
        bet_key= ""
        bet_key += hashlib.md5(game_key_form+home+away+total+over_under+amount+salt).hexdigest()
        if nfl_game.AwayTeam == away and nfl_game.HomeTeam == home and nfl_game.GameKey == game_key_form:
            bet_o = NFLOverUnderBet(
                game_key=game_key_form, 
                game_date=parse_date(nfl_game.Date), 
                over_under=over_under,
                vs=away+" vs "+"@"+home,
                home_team = home,
                away_team = away,
                total=total,
                amount=amount,
                bet_key=bet_key,
                user_id=current_user.id
                )
            
            profile1.bets_created += 1
            db.session.add(profile1)
            db.session.add(bet_o)
            db.session.commit()
            return redirect(url_for('nfl.nfl_confirm_bet', bet_key=bet_key))
        else:
            flash("There was a problem. Your bet did NOT go through.  <a href='/nfl/schedule/'>Go back</a> and try again", "danger")
            return render_template("nfl_error.html")

    elif form_a.validate_on_submit():
        game_key_form = request.form["game_key"]
        home = request.form["home_"]
        away = request.form["away_"]
        awayteam = request.form["away_team"]
        away_ps = request.form["point_spread"]
        amount = request.form["amount"]
        bet_key = ""
        bet_key += hashlib.md5(game_key_form+home+away+awayteam+away_ps+amount+salt).hexdigest()
        if nfl_game.AwayTeam == away and nfl_game.HomeTeam == home and nfl_game.GameKey == game_key_form:
            bet_h = NFLSideBet(
                game_key=game_key_form,
                game_date=parse_date(nfl_game.Date),
                team=awayteam,
                home_team = home,
                away_team = away,
                vs=away+" vs "+"@"+home,
                ps=away_ps,
                amount=amount,
                bet_key=bet_key,
                user_id=current_user.id)
            db.session.add(bet_h)
            profile1.bets_created += 1
            db.session.add(profile1)
            db.session.commit()
            return redirect(url_for('nfl.nfl_confirm_bet', bet_key=bet_key))
        else:
            flash("There was a problem. Your bet did NOT go through.  <a href='/nfl/schedule/'>Go back</a> and try again", "danger")
            return render_template("nfl_error.html")

    elif form_h.validate_on_submit():
        game_key_form = request.form["game_key"]
        home = request.form["home_"]
        away = request.form["away_"]
        hometeam = request.form["home_team"]
        home_ps = request.form["point_spread"]
        amount = request.form["amount"]
        bet_key = ""
        bet_key += hashlib.md5(game_key_form+home+away+hometeam+home_ps+amount+salt).hexdigest()
        if nfl_game.AwayTeam == away and nfl_game.HomeTeam == home and nfl_game.GameKey == game_key_form:
            bet_h = NFLSideBet(
                game_key=game_key_form,
                game_date=parse_date(nfl_game.Date),
                home_team = home,
                away_team = away,
                team=hometeam,
                ps=home_ps,
                vs=away+" vs "+"@"+home,
                amount=amount,
                bet_key=bet_key,
                user_id=current_user.id)
            db.session.add(bet_h)
            profile1.bets_created += 1
            db.session.add(profile1)
            db.session.commit()
            return redirect(url_for('nfl.nfl_confirm_bet', bet_key=bet_key))
        else:
            flash("There was a problem. Your bet did NOT go through.  <a href='/nfl/schedule/'>Go back</a> and try again", "danger")
            return render_template("nfl_error.html")
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
        nfl_bet = NFLSideBet.query.filter_by(bet_key=bet_key).one()
    except exc.SQLAlchemyError:
        print "No Side Bets"
    try:
        nfl_bet = NFLOverUnderBet.query.filter_by(bet_key=bet_key).one()
    except exc.SQLAlchemyError:
        print "No Over Under bets"

    return render_template('nfl_confirm.html', nfl_bet=nfl_bet, all_teams=all_teams)
    
@nfl_blueprint.route("/nfl/bet/<path:bet_key>/edit/", methods=["GET","POST"])
def nfl_edit_bet(bet_key):
    all_teams = all_nfl_teams()
    try:
        nfl = NFLOverUnderBet.query.filter_by(bet_key=bet_key).one()
        if nfl is not None:
            a_team = nfl.vs.split("vs")[0].strip()
            h_team = nfl.vs.split("@")[1].strip()
            form = OverUnderForm(obj=nfl)
            if form.validate_on_submit():
                nfl.amount = form.amount.data
                nfl.over_under = form.over_under.data
                nfl.total =  form.total.data
                db.session.add(nfl)
                db.session.commit()
                flash("%s you just edited <u>%s</u>. BetKey: %s" % (nfl.users.username,nfl.vs,nfl.bet_key),"info")
                return redirect(url_for("nfl.nfl_public_board"))
    except exc.SQLAlchemyError:
        print "No over under bets"
    try:
        nfl = NFLSideBet.query.filter_by(bet_key=bet_key).one()
        if nfl is not None:
            a_team = nfl.vs.split("vs")[0].strip()
            h_team = nfl.vs.split("@")[1].strip()
            if nfl.ps and nfl.team == nfl.home_team:
                form = HomeTeamForm(obj=nfl)
                if form.validate_on_submit():
                    nfl.amount = form.amount.data
                    nfl.ps = form.point_spread.data
                    db.session.add(nfl)
                    db.session.commit()
                    flash("%s you just edited <u>%s</u>. BetKey: %s" % (nfl.users.username,nfl.vs,nfl.bet_key),"info")
                    return redirect(url_for("nfl.nfl_public_board"))
            elif nfl.ps and nfl.team == nfl.away_team:
                form = AwayTeamForm(obj=nfl)
                if form.validate_on_submit():
                    nfl.amount = form.amount.data
                    nfl.ps = form.point_spread.data
                    db.session.add(nfl)
                    db.session.commit()
                    flash("%s you just edited <u>%s</u>. BetKey: %s" % (nfl.users.username,nfl.vs,nfl.bet_key),"info")
                    return redirect(url_for("nfl.nfl_public_board"))
    except exc.SQLAlchemyError:
        print "No side bets"
    return render_template(
        "nfl_edit_bet.html", 
        all_teams=all_teams,
        nfl=nfl,
        h_team=h_team,
        a_team=a_team,
        form = form,
        bet_key=bet_key
        )

@nfl_blueprint.route("/nfl/bet/<path:bet_key>/delete/", methods=["GET","POST"])
@login_required
def nfl_delete_bet(bet_key):
    all_teams = all_nfl_teams()
    try:
        nfl = NFLOverUnderBet.query.filter_by(bet_key=bet_key).one_or_none()
    except exc.SQLAlchemyError:
        print "No Over Under Bets"
    try:
        nfl = NFLSideBet.query.filter_by(bet_key=bet_key).one()
    except exc.SQLAlchemyError:
        print "No Side Bets"
    form = OverUnderForm()
    if nfl is not None:
        if request.method == "POST":
            db.session.delete(nfl)
            db.session.commit()
            flash("%s, you just deleted the bet you made between <u>%s</u> for $%s" % (nfl.users.username,nfl.vs,nfl.amount), "danger")
            return redirect(url_for("nfl.nfl_public_board"))
    return render_template("nfl_delete_bet.html", nfl=nfl, form=form, all_teams=all_teams)


@nfl_blueprint.route("/nfl/bet/action/<path:bet_key>/", methods=["GET","POST"])
def nfl_bet(bet_key):
    all_teams = all_nfl_teams()
    try:
        nfl = NFLOverUnderBet.query.filter_by(bet_key=bet_key).one()
    except exc.SQLAlchemyError:
        print "No OverUnder bets"
    try:
        nfl = NFLSideBet.query.filter_by(bet_key=bet_key).one()
    except exc.SQLAlchemyError:
        print "No side bets"
    profile_taker = Profile.query.filter_by(user_id=current_user.id).one()
    profile_bet_creator = Profile.query.filter_by(user_id=nfl.users.id).one() 
    if request.method == "POST":
        nfl.bet_taken = True
        nfl.taken_by = current_user.id 
        profile_bet_creator.bets_taken += 1
        profile_taker.bets_taken += 1
        db.session.add_all([profile_taker,profile_bet_creator,nfl])
        db.session.commit()
        flash("%s, You have action" % current_user.username,  "success")
        return redirect(url_for("nfl.nfl_confirm_take_bet", bet_key=bet_key))
    return render_template("nfl_bet.html", all_teams=all_teams, nfl=nfl)

@nfl_blueprint.route("/nfl/bet/action/<path:bet_key>/confirm/")
def nfl_confirm_take_bet(bet_key):
    try:
        live_bet = NFLOverUnderBet.query.filter_by(bet_key=bet_key).one()
    except exc.SQLAlchemyError:
        print "No OverUnder Bets"
    try:
        live_bet = NFLSideBet.query.filter_by(bet_key=bet_key).one()
    except exc.SQLAlchemyError:
        print "No Side Bets"
    return render_template("nfl_confirm_take_bet.html", live_bet=live_bet)


@nfl_blueprint.route("/nfl/team/home/<int:sid>/<path:key>/<path:team>/")
def nfl_team_home(sid,key,team):
    all_teams = all_nfl_teams()
    dt = today_and_now()
    dt_plus_2h = dt - datetime.timedelta(hours=4)
    jj = NFLTeam.query.filter_by(Key=key).one()
    tt = NFLStadium.query.filter_by(StadiumID=jj.StadiumID).one() 
    ss = NFLStandings.query.filter_by(Team=key).one()
    tss = NFLTeamSeason.query.filter_by(Team=key, SeasonType=sid).one()
    ts = NFLSchedule.query.filter_by(SeasonType=sid).filter((NFLSchedule.AwayTeam==key) | (NFLSchedule.HomeTeam==key))
    team_score = NFLScore.query.filter_by(SeasonType=sid).filter((NFLScore.AwayTeam==key) | (NFLScore.HomeTeam==key))
    team_rush_rank = team_rush_avg(tss.RushingYards,tss.Team, sid) 
    team_pass_rank = team_pass_avg(tss.PassingYards,tss.Team, sid) 
    opp_team_rush_rank = opp_team_rush_avg(tss.OpponentRushingYards,tss.Team, sid) 
    opp_team_pass_rank = opp_team_pass_avg(tss.OpponentPassingYards,tss.Team, sid) 
    team_off_rank = team_off_avg(tss.OffensiveYards,tss.Team, sid)
    team_def_rank = team_def_avg(tss.OpponentOffensiveYards,tss.Team, sid) 
    return render_template(
        "nfl_team/nfl_team_home.html",
        all_teams=all_teams,
        team_rush_rank=team_rush_rank,
        team_pass_rank=team_pass_rank,
        opp_team_rush_rank=opp_team_rush_rank,
        opp_team_pass_rank=opp_team_pass_rank,
        team_off_rank=team_off_rank,
        team_def_rank=team_def_rank,
        team_score=team_score,
        dt_plus_2h=dt_plus_2h,
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








