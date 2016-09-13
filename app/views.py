import json
import datetime
from app import app, db
from forms import CreateNflBet
from flask import render_template, url_for

with open('Schedule.2016.json') as data_file:    
        data = json.load(data_file)

@app.route("/")
@app.route("/nfl/home/")
def nfl_home():
    return render_template("nfl_home.html")

@app.route("/nfl/schedule/")
def nfl_schedule():
    t = datetime.time()
    d = datetime.date.today()
    dt = datetime.datetime.combine(d,t)
    dn = datetime.datetime.now()
    return render_template("nfl_schedule.html" , data=data, dt=dt, dn=dn)

@app.route("/nfl/board/")
def nfl_public_board():
    return render_template("nfl_public_board.html")

@app.route("/nfl/create/<path:game_key>/")
def nfl_create_bet(game_key):
    for d in data:
        if d['GameKey'] == game_key:
            nfl_game = d
    form = CreateNflBet()
    
    return render_template("nfl_create_bet.html" ,form=form, nfl_game=nfl_game)

@app.route("/profile/")
def profile():
    return render_template("profile.html")

