import json
from dateutil.parser import parse as parse_date
from app import app, db, cache 
from flask import request
from flask_security import login_required, roles_required, current_user
from app.users.models import Users, Profile 
from app.nfl_stats.models import NFLTeam, NFLScore
from app.nfl.models import NFLBetGraded, NFLOverUnderBet, NFLSideBet, NFLMLBet
from flask import Blueprint, render_template

home_blueprint = Blueprint("home", __name__, template_folder="templates")

def all_nfl_teams(update=False):
    key = "teams"
    all_teams = cache.get(key)
    if all_teams in None or update:
        all_teams = NFLTeam.query.all()
        all_teams = list(all_teams)
        cache.st(key, all_teams)
    return all_teams 

def graded_bets():
    NFLBetGraded.__table__.drop(db.engine)
    NFLBetGraded.__table__.create(db.engine)
    score1 = db.session.query(NFLScore).filter_by(SeasonType=1).all()
    score = list(score1)
    for x in score:
        grade = NFLBetGraded(game_key=x.GameKey,week = x.Week,game_date=parse_date(x.Date),home_team=x.HomeTeam,home_score=x.HomeScore,away_team=x.AwayTeam,away_score=x.AwayScore,total_score=(x.AwayScore+x.HomeScore),over_under=x.OverUnder,ps=x.PointSpread,cover_total=x.cover_total(),cover_side=x.cover_line(),cover_ml=x.cover_ml())
        db.session.add(grade)
        db.session.commit()

def grade_tb():
    graded_bets()
    graded1 = NFLBetGraded.query.all()
    cb1 = NFLOverUnderBet.query.filter_by(bet_taken=True).all()
    cb = list(cb1)
    grd = list(graded1)
    if cb:
        for g in grd:
            for c in cb:
                if g.game_key == c.game_key:
                    if c.over_under == g.cover_total:
                        c.win = True
                        c.lose = False
                        c.bet_graded = True
                    else:
                        c.lose = True
                        c.win = False
                        c.bet_graded = True
        db.session.add(c)
        db.session.commit()
    else:
        return None

def grade_sb():
    graded_bets()
    graded1 = NFLBetGraded.query.all()
    cb1 = NFLSideBet.query.filter_by(bet_taken=True).all()
    cb = list(cb1)
    grd = list(graded1)
    if cb:
        for g in grd:
            for c in cb:
                if g.game_key == c.game_key:
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
    else:
        return None

def grade_ml():
    graded_bets()
    graded1 = NFLBetGraded.query.all()
    cb1 = NFLMLBet.query.filter_by(bet_taken=True).all()
    cb = list(cb1)
    grd = list(graded1)
    if cb:
        for g in grd:
            for c in cb:
                if g.game_key == c.game_key:
                    if c.team == g.cover_ml:
                        c.win = True
                        c.lose = False
                        c.bet_graded = True
                    else:
                        c.lose = True
                        c.win = False 
                        c.bet_graded = True
        db.session.add(c)
        db.session.commit()
    else:
        return None

def count_wins_losses_user_id(id, ct):
    """
    counts total wins or losses for user_id. ct=True is for wins. ct=False is for losses.  ct=True,win==win, ct=False,win==loss
    """
    ml = NFLMLBet.query.filter_by(user_id=id,win=ct,bet_taken=True).count()
    tb = NFLOverUnderBet.query.filter_by(user_id=id,win=ct,bet_taken=True).count()
    sb = NFLSideBet.query.filter_by(user_id=id,win=ct,bet_taken=True).count()
    return (ml+tb+sb)

def count_wins_losses_taken_by(id, ct):
    """
    counts total wins or losses for taken_by. ct=False is for wins. ct=True is for losses.  ct=False,win==win, ct=True,win==loss
    """
    ml = NFLMLBet.query.filter_by(taken_by=id,win=ct,bet_taken=True).count()
    tb = NFLOverUnderBet.query.filter_by(taken_by=id,win=ct,bet_taken=True).count()
    sb = NFLSideBet.query.filter_by(taken_by=id,win=ct,bet_taken=True).count()
    return (ml+tb+sb)

def update_profile_w(uid):
    """ updates all users Profile wins by uid """
    profile = Profile.query.filter_by(user_id=uid).one()
    profile.wins = (count_wins_losses_taken_by(uid, False) + count_wins_losses_user_id(uid,True)) # just counts wins
    db.session.add(profile)
    db.session.commit()

def update_profile_l(uid):
    """ updates all users Profile by losses by uid """
    profile = Profile.query.filter_by(user_id=uid).one()
    profile.losses = count_wins_losses_user_id(uid,False) + count_wins_losses_taken_by(uid, True) # just counts losses
    db.session.add(profile)
    db.session.commit()

def update_users_wins_losses():
    users1 = Users.query.all()
    users = list(users1)
    for u in users:
        update_profile_w(u.id)
        update_profile_l(u.id)  

def pay_winners_from_losers():
    users1 = Users.query.all()
    users = list(users1) # list of all users id
    for u in users:
        sb1 = NFLSideBet.query.filter_by(user_id=u.id,bet_taken=True,paid=False).all()
        sb = list(sb1)
        ou1 = NFLOverUnderBet.query.filter_by(user_id=u.id,bet_taken=True,paid=False).all()
        ou = list(ou1)
        ml1 = NFLMLBet.query.filter_by(user_id=u.id,bet_taken=True,paid=False).all()
        ml = list(ml1)
        if sb:
            for ss in sb:
                c_profile = Profile.query.filter_by(user_id=ss.user_id).one()
                t_profile = Profile.query.filter_by(user_id=ss.taken_by).one()
                if ss.win == True:
                    print "player %s gets paid from player %s this amount %s" % (ss.user_id, ss.taken_by, ss.amount)
                    c_profile.d_amount += ss.amount_win
                    t_profile.d_amount -= ss.amount 
                    ss.paid = True 
                if ss.win == False:
                    print "player %s gets paid from player %s this amount %s" % (ss.taken_by, ss.user_id, ss.amount)
                    t_profile.d_amount += ss.amount_win
                    c_profile.d_amount -= ss.amount 
                    ss.paid = True 
                db.session.add(c_profile)
                db.session.add(t_profile)
            db.session.add(ss)
            db.session.commit()
        if ou:
            for oo in ou:
                c_profile = Profile.query.filter_by(user_id=oo.user_id).one()
                t_profile = Profile.query.filter_by(user_id=oo.taken_by).one()
                if oo.win == True:
                    print "player %s gets paid from player %s this amount %s" % (oo.user_id, oo.taken_by, oo.amount)
                    c_profile.d_amount += oo.amount_win
                    t_profile.d_amount -= oo.amount 
                    oo.paid = True 
                if oo.win == False:
                    print "player %s gets paid from player %s this amount %s" % (oo.taken_by, oo.user_id, oo.amount)
                    t_profile.d_amount += oo.amount_win
                    c_profile.d_amount -= oo.amount 
                    oo.paid = True 
                db.session.add(c_profile)
                db.session.add(t_profile)
            db.session.add(oo)
            db.session.commit()
        if ml:
            for ll in ml:
                c_profile = Profile.query.filter_by(user_id=ll.user_id).one()
                t_profile = Profile.query.filter_by(user_id=ll.taken_by).one()
                if ll.win == True:
                    print "player %s gets paid from player %s this amount %s" % (ll.user_id, ll.taken_by, ll.amount)
                    c_profile.d_amount += ll.amount_win
                    t_profile.d_amount -= ll.amount 
                    ll.paid = True 
                if ll.win == False:
                    print "player %s gets paid from player %s this amount %s" % (ll.taken_by, ll.user_id, ll.amount)
                    t_profile.d_amount += ll.amount_win
                    c_profile.d_amount -= ll.amount 
                    ll.paid = True 
                db.session.add(c_profile)
                db.session.add(t_profile)
            db.session.add(ll)
            db.session.commit()

def count_pending_bets():
    user = Users.query.filter_by(id=current_user.id).one()
    ou = NFLOverUnderBet.query.filter((NFLOverUnderBet.user_id==user.id) | (NFLOverUnderBet.taken_by==user.id)).filter_by(bet_taken=True,bet_graded=False).count()
    sb = NFLSideBet.query.filter((NFLSideBet.user_id==user.id) | (NFLSideBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).count()
    ml = NFLMLBet.query.filter((NFLMLBet.user_id==user.id) | (NFLMLBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).count()
    return (ou+sb+ml)

def count_graded_bets():
    user = Users.query.filter_by(id=current_user.id).one()
    graded_sb = NFLSideBet.query.filter((NFLSideBet.user_id==user.id) | (NFLSideBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=True,paid=True).count()
    graded_ou = NFLOverUnderBet.query.filter((NFLOverUnderBet.user_id==user.id) | (NFLOverUnderBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=True,paid=True).count()
    graded_ml = NFLMLBet.query.filter((NFLMLBet.user_id==user.id) | (NFLMLBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=True,paid=True).count()
    return (graded_sb+graded_ou+graded_ml)


@home_blueprint.route("/", methods=["GET","POST"])
def home():
    all_teams = all_nfl_teams()
    return render_template("home.html", all_teams=all_teams)

@home_blueprint.route("/profile/")
@login_required
def profile():
    all_teams = all_nfl_teams()
    grade_sb()
    grade_tb()
    grade_ml()
    update_users_wins_losses()
    pay_winners_from_losers()
    num_pending = count_pending_bets()
    num_graded = count_graded_bets()
    user = Users.query.filter_by(id=current_user.id).one()
    ou = NFLOverUnderBet.query.filter((NFLOverUnderBet.user_id==user.id) | (NFLOverUnderBet.taken_by==user.id)).filter_by(bet_taken=True,bet_graded=False).all()
    sb = NFLSideBet.query.filter((NFLSideBet.user_id==user.id) | (NFLSideBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).all()
    ml = NFLMLBet.query.filter((NFLMLBet.user_id==user.id) | (NFLMLBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).all()
    graded_sb = NFLSideBet.query.filter((NFLSideBet.user_id==user.id) | (NFLSideBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=True,paid=True).all()
    graded_ou = NFLOverUnderBet.query.filter((NFLOverUnderBet.user_id==user.id) | (NFLOverUnderBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=True,paid=True).all()
    graded_ml = NFLMLBet.query.filter((NFLMLBet.user_id==user.id) | (NFLMLBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=True,paid=True).all()
    return render_template(
        "profile.html", 
        all_teams=all_teams, 
        user=user, 
        ou=ou,
        sb=sb,
        ml=ml,
        num_pending=num_pending,
        num_graded=num_graded,
        graded_sb=graded_sb,
        graded_ou=graded_ou,
        graded_ml=graded_ml
        )

@home_blueprint.route("/admin/")
@roles_required("admin")
def admin():
    all_teams = all_nfl_teams()
    return "Admin page"

