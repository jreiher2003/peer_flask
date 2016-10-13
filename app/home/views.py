import json
from dateutil.parser import parse as parse_date
from app import app, db, cache, block_io
from flask import request, flash, redirect, url_for
from sqlalchemy import exc
from flask_security import login_required, roles_required, roles_accepted, current_user
from app.users.models import Users, Profile, BitcoinWallet 
from app.users.forms import BitcoinWalletForm
from app.nfl_stats.models import NFLTeam, NFLScore
from app.nfl.models import NFLBetGraded, NFLOverUnderBet, NFLSideBet, NFLMLBet
from flask import Blueprint, render_template
from .utils import all_nfl_teams, grade_query, count_pending_bets, count_graded_bets, ou, sb, ml, graded_sb, graded_ou, graded_ml, get_user_wallet

home_blueprint = Blueprint("home", __name__, template_folder="templates")
 
@home_blueprint.route("/", methods=["GET","POST"])
def home():
    all_address = block_io.get_my_addresses()
    return render_template(
        "home.html",
        all_teams = all_nfl_teams(),
        all_address = all_address
        )

@home_blueprint.route("/profile/", methods=["GET", "POST"])
# @cache.cached(timeout=60*15, key_prefix="user_profile")
@roles_accepted("player", "bookie")
@login_required
def profile():
    wallet = get_user_wallet()
    form = BitcoinWalletForm()
    if form.validate_on_submit():
        try:
            wallet = BitcoinWallet.query.filter_by(user_id=current_user.id).one()
            btc = block_io.get_new_address()
            print btc
            if wallet is not None:
                wallet.label = btc["data"]["label"]
                wallet.address = btc["data"]["address"]
                db.session.add(wallet)
                db.session.commit()
                cache.delete("user_profile")
                flash("edited wallet", "success")
                return redirect(url_for("home.profile"))
        except exc.SQLAlchemyError:
            print "Need to create a wallet first" 
        try:
            btc = block_io.get_new_address() 
            wallet = BitcoinWallet(label=btc["data"]["label"], address=btc["data"]["address"], user_id=current_user.id)
            db.session.add(wallet)
            db.session.commit()
            cache.delete("user_profile")
            flash("created a New wallet fresh", "success")
            return redirect(url_for("home.profile"))
        except exc.SQLAlchemyError:
            print "some thing else happend"
    return render_template(
        "profile.html", 
        all_teams = all_nfl_teams(), 
        wallet = wallet,
        form = form,
        ou = ou(),
        sb = sb(),
        ml = ml(),
        num_pending = count_pending_bets(),
        num_graded = count_graded_bets(),
        graded_sb = graded_sb(),
        graded_ou = graded_ou(),
        graded_ml = graded_ml(),
        )

@home_blueprint.route("/admin/")
@roles_required("admin")
def admin():
    return render_template(
        "admin_page.html",
     all_teams = all_nfl_teams(),
     )

