import json
from app import app, db 
from flask import request
from flask_security import login_required, roles_required, current_user
from app.users.models import Users 
from app.nfl_stats.models import NFLTeam 

from flask import Blueprint, render_template

home_blueprint = Blueprint("home", __name__, template_folder="templates")

def all_nfl_teams():
    return NFLTeam.query.all()

@home_blueprint.route("/", methods=["GET","POST"])
def home():
    all_teams = all_nfl_teams()
    return render_template("home.html", all_teams=all_teams)

@home_blueprint.route("/profile/")
@login_required
def profile():
    all_teams = all_nfl_teams()
    user = Users.query.filter_by(id=current_user.id).one()
    return render_template("profile.html", user=user, all_teams=all_teams)

@home_blueprint.route("/admin/")
@roles_required("admin")
def admin():
    all_teams = all_nfl_teams()
    return "Admin page"

