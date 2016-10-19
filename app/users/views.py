
from app import app, db
from flask import Blueprint, render_template

users_blueprint = Blueprint("users", __name__, template_folder="templates")


