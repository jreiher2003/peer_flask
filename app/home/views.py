import json
from dateutil.parser import parse as parse_date
from app import app, db 
from flask import request
from flask_security import login_required, roles_required, current_user
from app.users.models import Users, Profile 
from app.nfl_stats.models import NFLTeam,NFLScore
from app.nfl.models import NFLcreateBet,NFLBetGraded,NFLtakeBet

from flask import Blueprint, render_template

home_blueprint = Blueprint("home", __name__, template_folder="templates")

def all_nfl_teams():
    return NFLTeam.query.all()

def graded_bets():
    score = db.session.query(NFLScore).filter_by(SeasonType=1).all()
    NFLBetGraded.__table__.drop(db.engine)
    NFLBetGraded.__table__.create(db.engine)
    for x in score:
        grade = NFLBetGraded(game_key=x.GameKey,week = x.Week,game_date=parse_date(x.Date),home_team=x.HomeTeam,home_score=x.HomeScore,away_team=x.AwayTeam,away_score=x.AwayScore,total_score=(x.AwayScore+x.HomeScore),over_under=x.OverUnder,ps=x.PointSpread,cover_total=x.cover_total(),cover_side=x.cover_line())
        db.session.add(grade)
        db.session.commit()

def grade_cb():
    graded_bets()
    graded1 = NFLBetGraded.query.all()
    cb1 = NFLcreateBet.query.all()
    cb = [r for r in cb1]
    grd = [r for r in graded1]
    for g in grd:
        for c in cb:
            if g.game_key == c.game_key:
                if c.over_under == "u" or c.over_under == "o":
                    if c.over_under == g.cover_total:
                        c.win = True
                        c.lose = False
                        c.bet_graded = True
                    else:
                        c.lose = True
                        c.win = False
                        c.bet_graded = True

                if c.ps != None:
                    if c.team == g.cover_side:
                        c.win = True
                        c.lose = False
                        c.bet_graded = True
                    else:
                        c.lose = True
                        c.win = False 
                        c.bet_graded = True
    db.session.add(c)
    db.session.commit()

def grade_tb():
    graded_bets()
    graded1 = NFLBetGraded.query.all()
    cb1 = NFLtakeBet.query.all()
    cb = [r for r in cb1]
    grd = [r for r in graded1]
    for g in grd:
        for c in cb:
            if g.game_key == c.game_key:
                if c.over_under == "u" or c.over_under == "o":
                    if c.over_under == g.cover_total:
                        c.win = True
                        c.lose = False
                        c.bet_graded = True
                    else:
                        c.lose = True
                        c.win = False
                        c.bet_graded = True
                if c.ps != None:
                    if c.team == g.cover_side:
                        c.win = True
                        c.lose = False
                        c.bet_graded = True
                    else:
                        c.lose = True
                        c.win = False 
                        c.bet_graded = True
    db.session.add(c)
    db.session.commit()

def count_wins_losses():
    users1 = Users.query.all()
    users = [r for r in users1] # list of all users id
    for u in users:
        count_wins_c = NFLcreateBet.query.filter_by(user_id=u.id,win=True).count()
        count_losses_c = NFLcreateBet.query.filter_by(user_id=u.id,win=False).count()
        count_wins_t = NFLtakeBet.query.filter_by(user_id=u.id,win=True).count()
        count_losses_t = NFLtakeBet.query.filter_by(user_id=u.id,win=False).count()
        u.profile.wins = (count_wins_c + count_wins_t)
        u.profile.losses = (count_losses_c + count_losses_t)  
    db.session.add(u)
    db.session.commit()

def pay_winners_from_losers():
    users1 = Users.query.all()
    users = list(users1) # list of all users id
    for u in users:
        money1 = NFLcreateBet.query.filter_by(user_id=u.id,bet_taken=True,paid=False).all()
        money = list(money1)
        if money:
            for m in money:
                # print m.amount,m.win,m.lose,u.username,u.profile.d_amount, m.taken_by
                c_profile = Profile.query.filter_by(user_id=m.user_id).one()
                t_profile = Profile.query.filter_by(user_id=m.taken_by).one()
                if m.win == True:
                    print "player %s gets paid from player %s this amount %s" % (m.user_id, m.taken_by, m.amount)
                    c_profile.d_amount += int("%.15g" % m.amount_win())
                    t_profile.d_amount -= m.amount 
                    m.paid = True 
                if m.win == False:
                    print "player %s gets paid from player %s this amount %s" % (m.taken_by, m.user_id, m.amount)
                    t_profile.d_amount += int("%.15g" % m.amount_win())
                    c_profile.d_amount -= m.amount 
                    m.paid = True 
                db.session.add(c_profile)
                db.session.add(t_profile)
            db.session.add(m)
            db.session.commit()
        else:
            print "all bets are paid"

    


@home_blueprint.route("/", methods=["GET","POST"])
def home():
    all_teams = all_nfl_teams()
    return render_template("home.html", all_teams=all_teams)

@home_blueprint.route("/profile/")
@login_required
def profile():
    all_teams = all_nfl_teams()
    grade_cb()
    grade_tb()
    count_wins_losses()
    pay_winners_from_losers()
    user = Users.query.filter_by(id=current_user.id).one()
    pending_bets = NFLcreateBet.query.filter((NFLcreateBet.user_id==user.id) | (NFLcreateBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).all()
    graded_bets = NFLcreateBet.query.filter((NFLcreateBet.user_id==user.id) | (NFLcreateBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=True,paid=True).all()
    
    return render_template("profile.html", user=user, all_teams=all_teams, pending_bets=pending_bets, graded_bets=graded_bets)

@home_blueprint.route("/admin/")
@roles_required("admin")
def admin():
    all_teams = all_nfl_teams()
    return "Admin page"

