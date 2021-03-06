from app import app, db, cache, block_io
from decimal import Decimal
from flask_security import current_user
from app.nfl_stats.models import NFLTeam 
from app.nfl.models import NFLBetGraded, NFLSideBet, NFLOverUnderBet, NFLMLBet
from app.nfl.utils import make_salt 
from app.users.models import Users, Profile, BitcoinWallet
import time

def all_nfl_teams(update=False):
    key = "teams"
    all_teams = cache.get(key)
    if all_teams is None or update:
        all_teams = NFLTeam.query.all()
        all_teams = list(all_teams)
        cache.set(key, all_teams)
    return all_teams

def get_user_wallet():
    if current_user.get_id():
        wallet = BitcoinWallet.query.filter_by(user_id=current_user.id).one_or_none()
        try:
            wallet = block_io.get_address_by_label(label=wallet.label)
        except AttributeError:
            print "no wallet created yet"
        return wallet or None 
    else:
        return None

#########################################################################################################
def ou():
    return NFLOverUnderBet.query.filter((NFLOverUnderBet.user_id==current_user.id) | (NFLOverUnderBet.taken_by==current_user.id)).filter_by(bet_taken=True, bet_graded=False).all()
def sb():    
    return NFLSideBet.query.filter((NFLSideBet.user_id==current_user.id) | (NFLSideBet.taken_by==current_user.id)).filter_by(bet_taken=True, bet_graded=False).all()

def ml():
    return NFLMLBet.query.filter((NFLMLBet.user_id==current_user.id) | (NFLMLBet.taken_by==current_user.id)).filter_by(bet_taken=True, bet_graded=False).all()

def graded_sb():
    return NFLSideBet.query.filter((NFLSideBet.user_id==current_user.id) | (NFLSideBet.taken_by==current_user.id)).filter_by(bet_taken=True, bet_graded=True, paid=True).all()

def graded_ou():
    return NFLOverUnderBet.query.filter((NFLOverUnderBet.user_id==current_user.id) | (NFLOverUnderBet.taken_by==current_user.id)).filter_by(bet_taken=True, bet_graded=True, paid=True).all()

def graded_ml():
    return NFLMLBet.query.filter((NFLMLBet.user_id==current_user.id) | (NFLMLBet.taken_by==current_user.id)).filter_by(bet_taken=True, bet_graded=True, paid=True).all()
#################################################################################
## this group of functions updates all the bet tables with wins loses or pushes
## win is True, lose is False, push is None
# @cache.cached(timeout=5, key_prefix="grading_query")
def grade_query():
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
                    if c.over_under == 'u':
                        if g.total_score < c.total:
                            c.win = True
                            c.bet_graded = True
                        elif g.total_score > c.total:
                            c.win = False
                            c.bet_graded = True
                        elif g.total_score == c.total:
                            c.win = None 
                            c.bet_graded = True 
                    elif c.over_under == 'o':
                        if g.total_score > c.total:
                            c.win = True 
                            c.bet_graded = True
                        elif g.total_score < c.total:
                            c.win = False
                            c.bet_graded = True
                        elif g.total_score == c.total:
                            c.win == None
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
                    if c.home_team == c.team:
                        if g.away_score < (g.home_score + c.ps):
                            c.win = True
                            c.bet_graded = True 
                        elif g.away_score > (g.home_score + c.ps):
                            c.win = False
                            c.bet_graded = True 
                        elif g.away_score == (g.home_score + c.ps):
                            c.win = None 
                            c.bet_graded = True
                    if c.away_team == c.team:
                        if g.home_score < (g.away_score + c.ps):
                            c.win = True
                            c.bet_graded = True
                        elif g.home_score > (g.away_score + c.ps):
                            c.win = False 
                            c.bet_graded = True 
                        elif g.home_score == (g.away_score + c.ps):
                            c.win = None 
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
                    if c.home_team == c.team:
                        if g.home_score > g.away_score:
                            c.win = True
                            c.bet_graded = True
                        elif g.home_score < g.away_score:
                            c.win = False 
                            c.bet_graded = True 
                        elif g.home_score == g.away_score:
                            c.win = None
                            c.bet_graded = True 
                    if c.away_team == c.team:
                        if g.away_score > g.home_score:
                            c.win = True
                            c.bet_graded = True
                        elif g.away_score < g.home_score:
                            c.win = False
                            c.bet_graded = True 
                        elif g.away_score == g.home_score:
                            c.win = None 
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
# @cache.cached(timeout=30, key_prefix="all_users")
def get_all_users():
    return Users.query.all()

def get_admin():
    user1 = Users.query.filter_by(id=1).one()
    return user1.admin

def pay_winners_from_losers_sb():
    # nonce = make_salt(length=32)
    # nonce1 = make_salt(length=32)
    # Admin = Users.query.filter_by(id=1).one()
    admin = "2MzrAiZFY24U1Zqtcf9ZqD1WskKprzYbqi7"
    users = get_all_users() # list of all users id
    for u in users:
        sb1 = NFLSideBet.query.filter_by(user_id=u.id, bet_taken=True, bet_graded=True, paid=False).all()
        sb = list(sb1)
        if sb:
            for ss in sb:
                c_user = Users.query.filter_by(id=ss.user_id).one()
                t_user = Users.query.filter_by(id=ss.taken_by).one()
                if ss.win == True:
                    print "player %s gets paid from player %s this amount %s" % (ss.user_id, ss.taken_by, ss.amount_win)
                    network_fees = block_io.get_network_fee_estimate(amounts = (float(ss.amount) + float(ss.amount_win)), from_addresses = admin, to_addresses = c_user.bitcoin_wallet.address, priority="low")
                    network_fees = float(network_fees["data"]["estimated_network_fee"])
                    block_io.withdraw_from_addresses(amounts = ((float(ss.amount) + float(ss.amount_win)) - network_fees), from_addresses = admin, to_addresses = c_user.bitcoin_wallet.address, priority="low", nonce=make_salt(length=32))
                    c_user.profile.pending -=  Decimal(ss.amount)
                    t_user.profile.pending -=  Decimal(ss.amount)
                    ss.network_fees += Decimal(network_fees)
                    ss.paid = True 
                if ss.win == False:
                    print "player %s gets paid from player %s this amount %s" % (ss.taken_by, ss.user_id, ss.amount_win)
                    network_fees = block_io.get_network_fee_estimate(amounts = (float(ss.amount) + float(ss.amount_win)), from_addresses = admin, to_addresses = t_user.bitcoin_wallet.address, priority="low")
                    network_fees = float(network_fees["data"]["estimated_network_fee"])
                    block_io.withdraw_from_addresses(amounts = ((float(ss.amount) + float(ss.amount_win)) - network_fees), from_addresses = admin, to_addresses = t_user.bitcoin_wallet.address, priority="low", nonce=make_salt(length=32))
                    t_user.profile.pending -=  Decimal(ss.amount)
                    c_user.profile.pending -=  Decimal(ss.amount)
                    ss.taken_network_fees += Decimal(network_fees)
                    ss.paid = True 
                if ss.win == None:
                    print "this is a push no payment both users get back their money"
                    network_fees = block_io.get_network_fee_estimate(amounts = (float(ss.amount)), from_addresses = admin, to_addresses = c_user.bitcoin_wallet.address, priority="low")
                    network_fees = float(network_fees["data"]["estimated_network_fee"])
                    taken_network_fees = block_io.get_network_fee_estimate(amounts = (float(ss.amount)), from_addresses = admin, to_addresses = t_user.bitcoin_wallet.address, priority="low")
                    taken_network_fees = float(taken_network_fees["data"]["estimated_network_fee"])
                    block_io.withdraw_from_addresses(amounts = (float(ss.amount) - network_fees), from_addresses = admin, to_addresses = c_user.bitcoin_wallet.address, priority="low", nonce=make_salt(length=32))
                    block_io.withdraw_from_addresses(amounts = (float(ss.amount) - taken_network_fees), from_addresses = admin, to_addresses = t_user.bitcoin_wallet.address, priority="low", nonce=make_salt(length=32))
                    c_user.profile.pending -=  Decimal(ss.amount)
                    t_user.profile.pending -=  Decimal(ss.amount)
                    ss.network_fees += Decimal(network_fees)
                    ss.taken_network_fees += Decimal(taken_network_fees)
                    ss.paid = True 
                db.session.add(c_user)
                db.session.add(t_user)
            db.session.add(ss)
            db.session.commit()


def pay_winners_from_losers_ou():
    # nonce = make_salt(length=32)
    # nonce1 = make_salt(length=32)
    Admin = Users.query.filter_by(id=1).one()
    admin = "2MzrAiZFY24U1Zqtcf9ZqD1WskKprzYbqi7"
    users = get_all_users()
    for u in users:
        ou1 = NFLOverUnderBet.query.filter_by(user_id=u.id, bet_taken=True, bet_graded=True, paid=False).all()
        ou = list(ou1)
        if ou:
            for oo in ou:
                c_user = Users.query.filter_by(id=oo.user_id).one()
                t_user = Users.query.filter_by(id=oo.taken_by).one()
                if oo.win == True:
                    print "player %s gets paid from player %s this amount %s" % (oo.user_id, oo.taken_by, oo.amount_win)
                    network_fees = block_io.get_network_fee_estimate(amounts = (float(oo.amount) + float(oo.amount_win)), from_addresses = admin, to_addresses = c_user.bitcoin_wallet.address, priority="low")
                    network_fees = float(network_fees["data"]["estimated_network_fee"])
                    block_io.withdraw_from_addresses(amounts = ((float(oo.amount) + float(oo.amount_win)) - network_fees), from_addresses = admin, to_addresses = c_user.bitcoin_wallet.address, priority="low", nonce=make_salt(length=32))
                   
                    c_user.profile.pending -=  Decimal(oo.amount)
                    t_user.profile.pending -=  Decimal(oo.amount)
                    oo.network_fees += Decimal(network_fees)
                    oo.paid = True 
                if oo.win == False:
                    print "player %s gets paid from player %s this amount %s" % (oo.taken_by, oo.user_id, oo.amount_win)
                    network_fees = block_io.get_network_fee_estimate(amounts = (float(oo.amount) + float(oo.amount_win)), from_addresses = admin, to_addresses = t_user.bitcoin_wallet.address, priority="low")
                    network_fees = float(network_fees["data"]["estimated_network_fee"])
                    block_io.withdraw_from_addresses(amounts = ((float(oo.amount) + float(oo.amount_win)) - network_fees), from_addresses = admin, to_addresses = t_user.bitcoin_wallet.address, priority="low", nonce=make_salt(length=32))
                    
                    t_user.profile.pending -=  Decimal(oo.amount)
                    c_user.profile.pending -=  Decimal(oo.amount)
                    oo.taken_network_fees += Decimal(network_fees)
                    oo.paid = True
                if oo.win == None:
                    print "this is a push no payment. People get back their money."
                    taken_network_fees = block_io.get_network_fee_estimate(amounts = (float(oo.amount)), from_addresses = admin, to_addresses = t_user.bitcoin_wallet.address, priority="low")
                    taken_network_fees = float(taken_network_fees["data"]["estimated_network_fee"])
                    network_fees = block_io.get_network_fee_estimate(amounts = (float(oo.amount)), from_addresses = admin, to_addresses = c_user.bitcoin_wallet.address, priority="low")
                    network_fees = float(network_fees["data"]["estimated_network_fee"])
                    block_io.withdraw_from_addresses(amounts = (float(oo.amount) - network_fees), from_addresses = admin, to_addresses = c_user.bitcoin_wallet.address, priority="low", nonce=nonce)
                    block_io.withdraw_from_addresses(amounts = (float(oo.amount) - taken_network_fees), from_addresses = admin, to_addresses = t_user.bitcoin_wallet.address, priority="low", nonce=nonce)
                    t_user.profile.pending -=  Decimal(oo.amount)
                    c_user.profile.pending -=  Decimal(oo.amount)
                    oo.taken_network_fees += Decimal(taken_network_fees)
                    oo.network_fees += Decimal(network_fees)
                    oo.paid = True  
                db.session.add(c_user)
                db.session.add(t_user)
            db.session.add(oo)
            db.session.commit()

def pay_winners_from_losers_ml():
    # nonce = make_salt(length=32)
    # nonce1 = make_salt(length=32)
    Admin = Users.query.filter_by(id=1).one()
    admin = "2MzrAiZFY24U1Zqtcf9ZqD1WskKprzYbqi7"
    users = get_all_users()
    for u in users:
        ml1 = NFLMLBet.query.filter_by(user_id=u.id, bet_taken=True, bet_graded=True, paid=False).all()
        ml = list(ml1)
        if ml:
            for ll in ml:
                c_user = Users.query.filter_by(id=ll.user_id).one()
                t_user = Users.query.filter_by(id=ll.taken_by).one()
                if ll.win == True:
                    print "player %s gets paid from player %s this amount %s" % (ll.user_id, ll.taken_by, ll.amount_win)
                    network_fees = block_io.get_network_fee_estimate(amounts = (float(ll.amount) + float(ll.amount_win)), from_addresses = admin, to_addresses = c_user.bitcoin_wallet.address, priority="low")
                    network_fees = float(network_fees["data"]["estimated_network_fee"])
                    block_io.withdraw_from_addresses(amounts = ((float(ll.amount) + float(ll.amount_win)) - network_fees), from_addresses = admin, to_addresses = c_user.bitcoin_wallet.address, priority="low", nonce=make_salt(length=32))
                    
                    c_user.profile.pending -=  Decimal(ll.amount)
                    t_user.profile.pending -=  Decimal(ll.amount)
                    ll.network_fees += Decimal(network_fees)
                    ll.paid = True 
                if ll.win == False:
                    print "player %s gets paid from player %s this amount %s" % (ll.taken_by, ll.user_id, ll.amount_win)
                    network_fees = block_io.get_network_fee_estimate(amounts = (float(ll.amount) + float(ll.amount_win)), from_addresses = admin, to_addresses = t_user.bitcoin_wallet.address, priority="low")
                    network_fees = float(network_fees["data"]["estimated_network_fee"])
                    block_io.withdraw_from_addresses(amounts = ((float(ll.amount) + float(ll.amount_win)) - network_fees), from_addresses = admin, to_addresses = t_user.bitcoin_wallet.address, priority="low", nonce=make_salt(length=32))
                    
                    t_user.profile.pending -=  Decimal(ll.amount)
                    c_user.profile.pending -=  Decimal(ll.amount)
                    ll.taken_network_fees += Decimal(network_fees)
                    ll.paid = True 
                if ll.win == None:
                    print "this is a push no payment. Everyone gets back their money"
                    network_fees = block_io.get_network_fee_estimate(amounts = (float(ll.amount)), from_addresses = admin, to_addresses = c_user.bitcoin_wallet.address, priority="low")
                    network_fees = float(network_fees["data"]["estimated_network_fee"])
                    taken_network_fees = block_io.get_network_fee_estimate(amounts = (float(ll.amount)), from_addresses = admin, to_addresses = t_user.bitcoin_wallet.address, priority="low")
                    taken_network_fees = float(taken_network_fees["data"]["estimated_network_fee"])
                    block_io.withdraw_from_addresses(amounts = (float(ll.amount) - network_fees), from_addresses = admin, to_addresses = c_user.bitcoin_wallet.address, priority="low", nonce=make_salt(length=32))
                    block_io.withdraw_from_addresses(amounts = (float(ll.amount) - taken_network_fees), from_addresses = admin, to_addresses = t_user.bitcoin_wallet.address, priority="low", nonce=make_salt(length=32))
                    c_user.profile.pending -=  Decimal(ll.amount)
                    t_user.profile.pending -=  Decimal(ll.amount)
                    ll.network_fees += Decimal(network_fees)
                    ll.taken_network_fees += Decimal(taken_network_fees)
                    ll.paid = True
                db.session.add(c_user)
                db.session.add(t_user)
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

def reset_pending_bets():
    """ checks if anybets are pending if nothing is pending resets pending to 0 """
    user = Users.query.filter_by(id=current_user.id).one()
    ou = NFLOverUnderBet.query.filter((NFLOverUnderBet.user_id==user.id) | (NFLOverUnderBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).all()
    sb = NFLSideBet.query.filter((NFLSideBet.user_id==user.id) | (NFLSideBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).all()
    ml = NFLMLBet.query.filter((NFLMLBet.user_id==user.id) | (NFLMLBet.taken_by==user.id)).filter_by(bet_taken=True, bet_graded=False).all()
    ou = list(ou)
    sb = list(sb)
    ml = list(ml)
    if not ou and not sb and not ml:
        print "all lists are empty. if no pending bets exsist then reset pending to 0"
    else:
        print "a list had something in it. and don't do anything at all"

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
