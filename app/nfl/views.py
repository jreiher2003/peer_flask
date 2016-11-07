import sys
import json
import datetime
from datetime import date
import hashlib
from dateutil.parser import parse as parse_date
from app import app, db, cache, block_io
from sqlalchemy import exc
from app.users.models import Users, Role, UserRoles, Profile
from .models import NFLOverUnderBet, NFLSideBet, NFLMLBet, Base
from app.nfl_stats.models import NFLStandings, NFLTeam, NFLStadium, NFLSchedule, NFLScore, NFLTeamSeason
from forms import OverUnderForm, HomeTeamForm, AwayTeamForm, VSForm
from flask import Blueprint, render_template, url_for, request, redirect,flash, abort
from flask_security import login_required, roles_required, current_user, roles_accepted
from slugify import slugify
from app.home.utils import all_nfl_teams, get_user_wallet
from .utils import team_rush_avg, team_pass_avg, \
opp_team_rush_avg, opp_team_pass_avg, team_off_avg, \
team_def_avg, today_date,today_and_now, make_salt, yesterday

nfl_blueprint = Blueprint("nfl", __name__, template_folder="templates")

@nfl_blueprint.route("/nfl/home/")
@nfl_blueprint.route("/nfl/")
def nfl_home():
    return render_template(
        "nfl_home.html", 
        all_teams = all_nfl_teams(),
        )

@nfl_blueprint.route("/nfl/standings/")
@cache.cached(timeout=60*5, key_prefix="nfl_season_standings")
def nfl_standings():
    st = NFLStandings.query.all()
    return render_template(
        "nfl_standings/nfl standings.html", 
        all_teams = all_nfl_teams(),
        standing = st, 
        )

@nfl_blueprint.route("/nfl/schedule/")
def nfl_schedule():
    dt = datetime.datetime.now()
    sch = NFLSchedule.query.filter(NFLSchedule.SeasonType == 1, NFLSchedule.PointSpread != None).all()
    return render_template(
        "nfl_schedule.html", 
        all_teams = all_nfl_teams(), 
        data = sch, 
        dt = dt,
        )

@nfl_blueprint.route("/nfl/stats/<int:sid>/")
def nfl_stats(sid): 
    teamseason1 = NFLTeamSeason.query.filter_by(SeasonType=sid).all()
    return render_template(
        "nfl_stats.html", 
        all_teams = all_nfl_teams(), 
        teamseason = teamseason1,
        )

@nfl_blueprint.route("/nfl/board/")
# @cache.cached(timeout=60*5, key_prefix="nflboard")
def nfl_public_board():
    dt = datetime.datetime.now()
    tb = NFLOverUnderBet.query.filter_by(bet_taken=False).all()
    sb = NFLSideBet.query.filter_by(bet_taken=False).all()
    ml = NFLMLBet.query.filter_by(bet_taken=False).all()
    return render_template(
        "nfl_public_board.html", 
        all_teams = all_nfl_teams(), 
        dt = dt, 
        tb = tb,
        sb = sb,
        ml = ml
        )

@nfl_blueprint.route("/nfl/board/create/<path:game_key>/", methods=["GET","POST"])
@roles_accepted("player", "bookie")
@login_required
# we have to check to see if bet_creator has enough bitcoins in their account to proceed.
def nfl_create_bet(game_key):
    salt = make_salt()
    admin = "2MzrAiZFY24U1Zqtcf9ZqD1WskKprzYbqi7"
    user1 = Users.query.filter_by(id = current_user.id).one()
    btc_address = user1.bitcoin_wallet.address
    btc_address if btc_address is not None else None
    nfl_game = NFLSchedule.query.filter_by(GameKey = game_key).one()
    h_team = nfl_game.HomeTeam 
    a_team = nfl_game.AwayTeam
    form_o = OverUnderForm()
    form_h = HomeTeamForm()
    form_a = AwayTeamForm()
    if form_o.validate_on_submit():
        amount = float(request.form["amount"])
        network_fees = block_io.get_network_fee_estimate(amounts = (amount), from_addresses = (btc_address), to_addresses = (admin), priority="low")
        network_fees = float(network_fees["data"]["estimated_network_fee"])
        if float(amount+network_fees) <= float(user1.bitcoin_wallet.available_btc): 
            game_key_form = request.form["game_key"]
            home = request.form["home_"]
            away = request.form["away_"]
            over_under = request.form["over_under"]
            total = request.form["total"]
            bet_key= ""
            bet_key += hashlib.md5(game_key_form+home+away+total+over_under+str(amount)+salt).hexdigest()
            if nfl_game.AwayTeam == away and nfl_game.HomeTeam == home and nfl_game.GameKey == game_key_form:
                bet_o = NFLOverUnderBet(
                    game_key=game_key_form, 
                    game_date=parse_date(nfl_game.Date), 
                    vs=away+" vs "+"@"+home,
                    home_team = home,
                    away_team = away,
                    over_under=over_under,
                    total=total,
                    amount=float(amount),
                    bet_key=bet_key,
                    user_id=current_user.id
                    )
                user1.profile.bets_created += 1
                db.session.add_all([user1,bet_o])
                db.session.commit()
                cache.delete("nflboard")
                cache.delete("user_profile")
                flash("%s, You just created a bet between %s taking %s%s risking <i class='fa fa-btc' aria-hidden='true'></i> %s to win <i class='fa fa-btc' aria-hidden='true'></i> %s." % (current_user.username, bet_o.vs, bet_o.over_under, bet_o.total, bet_o.amount, bet_o.amount*.9), "success")
                return redirect(url_for('nfl.nfl_confirm_create_bet', bet_key=bet_key))
            else:
                flash("There was a problem. Your bet did NOT go through.  <a href='/nfl/schedule/'>Go back</a> and try again", "danger")
                return render_template("nfl_error.html")
        else:
            flash("You don't have enough money in your account to make this bet", "danger")
            return redirect(url_for('nfl.nfl_create_bet', game_key=game_key))

    elif form_a.validate_on_submit():
        amount = float(request.form["amount"])
        network_fees = block_io.get_network_fee_estimate(amounts = (amount), from_addresses = (btc_address), to_addresses = (admin), priority="low")
        network_fees = float(network_fees["data"]["estimated_network_fee"])
        if float(amount+network_fees) <= float(user1.bitcoin_wallet.available_btc): 
            game_key_form = request.form["game_key"]
            home = request.form["home_"]
            away = request.form["away_"]
            awayteam = request.form["away_team"]
            away_ps = request.form["point_spread"]
            bet_key = ""
            bet_key += hashlib.md5(game_key_form+home+away+awayteam+away_ps+str(amount)+salt).hexdigest()
            if nfl_game.AwayTeam == away and nfl_game.HomeTeam == home and nfl_game.GameKey == game_key_form:
                bet_a = NFLSideBet(
                    game_key=game_key_form,
                    game_date=parse_date(nfl_game.Date),
                    team=awayteam,
                    home_team = home,
                    away_team = away,
                    vs=away+" vs "+"@"+home,
                    ps=away_ps,
                    amount=float(amount),
                    bet_key=bet_key,
                    user_id=current_user.id)
                user1.profile.bets_created += 1
                db.session.add_all([user1,bet_a])
                db.session.commit()
                cache.delete("nflboard")
                cache.delete("user_profile")
                flash("%s, You just created a bet between %s taking %s %s risking <i class='fa fa-btc' aria-hidden='true'></i> %s to win <i class='fa fa-btc' aria-hidden='true'></i> %s." % (current_user.username, bet_a.vs, bet_a.team, bet_a.ps_format, bet_a.amount, bet_a.amount*.9), "success")
                return redirect(url_for('nfl.nfl_confirm_create_bet', bet_key=bet_key))
            else:
                flash("There was a problem. Your bet did NOT go through.  <a href='/nfl/schedule/'>Go back</a> and try again", "danger")
                return render_template("nfl_error.html")
        else:
            flash("You don't have enough money in your account to make this bet", "danger")
            return redirect(url_for('nfl.nfl_create_bet', game_key=game_key))

    elif form_h.validate_on_submit():
        amount = float(request.form["amount"])
        network_fees = block_io.get_network_fee_estimate(amounts = (amount), from_addresses = (btc_address), to_addresses = (admin), priority="low")
        network_fees = float(network_fees["data"]["estimated_network_fee"])
        if float(amount+network_fees) <= float(user1.bitcoin_wallet.available_btc): 
            game_key_form = request.form["game_key"]
            home = request.form["home_"]
            away = request.form["away_"]
            hometeam = request.form["home_team"]
            home_ps = request.form["point_spread"]
            bet_key = ""
            bet_key += hashlib.md5(game_key_form+home+away+hometeam+home_ps+str(amount)+salt).hexdigest()
            if nfl_game.AwayTeam == away and nfl_game.HomeTeam == home and nfl_game.GameKey == game_key_form:
                bet_h = NFLSideBet(
                    game_key=game_key_form,
                    game_date=parse_date(nfl_game.Date),
                    home_team = home,
                    away_team = away,
                    team=hometeam,
                    ps=home_ps,
                    vs=away+" vs "+"@"+home,
                    amount=float(amount),
                    bet_key=bet_key,
                    user_id=current_user.id)
                user1.profile.bets_created += 1
                db.session.add_all([user1,bet_h])
                db.session.commit()
                cache.delete("nflboard")
                cache.delete("user_profile")
                flash("%s, You just created a bet between %s taking %s %s risking <i class='fa fa-btc' aria-hidden='true'></i> %s to win <i class='fa fa-btc' aria-hidden='true'></i> %s." % (current_user.username, bet_h.vs, bet_h.team, bet_h.ps_format, bet_h.amount, bet_h.amount*.9), "success")
                return redirect(url_for('nfl.nfl_confirm_create_bet', bet_key=bet_key))
            else:
                flash("There was a problem. Your bet did NOT go through.  <a href='/nfl/schedule/'>Go back</a> and try again", "danger")
                return render_template("nfl_error.html")
        else:
            flash("You don't have enough money in your account to make this bet", "danger")
            return redirect(url_for('nfl.nfl_create_bet', game_key=game_key))
    return render_template(
        "create_bet/nfl_create_bet.html",
        all_teams = all_nfl_teams(),
        form_o = form_o,
        form_h = form_h,
        form_a = form_a, 
        nfl_game = nfl_game, 
        h_team = h_team,
        a_team = a_team,
        )

@nfl_blueprint.route("/nfl/confirm/<path:bet_key>/", methods=["GET","POST"])
@roles_accepted("player", "bookie")
@login_required
def nfl_confirm_create_bet(bet_key):
    try:
        nfl_bet = NFLSideBet.query.filter_by(bet_key=bet_key).one()
    except Exception:
        print sys.exc_info()[1], "SideBet"
    try:
        nfl_bet = NFLOverUnderBet.query.filter_by(bet_key=bet_key).one()
    except Exception:
        print sys.exc_info()[1], "OverUnderBet"
    return render_template(
        'nfl_confirm_create_bet.html', 
        nfl_bet = nfl_bet, 
        all_teams = all_nfl_teams(),
        )
    
@nfl_blueprint.route("/nfl/bet/<path:bet_key>/edit/", methods=["GET","POST"])
@roles_accepted("player", "bookie")
@login_required
def nfl_edit_bet(bet_key):
    admin = "2MzrAiZFY24U1Zqtcf9ZqD1WskKprzYbqi7"
    user = Users.query.filter_by(id=current_user.id).one()
    btc_address = user.bitcoin_wallet.address 
    try:
        nfl = NFLOverUnderBet.query.filter_by(bet_key=bet_key).one()
        if nfl is not None:
            a_team = nfl.vs.split("vs")[0].strip()
            h_team = nfl.vs.split("@")[1].strip()
            form = OverUnderForm(obj=nfl)
            if form.validate_on_submit():
                nfl.amount = float(form.amount.data)
                network_fees = block_io.get_network_fee_estimate(amounts = (nfl.amount), from_addresses = (btc_address), to_addresses = (admin), priority="low")
                network_fees = float(network_fees["data"]["estimated_network_fee"])
                if float(nfl.amount+network_fees) <= float(user.bitcoin_wallet.available_btc):
                    nfl.over_under = form.over_under.data
                    nfl.total =  form.total.data
                    db.session.add(nfl)
                    db.session.commit()
                    cache.delete("nflboard")
                    flash("%s you just edited <u>%s</u>. BetKey: %s" % (nfl.users.username,nfl.vs,nfl.bet_key),"info")
                    return redirect(url_for("nfl.nfl_public_board"))
                else:
                    flash("You don't have enough money in your account to make this bet", "danger")
                    return redirect(url_for('nfl.nfl_edit_bet', bet_key=bet_key))
    except Exception:
        print sys.exc_info()[1], "OverUnderBet"
    try:
        nfl = NFLSideBet.query.filter_by(bet_key=bet_key).one() 
        if nfl is not None:
            a_team = nfl.vs.split("vs")[0].strip()
            h_team = nfl.vs.split("@")[1].strip()
            if nfl.team == nfl.home_team:
                form = HomeTeamForm(obj=nfl)
                if form.validate_on_submit():
                    nfl.amount = float(form.amount.data)
                    network_fees = block_io.get_network_fee_estimate(amounts = (nfl.amount), from_addresses = (btc_address), to_addresses = (admin), priority="low")
                    network_fees = float(network_fees["data"]["estimated_network_fee"])
                    if float(nfl.amount+network_fees) <= float(user.bitcoin_wallet.available_btc):
                        nfl.ps = form.point_spread.data
                        db.session.add(nfl)
                        db.session.commit()
                        cache.delete("nflboard")
                        flash("%s you just edited <u>%s</u>. BetKey: %s" % (nfl.users.username,nfl.vs,nfl.bet_key),"info")
                        return redirect(url_for("nfl.nfl_public_board"))
                    else:
                        flash("You don't have enough money in your account to make this bet", "danger")
                        return redirect(url_for('nfl.nfl_edit_bet', bet_key=bet_key))
            elif nfl.team == nfl.away_team:
                form = AwayTeamForm(obj=nfl)
                if form.validate_on_submit():
                    nfl.amount = float(form.amount.data)
                    network_fees = block_io.get_network_fee_estimate(amounts = (nfl.amount), from_addresses = (btc_address), to_addresses = (admin), priority="low")
                    network_fees = float(network_fees["data"]["estimated_network_fee"])
                    if float(nfl.amount+network_fees) <= float(user.bitcoin_wallet.available_btc):
                        nfl.ps = form.point_spread.data
                        db.session.add(nfl)
                        db.session.commit()
                        cache.delete("nflboard")
                        flash("%s you just edited <u>%s</u>. BetKey: %s" % (nfl.users.username,nfl.vs,nfl.bet_key),"info")
                        return redirect(url_for("nfl.nfl_public_board"))
                    else:
                        flash("You don't have enough money in your account to make this bet", "danger")
                        return redirect(url_for('nfl.nfl_edit_bet', bet_key=bet_key))
    except Exception:
        print sys.exc_info()[1], "SideBet"
    return render_template(
        "nfl_edit_bet.html", 
        all_teams = all_nfl_teams(),
        nfl = nfl,
        h_team = h_team,
        a_team = a_team,
        form = form,
        bet_key = bet_key
        )

@nfl_blueprint.route("/nfl/bet/<path:bet_key>/delete/", methods=["GET","POST"])
@roles_accepted("player", "bookie")
@login_required
def nfl_delete_bet(bet_key):
    try:
        nfl = NFLOverUnderBet.query.filter_by(bet_key=bet_key).one()
    except Exception:
        print sys.exc_info()[1], "OverUnderBet"
    try:
        nfl = NFLSideBet.query.filter_by(bet_key=bet_key).one()
    except Exception:
        print sys.exc_info()[1], "SideBet"
    form = OverUnderForm()
    user = Users.query.filter_by(id=nfl.user_id).one()
    if nfl is not None:
        if request.method == "POST":
            user.profile.bets_created -= 1
            db.session.delete(nfl)
            db.session.add_all([user])
            db.session.commit()
            cache.delete("nflboard")
            cache.delete("user_profile")
            flash("%s, you just deleted the bet you made between <u>%s</u> for $%s" % (nfl.users.username,nfl.vs,nfl.amount), "danger")
            return redirect(url_for("nfl.nfl_public_board"))
    return render_template(
        "nfl_delete_bet.html", 
        all_teams = all_nfl_teams(),
        nfl = nfl, 
        form = form, 
        )

@nfl_blueprint.route("/nfl/bet/action/<path:bet_key>/", methods=["GET","POST"])
@roles_accepted("player", "bookie")
@login_required
def nfl_bet_vs_bet(bet_key):
    try:
        nfl = NFLOverUnderBet.query.filter_by(bet_key=bet_key).one()
    except Exception:
        print sys.exc_info()[1], "OverUnderBet"
    try:
        nfl = NFLSideBet.query.filter_by(bet_key=bet_key).one()
    except Exception:
        print sys.exc_info()[1], "SideBets"
    bet_taker = Users.query.filter_by(id=current_user.id).one()
    bet_creator = Users.query.filter_by(id=nfl.users.id).one() 
    default = "2MzrAiZFY24U1Zqtcf9ZqD1WskKprzYbqi7" # default block_io address
    bc = bet_creator.bitcoin_wallet.address
    bt = bet_taker.bitcoin_wallet.address
    nonce = make_salt(length=32)
    nonce1 = make_salt(length=32)
    bc_amount = nfl.amount 
    bt_amount = nfl.amount 
    form = VSForm()
    if form.validate_on_submit():
        #form validate on submit
        network_fees = block_io.get_network_fee_estimate(amounts = (nfl.amount), from_addresses = (bc), to_addresses = (bt), priority="low")
        network_fees = float(network_fees["data"]["estimated_network_fee"])
        if float(bet_taker.bitcoin_wallet.available_btc) >= float(nfl.amount+network_fees) and float(bet_creator.bitcoin_wallet.available_btc) >= float(nfl.amount+network_fees):
            # check again if balances are enough to cover bets 
            nfl.bet_taken = True
            nfl.taken_by = current_user.id 
            nfl.taken_username = current_user.username 
            bet_creator.profile.bets_taken += 1
            bet_creator.profile.pending += (nfl.amount+network_fees)
            bet_taker.profile.bets_taken += 1
            bet_taker.profile.pending += (nfl.amount+network_fees)
            bc = bet_creator.bitcoin_wallet.address
            bt = bet_taker.bitcoin_wallet.address
            # we have to check to see if profile_taker and profile_bet_creator have enough bitcoins in their account to proceed.
            try:
                block_io.withdraw_from_addresses(amounts = bc_amount, from_addresses = bc, to_addresses = default, priority="low", nonce=nonce)
                block_io.withdraw_from_addresses(amounts = bt_amount, from_addresses = bt, to_addresses = default, priority="low", nonce=nonce1)
                db.session.add_all([bet_taker, bet_creator, nfl])
                db.session.commit()
                cache.clear()
                flash("%s, You have action" % current_user.username,  "success")
                return redirect(url_for("nfl.nfl_confirm_live_action", bet_key=bet_key))
            except Exception:
                print sys.exc_info()[1],"payment error"
                 
            # url = "/nfl/bet/action/%s/" % bet_key
            # base = "http://localhost:8600"
            # print base + url 
            # post_url = base + url
            # print block_io.create_notification(type="address", address = bc, url = post_url)
        else:
            flash("You or your opponent don't have enough money in their account to make this bet.  This is for your protection.", "danger")
            return redirect(url_for('nfl.nfl_edit_bet', bet_key=bet_key))
    return render_template(
        "nfl_vs_bet.html", 
        all_teams = all_nfl_teams(), 
        nfl = nfl,
        form = form,
        )

@nfl_blueprint.route("/nfl/bet/action/<path:bet_key>/confirm/")
@login_required
def nfl_confirm_live_action(bet_key):
    try:
        live_bet = NFLOverUnderBet.query.filter_by(bet_key=bet_key).one()
    except Exception:
        print sys.exc_info()[1], "OverUnderBet"
    try:
        live_bet = NFLSideBet.query.filter_by(bet_key=bet_key).one()
    except Exception:
        print sys.exc_info()[1], "SideBet"
    return render_template(
        "nfl_confirm_live_action.html",
        all_teams = all_nfl_teams(), 
        live_bet = live_bet)


@nfl_blueprint.route("/nfl/team/home/<int:sid>/<path:key>/<path:team>/")
def nfl_team_home(sid,key,team):
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
        all_teams = all_nfl_teams(),
        team_rush_rank = team_rush_rank,
        team_pass_rank = team_pass_rank,
        opp_team_rush_rank = opp_team_rush_rank,
        opp_team_pass_rank = opp_team_pass_rank,
        team_off_rank = team_off_rank,
        team_def_rank = team_def_rank,
        team_score = team_score,
        dt_plus_2h = dt_plus_2h,
        dt = dt,
        tt = tt,
        jj = jj,
        ss = ss,
        tss = tss,
        ts = ts
        )


@nfl_blueprint.route("/nfl/team/schedule/<path:team>/")
def nfl_team_schedule(team):
    all_teams = all_nfl_teams()
    return "schedule"

@nfl_blueprint.route("/nfl/team/stats/<path:team>/")
def nfl_team_stats(team):
    all_teams = all_nfl_teams()
    return "stats"








