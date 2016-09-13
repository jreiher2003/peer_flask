from app import app, db 

from flask import Blueprint, render_template

users_blueprint = Blueprint("users", __name__, template_folder="templates")

@users_blueprint.route("/login/", methods=["GET","POST"])
def login():
    return render_template("login.html")


@users_blueprint.route("/register/", methods=["GET","POST"])
def register():
    return render_template("register.html")

@users_blueprint.route("/logout/")
def logout():
    return render_template("logout.html")

