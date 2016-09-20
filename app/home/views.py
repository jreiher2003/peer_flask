import json
from app import app, db 
from flask import request
from flask_security import login_required, roles_required, current_user
from app.users.models import Users 

from flask import Blueprint, render_template

home_blueprint = Blueprint("home", __name__, template_folder="templates")

@home_blueprint.route("/")
def home():
    return render_template("home.html")

@home_blueprint.route("/profile/")
@login_required
def profile():
    user = Users.query.filter_by(id=current_user.id).one()
    return render_template("profile.html", user=user)

@home_blueprint.route("/admin/")
@roles_required("admin")
def admin():
    return "Admin page"

