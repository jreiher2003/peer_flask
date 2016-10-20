import datetime
from app import app, db, bcrypt 
from .models import Users
from .forms import LoginForm, RegisterForm, RecoverPasswordForm, ChangePasswordForm, ChangePasswordTokenForm
from .utils import get_ip, is_safe_url, generate_confirmation_token, confirm_token, send_email, password_reset_email
from flask import Blueprint, render_template, url_for, request, flash, redirect, session
from flask_login import login_user, logout_user, login_required, current_user 

users_blueprint = Blueprint("users", __name__, template_folder="templates")

@users_blueprint.route("/login/", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            remember = form.remember.data
            login_user(user,remember)
            user.login_count += 1
            user.last_login_ip = user.current_login_ip
            user.last_login_at = user.current_login_at
            user.current_login_ip = get_ip()
            user.current_login_at = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            next = request.args.get("next")
            if not is_safe_url(next):
                return flask.abort(400)
            return redirect(next or url_for("nfl.nfl_home"))
        else:
            flash("<strong>Invalid password.</strong> Please try again.", "danger")
            return redirect(url_for("users.login"))
    return render_template("security/login_user.html", form=form)

@users_blueprint.route("/register/", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Users(
            username = form.username.data,
            email = form.email.data,
            password = bcrypt.generate_password_hash(form.password.data),
            login_count = 1,
            current_login_ip = get_ip(),
            current_login_at = datetime.datetime.now()
            )
        try:
            db.session.add(user)
            db.session.commit()
            token = generate_confirmation_token(user.email)
            confirm_url = url_for('users.confirm_email', token=token, _external=True)
            html = render_template("security/email/welcome.html", confirm_url=confirm_url, user=user)
            subject = "Please confirm your email"
            send_email(user.email, subject, html)
            login_user(user,True)
           
            flash("Welcome <strong>%s</strong> to Peer2Peer. A confirmation email has been sent to %s" % (user.username,user.email), "success")
            next = request.args.get("next")
            print "next", next 
            if not is_safe_url(next):
                return flask.abort(400)
            return redirect(next or url_for("nfl.nfl_home"))
        except:
            flash("That username already exists", "danger")
            return redirect(url_for("users.register"))
    return render_template(
        "security/register_user.html",  
        form=form
        )

@users_blueprint.route("/logout/")
@login_required
def logout():
    logout_user()
    session.pop("logged_in", None)
    session.pop("session", None)
    flash("You have logged out.", "danger")
    referer = request.headers["Referer"]
    return redirect(referer)

@users_blueprint.route("/change-password/", methods=["GET","POST"])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(id=current_user.id).first()
        if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
            user.password = bcrypt.generate_password_hash(form.new_password.data)
            db.session.add(user)
            db.session.commit()
            referer = request.headers["Referer"]
            flash("Successfully changed your password", "success")
            return redirect(url_for("home.profile"))
    return render_template("security/change_password.html", form=form)

@users_blueprint.route('/confirm/<token>/')
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
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('home.profile'))

@users_blueprint.route("/forgot-password/", methods=["GET","POST"])
def forgot_password():
    form = RecoverPasswordForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data, confirmed=True).one_or_none()
        if user is not None:
            password_reset_email(user.email)
            flash("sent email to %s" % user.email, "warning")
            return redirect(url_for("users.login"))
        else:
            flash("this account is not confirmed", "danger")
            return redirect(url_for("users.login"))
    return render_template("security/forgot_password.html", form=form)

@users_blueprint.route("/password-reset/<token>/", methods=["GET","POST"])
def forgot_password_reset_token(token):
    try:
        email = confirm_token(token)
        print email
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = Users.query.filter_by(email=email).one_or_none()
    print user.username
    
    form = ChangePasswordTokenForm()
    if request.method == "POST": 
        user.password = bcrypt.generate_password_hash(request.form["password"])
        db.session.add(user)
        db.session.commit()
        flash("Successful password updated!", "success")
        return redirect(url_for("users.login"))
    
    return render_template("security/forgot_password_change.html", form=form, token=token)

