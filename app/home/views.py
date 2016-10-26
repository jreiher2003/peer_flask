import json
from dateutil.parser import parse as parse_date
from app import app, db, cache, block_io, bcrypt, uploaded_photos
from flask_uploads import UploadNotAllowed
from flask import request, flash, redirect, url_for
from sqlalchemy import exc
from flask_security import login_required, roles_required, roles_accepted, current_user
from app.users.models import Users, Profile, BitcoinWallet, UserRoles
from app.users.forms import BitcoinWalletForm, BitcoinWithdrawlForm, ProfileForm, SendEmailConfirmForm, ChangePasswordForm
from app.nfl_stats.models import NFLTeam, NFLScore
from app.nfl.models import NFLBetGraded, NFLOverUnderBet, NFLSideBet, NFLMLBet
from app.nfl.utils import make_salt
from flask import Blueprint, render_template
from .utils import all_nfl_teams, grade_query, count_pending_bets, count_graded_bets, ou, sb, ml, graded_sb, graded_ou, graded_ml, get_user_wallet
from app.users.utils import profile_confirm_email, email_reset_notice

home_blueprint = Blueprint("home", __name__, template_folder="templates")
 
@home_blueprint.route("/", methods=["GET","POST"])
def home():
    all_address = block_io.get_my_addresses()
    print current_user.has_role("admin")
    return render_template(
        "home.html",
        all_teams = all_nfl_teams(),
        all_address = all_address
        )

@home_blueprint.route("/profile/", methods=["GET", "POST"])
@cache.cached(timeout=60*5, key_prefix="user_profile")
@login_required
def profile():
    user = Users.query.filter_by(id=current_user.id).one() 
    form_p = ProfileForm(obj=user)
    form_w = BitcoinWithdrawlForm()
    form_c = BitcoinWalletForm()
    form = SendEmailConfirmForm(obj=user)
    form_cp = ChangePasswordForm()
    return render_template(
        "profile/profile.html", 
        all_teams = all_nfl_teams(), 
        form = form,
        form_cp = form_cp,
        form_c = form_c,
        form_w = form_w,
        form_p = form_p,
        ou = ou(),
        sb = sb(),
        ml = ml(),
        num_pending = count_pending_bets(),
        num_graded = count_graded_bets(),
        graded_sb = graded_sb(),
        graded_ou = graded_ou(),
        graded_ml = graded_ml(),
        )

@home_blueprint.route("/profile_update/", methods=["POST"])
@login_required
def update_profile():
    user = Users.query.filter_by(id=current_user.id).one()
    form = SendEmailConfirmForm(obj=user)
    form_cp = ChangePasswordForm()
    form_p = ProfileForm(obj=user)
    form_w = BitcoinWithdrawlForm()
    form_c = BitcoinWalletForm()
    if form_p.validate_on_submit():
        avatar = request.files["avatar"]
        username = request.form["username"]
        email = request.form["email"]
        if avatar:
            try:
                avatar = uploaded_photos.save(avatar)
                user.profile.avatar = avatar
                user.username = username
                user.email = email
                db.session.add_all([user])
                db.session.commit()
                flash("Successful update", "warning")
                cache.delete("update_profile")
                return redirect(url_for('home.profile'))
            except UploadNotAllowed:
                flash("The upload was not allowed")
        else:
            user.username = username
            user.email = email
            db.session.add(user)
            db.session.commit()
            flash("Successful update", "warning")
            cache.delete("update_profile")
            return redirect(url_for('home.profile'))
    return render_template(
        "profile/profile.html", 
        all_teams = all_nfl_teams(), 
        form_c = form_c,
        form_w = form_w,
        form_p = form_p,
        form = form,
        form_cp = form_cp,
        ou = ou(),
        sb = sb(),
        ml = ml(),
        num_pending = count_pending_bets(),
        num_graded = count_graded_bets(),
        graded_sb = graded_sb(),
        graded_ou = graded_ou(),
        graded_ml = graded_ml(),
        ) 

@home_blueprint.route("/bitcoin_widthdrawl/", methods=["POST"])
@login_required
def bitcoin_widthdrawl():
    nonce = make_salt(length=32)
    form_w = BitcoinWithdrawlForm()
    if form_w.validate_on_submit():
        amount = request.form["amount"]
        address = request.form["address"]
        print amount,address, type(amount),type(address)
        print current_user.bitcoin_wallet.address, type(current_user.bitcoin_wallet.address)
        try: 
            block_io.withdraw_from_addresses(amounts = float(amount), from_addresses = str(current_user.bitcoin_wallet.address), to_addresses = str(address), priority="low", nonce=nonce)
            flash("You just send this amount of bitcoins %s BTC - to this address %s" % (address,amount), "info")
            cache.delete("user_profile")
            return redirect(url_for("home.profile"))
        except:
            print "Something went wrong"

    user = Users.query.filter_by(id=current_user.id).one()
    form_p = ProfileForm(obj=user)
    return render_template(
        "profile/profile.html", 
        all_teams = all_nfl_teams(), 
        form_w = form_w,
        form_p = form_p,
        ou = ou(),
        sb = sb(),
        ml = ml(),
        num_pending = count_pending_bets(),
        num_graded = count_graded_bets(),
        graded_sb = graded_sb(),
        graded_ou = graded_ou(),
        graded_ml = graded_ml(),
        ) 

@home_blueprint.route("/create_bitcoin/", methods=["POST"])
@login_required
def create_bitcoin():
    form_c = BitcoinWalletForm()
    if form_c.validate_on_submit():
        try:
            btc = block_io.get_new_address() 
            wallet = BitcoinWallet(label=btc["data"]["label"], address=btc["data"]["address"], user_id=current_user.id)
            db.session.add(wallet)
            db.session.commit()
            cache.delete("user_profile")
            flash("Just created a new Bitcoin Wallet, Now Make a deposit and start playing!", "success")
            return redirect(url_for("home.profile"))
        except exc.SQLAlchemyError:
            print "some thing else happend"

@home_blueprint.route("/change-password/", methods=["GET","POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(id=current_user.id).first()
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            user.password = form.new_password.data
            db.session.add(user)
            db.session.commit()
            referer = request.headers["Referer"]
            email_reset_notice(user.email)
            flash("Successfully changed your password", "success")
            return redirect(url_for("home.profile"))
    return render_template("security/change_password.html", form=form)

#if user doesn't confirm on register
@home_blueprint.route("/confirm-email/", methods=["GET","POST"])
@login_required
def profile_c_email():
    user = Users.query.filter_by(id=current_user.id).one()
    form = SendEmailConfirmForm(obj=user)
    if form.validate_on_submit():
        profile_confirm_email(user.email)
        flash("An email was send to %s" % user.email, "info")
        return redirect(url_for('home.profile'))
    return render_template("security/send_confirmation.html", form=form) 

#app.user.home.views.profile_c_email
@home_blueprint.route('/confirm/<token>/')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = Users.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_at = datetime.datetime.now()
        user_roles = UserRoles(user_id=user.id, role_id=2)
        db.session.add_all([user, user_roles])
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('home.profile'))
