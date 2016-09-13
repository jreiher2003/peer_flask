from app import app, db 

from flask import Blueprint, render_template

home_blueprint = Blueprint("home", __name__, template_folder="templates")

@home_blueprint.route("/")
def home():
    return render_template("home.html")

@home_blueprint.route("/profile/")
def profile():
    return render_template("profile.html")