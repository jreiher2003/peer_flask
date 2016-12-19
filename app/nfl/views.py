import sys
import json
import datetime
from datetime import date
import hashlib
from decimal import Decimal
from PIL import Image
from dateutil.parser import parse as parse_date
from app import app, db, cache, block_io
from sqlalchemy import exc
from app.users.models import Users, Role, UserRoles, Profile
from .models import NFLOverUnderBet, NFLSideBet, NFLMLBet, Base
from app.nfl_stats.models import NFLStandings, NFLTeam, NFLStadium, NFLSchedule, NFLScore, NFLTeamSeason
from forms import OverUnderForm, HomeTeamForm, AwayTeamForm, VSForm, DeleteForm
from flask import Blueprint, render_template, url_for, request, redirect,flash, abort
from flask_security import login_required, roles_required, current_user, roles_accepted
from slugify import slugify
from app.home.utils import all_nfl_teams, get_user_wallet
from .utils import team_rush_avg, team_pass_avg, \
opp_team_rush_avg, opp_team_pass_avg, team_off_avg, \
team_def_avg, today_date,today_and_now, make_salt, yesterday, date_to_string

nfl_blueprint = Blueprint("nfl", __name__, template_folder="templates")

@nfl_blueprint.route("/nfl/odds/")
@nfl_blueprint.route("/nfl/home/")
@nfl_blueprint.route("/nfl/")
@nfl_blueprint.route("/")
def nfl_odds():
    dt = datetime.datetime.now()
    date_string = date_to_string(dt)
    sch = NFLSchedule.query.filter(NFLSchedule.SeasonType == 1, NFLSchedule.PointSpread != None).all()
    form_o = OverUnderForm()
    form_h = HomeTeamForm()
    form_a = AwayTeamForm()
    return render_template(
        "nfl_schedule.html", 
        all_teams = all_nfl_teams(), 
        data = sch, 
        dt = dt,
        form_o = form_o,
        form_h = form_h,
        form_a = form_a, 
        )

@nfl_blueprint.route("/nfl/board/")
# @cache.cached(timeout=60*5, key_prefix="nflboard")
def nfl_public_board():
    dt = datetime.datetime.now()
    tb = NFLOverUnderBet.query.filter_by(bet_taken=False).all()
    sb = NFLSideBet.query.filter_by(bet_taken=False).all()
    ml = NFLMLBet.query.filter_by(bet_taken=False).all()
    form_d = DeleteForm()
    form_o = OverUnderForm()
    form_h = HomeTeamForm()
    form_a = AwayTeamForm()
    return render_template(
        "nfl_public_board.html", 
        all_teams = all_nfl_teams(), 
        dt = dt, 
        tb = tb,
        sb = sb,
        ml = ml,
        form_d = form_d,
        form_o = form_o,
        form_h = form_h,
        form_a = form_a
        )

@nfl_blueprint.route("/nfl/board/create/<path:game_key>/", methods=["GET","POST"])
@roles_accepted("player", "bookie")
@login_required
def nfl_create_bet(game_key):
    salt = make_salt()
    admin = "2MzrAiZFY24U1Zqtcf9ZqD1WskKprzYbqi7"
    user1 = Users.query.filter_by(id = current_user.id).one()
    btc_address = user1.bitcoin_wallet.address
    btc_address if btc_address else None
    nfl_game = NFLSchedule.query.filter_by(GameKey = game_key).one()
    h_team = nfl_game.HomeTeam 
    a_team = nfl_game.AwayTeam
    form_o = OverUnderForm()
    form_h = HomeTeamForm()
    form_a = AwayTeamForm()
    if form_o.validate_on_submit():
        network_fees = 0.00060
        amount = float(request.form["amount"])
        print amount, type(amount), "overunder amount"
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
                    total=float(total),
                    amount=amount,
                    bet_key=bet_key,
                    user_id=current_user.id
                    )
                user1.profile.bets_created += 1
                db.session.add_all([user1,bet_o])
                db.session.commit()
                cache.delete("nflboard")
                cache.delete("user_profile")
                flash("%s, You just created a bet between %s taking %s%s risking <i class='fa fa-btc' aria-hidden='true'></i> %s to win <i class='fa fa-btc' aria-hidden='true'></i> %s." % (current_user.username, bet_o.vs, bet_o.over_under, bet_o.total, bet_o.amount, bet_o.amount_win), "success")
                return redirect(url_for('nfl.nfl_public_board'))
            else:
                flash("There was a problem. Your bet did NOT go through.  <a href='/nfl/schedule/'>Go back</a> and try again", "danger")
                return render_template("nfl_error.html")
        else:
            flash("You don't have enough money in your account to make this bet", "danger")
            return redirect(url_for('nfl.nfl_create_bet', game_key=game_key))

    elif form_a.validate_on_submit():
        network_fees = 0.00060
        amount = float(request.form["amount"])
        print amount, type(amount), "away"
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
                    ps=float(away_ps),
                    amount=amount,
                    bet_key=bet_key,
                    user_id=current_user.id)
                user1.profile.bets_created += 1
                db.session.add_all([user1,bet_a])
                db.session.commit()
                cache.delete("nflboard")
                cache.delete("user_profile")
                flash("%s, You just created a bet between %s taking %s %s risking <i class='fa fa-btc' aria-hidden='true'></i> %s to win <i class='fa fa-btc' aria-hidden='true'></i> %s." % (current_user.username, bet_a.vs, bet_a.team, bet_a.ps_format, bet_a.amount, bet_a.amount_win), "success")
                return redirect(url_for('nfl.nfl_public_board', bet_key=bet_key))
            else:
                flash("There was a problem. Your bet did NOT go through.  <a href='/nfl/schedule/'>Go back</a> and try again", "danger")
                return render_template("nfl_error.html")
        else:
            flash("You don't have enough money in your account to make this bet", "danger")
            return redirect(url_for('nfl.nfl_create_bet', game_key=game_key))

    elif form_h.validate_on_submit():
        network_fees = 0.00060
        amount = float(request.form["amount"])
        print amount, type(amount), "home"
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
                    ps=float(home_ps),
                    vs=away+" vs "+"@"+home,
                    amount=amount,
                    bet_key=bet_key,
                    user_id=current_user.id)
                user1.profile.bets_created += 1
                db.session.add_all([user1,bet_h])
                db.session.commit()
                cache.delete("nflboard")
                cache.delete("user_profile")
                flash("%s, You just created a bet between %s taking %s %s risking <i class='fa fa-btc' aria-hidden='true'></i> %s to win <i class='fa fa-btc' aria-hidden='true'></i> %s." % (current_user.username, bet_h.vs, bet_h.team, bet_h.ps_format, bet_h.amount, bet_h.amount_win), "success")
                return redirect(url_for('nfl.nfl_public_board', bet_key=bet_key))
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
        if nfl:
            a_team = nfl.vs.split("vs")[0].strip()
            h_team = nfl.vs.split("@")[1].strip()
            form = OverUnderForm(obj=nfl)
            if form.validate_on_submit():
                nfl.amount = form.amount.data
                network_fees = 0.00060
                if (float(nfl.amount)+network_fees) <= float(user.bitcoin_wallet.available_btc):
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
        if nfl:
            a_team = nfl.vs.split("vs")[0].strip()
            h_team = nfl.vs.split("@")[1].strip()
            if nfl.team == nfl.home_team:
                form = HomeTeamForm(obj=nfl)
                if form.validate_on_submit():
                    nfl.amount = form.amount.data
                    network_fees = 0.00060
                    if (float(nfl.amount)+network_fees) <= float(user.bitcoin_wallet.available_btc):
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
                    nfl.amount = form.amount.data
                    network_fees = 0.00060
                    if (float(nfl.amount)+network_fees) <= float(user.bitcoin_wallet.available_btc):
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
    form_d = DeleteForm()
    return render_template(
        "nfl_edit_bet.html", 
        all_teams = all_nfl_teams(),
        nfl = nfl,
        h_team = h_team,
        a_team = a_team,
        form = form,
        form_d = form_d,
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
    form = DeleteForm()
    user = Users.query.filter_by(id=nfl.user_id).one()
    if nfl:
        if form.validate_on_submit():
            user.profile.bets_created -= 1
            db.session.delete(nfl)
            db.session.add_all([user])
            db.session.commit()
            cache.clear()
            flash("%s, you just deleted the bet you made between <u>%s</u> for %s BTC" % (nfl.users.username,nfl.vs,nfl.amount), "danger")
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
    default = "2MzrAiZFY24U1Zqtcf9ZqD1WskKprzYbqi7" 
    bc = bet_creator.bitcoin_wallet.address
    bt = bet_taker.bitcoin_wallet.address
    nonce = make_salt(length=32)
    nonce1 = make_salt(length=32)
    bc_amount = float(nfl.amount) 
    bt_amount = float(nfl.amount)
    form = VSForm()
    if form.validate_on_submit():
        print bc_amount, type(bc_amount)
        print bt_amount, type(bt_amount)
        nflamount = float(nfl.amount)
        if float(bet_taker.bitcoin_wallet.available_btc) >= (nflamount+.0002) and float(bet_creator.bitcoin_wallet.available_btc) >= (nflamount+.0002):
            try:
                network_fees = block_io.get_network_fee_estimate(amounts = (nfl.amount), from_addresses = (bc), to_addresses = (default), priority="low")
                network_fees = float(network_fees["data"]["estimated_network_fee"])
                taken_network_fees = block_io.get_network_fee_estimate(amounts = (nfl.amount), from_addresses = (bt), to_addresses = (default), priority="low")
                taken_network_fees = float(taken_network_fees["data"]["estimated_network_fee"])
                nfl.bet_taken = True
                nfl.taken_by = current_user.id 
                nfl.taken_username = current_user.username 
                nfl.network_fees = Decimal(network_fees)
                nfl.taken_network_fees = Decimal(taken_network_fees)
                bet_creator.profile.bets_taken += 1
                bet_creator.profile.pending += Decimal(nflamount)
                bet_taker.profile.bets_taken += 1
                bet_taker.profile.pending += Decimal(nflamount)
                bc = bet_creator.bitcoin_wallet.address
                bt = bet_taker.bitcoin_wallet.address
                block_io.withdraw_from_addresses(amounts = bc_amount, from_addresses = bc, to_addresses = default, priority="low", nonce=nonce)
                block_io.withdraw_from_addresses(amounts = bt_amount, from_addresses = bt, to_addresses = default, priority="low", nonce=nonce1)
                db.session.add_all([bet_taker, bet_creator, nfl])
                db.session.commit()
                cache.clear()
                flash("%s, You have action" % current_user.username,  "success")
                return redirect(url_for("nfl.nfl_confirm_live_action", bet_key=bet_key))
            except Exception:
                print sys.exc_info()[1],"payment error"
        else:
            flash("You or your opponent don't have enough money in their account to make this bet.  This is for your protection. Please check your balance/pending and try again!", "danger")
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


@nfl_blueprint.route("/nfl/standings/")
@cache.cached(timeout=60*5, key_prefix="nfl_season_standings")
def nfl_standings():
    afc_east = NFLStandings.query.filter_by(Conference="AFC",Division="East").all()
    afc_north = NFLStandings.query.filter_by(Conference="AFC",Division="North").all()
    afc_south = NFLStandings.query.filter_by(Conference="AFC",Division="South").all()
    afc_west = NFLStandings.query.filter_by(Conference="AFC",Division="West").all() 
    nfc_east = NFLStandings.query.filter_by(Conference="NFC",Division="East").all()
    nfc_north = NFLStandings.query.filter_by(Conference="NFC",Division="North").all()
    nfc_south = NFLStandings.query.filter_by(Conference="NFC",Division="South").all()
    nfc_west = NFLStandings.query.filter_by(Conference="NFC",Division="West").all()
    return render_template(
        "nfl_standings/nfl standings.html", 
        all_teams = all_nfl_teams(),
        afc_east = afc_east,
        afc_north = afc_north,
        afc_south = afc_south,
        afc_west = afc_west,
        nfc_east = nfc_east,
        nfc_north = nfc_north,
        nfc_south = nfc_south,
        nfc_west = nfc_west 
        )

@nfl_blueprint.route("/nfl/stats/<int:sid>/")
def nfl_stats(sid): 
    teamseason1 = NFLTeamSeason.query.filter_by(SeasonType=sid).all()
    return render_template(
        "nfl_stats.html", 
        all_teams = all_nfl_teams(), 
        teamseason = teamseason1,
        )







