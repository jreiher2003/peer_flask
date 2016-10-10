from app import app, db, cache 
from flask_security import current_user
from app.nfl_stats.models import NFLTeam 
from app.nfl.models import NFLBetGraded, NFLSideBet, NFLOverUnderBet, NFLMLBet
from app.users.models import Users, Profile

def all_nfl_teams(update=False):
    key = "teams"
    all_teams = cache.get(key)
    if all_teams is None or update:
        all_teams = NFLTeam.query.all()
        all_teams = list(all_teams)
        cache.set(key, all_teams)
    return all_teams

#################################################################################
## this group of functions updates all the bet tables with wins loses or pushes
## win is True, lose is False, push is None
@cache.cached(timeout=30, key_prefix="grading_query")
def grade_query(update=True):
    return NFLBetGraded.query.all() 

def grade_tb():
    """ this function updates all NFLOverUnderBet table with correct win booleans
    Also marks bet graded.  grade_query is a cache of NFLBetGraded table.  
    """ 
    cb1 = NFLOverUnderBet.query.filter_by(bet_taken=True, bet_graded=False).all()
    cb = list(cb1)
    grd = grade_query()
    if cb:
        for g in grd:
            for c in cb:
                if g.game_key == c.game_key:
                    if g.cover_total == "Push":
                        c.win == None
                        c.bet_graded = True
                    elif g.cover_total == c.over_under:
                        c.win = True
                        c.bet_graded = True
                    else:
                        c.win = False
                        c.bet_graded = True
        db.session.add(c)
        db.session.commit()
    else:
        return None

def grade_sb():
    """ this function updates all NFLSideBet table with correct win booleans
    Also marks bet graded.  grade_query is a cache of NFLBetGraded table. 
    """ 
    cb1 = NFLSideBet.query.filter_by(bet_taken=True, bet_graded=False).all()
    cb = list(cb1)
    grd = grade_query()
    if cb:
        for g in grd:
            for c in cb:
                if g.game_key == c.game_key:
                    if g.cover_side == "Push":
                        c.win = None
                        c.bet_graded = True
                    elif g.cover_side == c.team:
                        c.win = True
                        c.bet_graded = True
                    else:
                        c.win = False 
                        c.bet_graded = True
        db.session.add(c)
        db.session.commit()
    else:
        return None

def grade_ml():
    """ this function updates all NFLMLBet table with correct win booleans
    Also marks bet graded.  grade_query is a cache of NFLBetGraded table.
    """ 
    cb1 = NFLMLBet.query.filter_by(bet_taken=True, bet_graded=False).all()
    cb = list(cb1)
    grd = grade_query()
    if cb:
        for g in grd:
            for c in cb:
                if g.game_key == c.game_key:
                    if g.cover_ml == "Push":
                        c.win = None
                        c.bet_graded = True 
                    elif g.cover_ml == c.team:
                        c.win = True
                        c.bet_graded = True
                    else:
                        c.win = False 
                        c.bet_graded = True
        db.session.add(c)
        db.session.commit()
    else:
        return None

def grade_all_bets():
    grade_sb()
    grade_ml()
    grade_tb()

#############################################################
### this group of functions pays winners from losers.  Also
# pays admin 10% of risk of loser.  Push no one gets paid.  
############################################################
@cache.cached(timeout=30, key_prefix="all_users")
def get_all_users():
    return Users.query.all()

def pay_winners_from_losers_sb():
    users = get_all_users() # list of all users id
    for u in users:
        sb1 = NFLSideBet.query.filter_by(user_id=u.id, bet_taken=True, bet_graded=True, paid=False).all()
        sb = list(sb1)
        if sb:
            for ss in sb:
                c_profile = Profile.query.filter_by(user_id=ss.user_id).one()
                t_profile = Profile.query.filter_by(user_id=ss.taken_by).one()
                admin = Profile.query.filter_by(user_id=1).one()
                if ss.win == True:
                    print "player %s gets paid from player %s this amount %s" % (ss.user_id, ss.taken_by, ss.amount_win)
                    print "sb w", ss.admin_win 
                    admin.d_amount += ss.admin_win
                    c_profile.d_amount += ss.amount_win
                    t_profile.d_amount -= ss.amount 
                    ss.paid = True 
                if ss.win == False:
                    print "player %s gets paid from player %s this amount %s" % (ss.taken_by, ss.user_id, ss.amount_win)
                    print "sb l", ss.admin_win
                    admin.d_amount += ss.admin_win
                    t_profile.d_amount += ss.amount_win
                    c_profile.d_amount -= ss.amount 
                    ss.paid = True 
                if ss.win == None:
                    print "this is a push no payment"
                    ss.paid = True 
                db.session.add(admin)
                db.session.add(c_profile)
                db.session.add(t_profile)
            db.session.add(ss)
            db.session.commit()


def pay_winners_from_losers_ou():
    users = get_all_users()
    for u in users:
        ou1 = NFLOverUnderBet.query.filter_by(user_id=u.id, bet_taken=True, bet_graded=True, paid=False).all()
        ou = list(ou1)
        if ou:
            for oo in ou:
                c_profile = Profile.query.filter_by(user_id=oo.user_id).one()
                t_profile = Profile.query.filter_by(user_id=oo.taken_by).one()
                admin = Profile.query.filter_by(user_id=1).one()
                if oo.win == True:
                    print "player %s gets paid from player %s this amount %s" % (oo.user_id, oo.taken_by, oo.amount_win)
                    admin.d_amount = oo.admin_win
                    print "ou w", oo.admin_win
                    c_profile.d_amount += oo.amount_win
                    t_profile.d_amount -= oo.amount 
                    oo.paid = True 
                if oo.win == False:
                    print "player %s gets paid from player %s this amount %s" % (oo.taken_by, oo.user_id, oo.amount_win)
                    print "ou l", oo.admin_win
                    admin.d_amount += oo.admin_win
                    t_profile.d_amount += oo.amount_win
                    c_profile.d_amount -= oo.amount 
                    oo.paid = True
                if oo.win == None:
                    print "this is a push no payment."
                    oo.paid = True  
                db.session.add(admin)
                db.session.add(c_profile)
                db.session.add(t_profile)
            db.session.add(oo)
            db.session.commit()

def pay_winners_from_losers_ml():
    users = get_all_users()
    for u in users:
        ml1 = NFLMLBet.query.filter_by(user_id=u.id, bet_taken=True, bet_graded=True, paid=False).all()
        ml = list(ml1)
        if ml:
            for ll in ml:
                c_profile = Profile.query.filter_by(user_id=ll.user_id).one()
                t_profile = Profile.query.filter_by(user_id=ll.taken_by).one()
                admin = Profile.query.filter_by(user_id=1).one()
                if ll.win == True:
                    print "player %s gets paid from player %s this amount %s" % (ll.user_id, ll.taken_by, ll.amount_win)
                    admin.d_amount += ll.admin_win 
                    print "ml w", ll.admin_win
                    c_profile.d_amount += ll.amount_win
                    t_profile.d_amount -= ll.amount 
                    ll.paid = True 
                if ll.win == False:
                    print "player %s gets paid from player %s this amount %s" % (ll.taken_by, ll.user_id, ll.amount_win)
                    admin.d_amount += ll.admin_win 
                    print "ml l", ll.admin_win
                    t_profile.d_amount += ll.amount_win
                    c_profile.d_amount -= ll.amount 
                    ll.paid = True 
                if ll.win == None:
                    print "this is a push no payment"
                    ll.paid = True
                db.session.add(admin) 
                db.session.add(c_profile)
                db.session.add(t_profile)
            db.session.add(ll)
            db.session.commit()

def pay_everyone():
    pay_winners_from_losers_ou()
    pay_winners_from_losers_sb()
    pay_winners_from_losers_ml()

################################################################################
## this group of functions updates all profiles based on graded wins and loses
# and puts wins and loses in profile.win profile.lose and profile.push  
################################################################################
def count_wins_losses_user_id(id, ct):
    """
    counts total wins or losses for user_id. ct=True is for wins. ct=False is for losses.  ct=True,win==win, ct=False,win==loss
    """
    ml = NFLMLBet.query.filter_by(user_id=id, win=ct, bet_taken=True, bet_graded=True, paid=True).count()
    tb = NFLOverUnderBet.query.filter_by(user_id=id, win=ct, bet_taken=True, bet_graded=True, paid=True).count()
    sb = NFLSideBet.query.filter_by(user_id=id,win=ct, bet_taken=True, bet_graded=True, paid=True).count()
    return (ml+tb+sb)

def count_wins_losses_taken_by(id, ct):
    """
    counts total wins or losses for taken_by id. ct=False is for wins. ct=True is for losses.  ct=False,win==win, ct=True,win==loss
    """
    ml = NFLMLBet.query.filter_by(taken_by=id, win=ct, bet_taken=True, bet_graded=True, paid=True).count()
    tb = NFLOverUnderBet.query.filter_by(taken_by=id, win=ct, bet_taken=True, bet_graded=True, paid=True).count()
    sb = NFLSideBet.query.filter_by(taken_by=id, win=ct, bet_taken=True, bet_graded=True, paid=True).count()
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

def update_profile_p(uid):
    """ updates all users Profile by pushes by uid """
    profile = Profile.query.filter_by(user_id=uid).one()
    profile.pushes = count_wins_losses_user_id(uid,None) + count_wins_losses_taken_by(uid, None)
    db.session.add(profile)
    db.session.commit() 

def update_users_wins_losses():
    users = get_all_users()
    for u in users:
        update_profile_w(u.id)
        update_profile_l(u.id)  
        update_profile_p(u.id)

##############################################################################################################
### the kitchen sink function -- combination of all other functions ran then cached  at the end.  
def kitchen_sink():
    grade_all_bets()
    pay_everyone()
    update_users_wins_losses()
##############################################################################################################
def count_pending_bets():
    """ counts the current pending bets for each user """
    user = Users.query.filter_by(id=current_user.id).one()
    ou = NFLOverUnderBet.query.filter((NFLOverUnderBet.user_id==user.id) | (NFLOverUnderBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).count()
    sb = NFLSideBet.query.filter((NFLSideBet.user_id==user.id) | (NFLSideBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).count()
    ml = NFLMLBet.query.filter((NFLMLBet.user_id==user.id) | (NFLMLBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).count()
    return (ou+sb+ml)

def count_graded_bets():
    """ counts all of the graded bets for each user since the beginning of time """
    user = Users.query.filter_by(id=current_user.id).one()
    graded_sb = NFLSideBet.query.filter((NFLSideBet.user_id==user.id) | (NFLSideBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=True, paid=True).count()
    graded_ou = NFLOverUnderBet.query.filter((NFLOverUnderBet.user_id==user.id) | (NFLOverUnderBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=True, paid=True).count()
    graded_ml = NFLMLBet.query.filter((NFLMLBet.user_id==user.id) | (NFLMLBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=True, paid=True).count()
    return (graded_sb+graded_ou+graded_ml)