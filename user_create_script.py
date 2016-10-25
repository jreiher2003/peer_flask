from dateutil.parser import parse as parse_date
from app.users.models import Users, Role, UserRoles, Profile, Admin, BitcoinWallet
from app.nfl.models import NFLBetGraded, NFLOverUnderBet, NFLSideBet,NFLMLBet
from app.nfl_stats.models import NFLScore
from app import app, db, block_io, bcrypt 
# from flask_security.utils import encrypt_password

def create_users():
    with app.app_context():
        role1 = Role(id=1,name="admin", description="Admin of site")
        role2 = Role(id=2,name="player", description="basic user of site")
        role3 = Role(id=3,name="bookie", description="More privileges then basic user")
        db.session.add_all([role1,role2,role3])
        db.session.commit() 
        user1 = Users(id=1,username="admin", email="jreiher2003@yahoo.com", password="password123456")
        user2 = Users(id=2,username="j3ff_", email="jeffreiher@gmail.com", password="password123456")
        user3 = Users(id=3, username="Nhilson", email="ken@gmail.com", password="password123456")
        user4 = Users(id=4, username="Mike", email="mike@gmail.com", password="password123456")
        user5 = Users(id=5, username="Greg", email="greg@gmail.com", password="password123456")
        user6 = Users(id=6, username="Rob", email="rob@gmail.com", password="password123456")
        db.session.add_all([user1,user2,user3,user4,user5,user6])
        db.session.commit()


        u1 = UserRoles(user_id=user1.id, role_id=role1.id)
        u11 = UserRoles(user_id=user1.id, role_id=role2.id)
        u12 = UserRoles(user_id=user1.id, role_id=role3.id)
        admin = Admin(id=1, user_id=1)
        profile1 = Profile(id=1,avatar=None,user_id=1)
        # user 2
        u2 = UserRoles(user_id=user2.id, role_id=role2.id)
        u3 = UserRoles(user_id=user2.id, role_id=role3.id)
        profile2 = Profile(id=2,user_id=2)
        #user 3
        u4 = UserRoles(user_id=user3.id, role_id=role2.id)
        u5 = UserRoles(user_id=user3.id, role_id=role3.id)
        profile3 = Profile(id=3,user_id=3)
        # user 4
        u6 = UserRoles(user_id=user4.id, role_id=role2.id)
        u7 = UserRoles(user_id=user4.id, role_id=role3.id)
        profile4 = Profile(id=4,user_id=4)
        # user 5
        u8 = UserRoles(user_id=user5.id, role_id=role2.id)
        u9 = UserRoles(user_id=user5.id, role_id=role3.id)
        profile5 = Profile(id=5,user_id=5)
        # user 6
        u10 = UserRoles(user_id=user6.id, role_id=role2.id)
        u11 = UserRoles(user_id=user6.id, role_id=role3.id)
        profile6 = Profile(id=6,user_id=6)
        db.session.add_all([u1,admin,u11,u12,profile1,u2,u3,profile2,u4,u5,profile3,u6,u7,profile4,u8,u9,profile5,u10,u11,profile6])
        db.session.commit()

def create_wallets():
    user1 = BitcoinWallet(label = "default", address= "2MzrAiZFY24U1Zqtcf9ZqD1WskKprzYbqi7", user_id=1)
    user2 = BitcoinWallet(label = "bacru22", address = "2N7xdmuX55uRFLQTwmcU6FR1SH3mQXSTog5", user_id=2)
    user3 = BitcoinWallet(label = "juby67", address = "2NEysAXjp2ozYwcNoqAN6EJCXrTiQYvHVze", user_id=3)
    user4 = BitcoinWallet(label = "fonty81", address = "2NDTcuhDuZPgV5b9FN8svdrEJtVeKCRPQDH", user_id=4)
    user5 = BitcoinWallet(label = "zevu17", address = "2NGFk7ZLf3bUPqg4ZLybbJJWD9APCZdaGh2", user_id=5)
    db.session.add_all([user1,user2,user3,user4,user5])
    db.session.commit()

def update_profiles_bitcoin():
    user1 = Users.query.filter_by(id=1).one()
    user2 = Users.query.filter_by(id=2).one()
    user3 = Users.query.filter_by(id=3).one()
    user4 = Users.query.filter_by(id=4).one()
    user5 = Users.query.filter_by(id=5).one()
    user1.admin.site_money = user1.bitcoin_wallet.available_btc 
    
    db.session.add_all([user1,user2,user3,user4,user5])
    db.session.commit()

def create_bet():
    user1 = Users.query.filter_by(id=1).one()
    user2 = Users.query.filter_by(id=2).one()
    user3 = Users.query.filter_by(id=3).one()
    user4 = Users.query.filter_by(id=4).one()
    user5 = Users.query.filter_by(id=5).one()
    user6 = Users.query.filter_by(id=6).one()
    network = block_io.get_network_fee_estimate(amounts = 0.004, from_addresses = "2N7xdmuX55uRFLQTwmcU6FR1SH3mQXSTog5", to_addresses = "2NEysAXjp2ozYwcNoqAN6EJCXrTiQYvHVze", priority="low")
    network_fees = float(network["data"]["estimated_network_fee"])

    bet1 = NFLOverUnderBet(id=1, bet_key=1, game_key=201610420, game_date=parse_date("10/3/2016 8:30:00 PM"), away_team="NYG", home_team="MIN", over_under="u", vs="NYG vs @MIN", total=42.5, amount=0.004, user_id=2, bet_taken=True, taken_by=3, taken_username="Nhilson")
    user2.profile.bets_created += 1
    user2.profile.bets_taken += 1
    user2.profile.pending -= (bet1.amount + network_fees)
    user3.profile.bets_taken += 1
    user3.profile.pending -= (bet1.amount + network_fees)

    bet2 = NFLSideBet(id=2, bet_key=2, game_key=201610420, game_date=parse_date("10/3/2016 8:30:00 PM"), away_team="NYG", home_team="MIN", vs="NYG vs @MIN", ps=3.5, team="NYG", amount=0.004, user_id=2, bet_taken=True, taken_by=3, taken_username="Nhilson")
    user2.profile.bets_created += 1
    user2.profile.bets_taken += 1
    user2.profile.pending -= (bet2.amount + network_fees)
    user3.profile.bets_taken += 1
    user3.profile.pending -= (bet2.amount + network_fees)

    # bet3 = NFLMLBet(id=3,bet_key=3, game_key=201610420, game_date=parse_date("10/3/2016 8:30:00 PM"), away_team="NYG", home_team="MIN", vs="NYG vs @MIN", ml=-125, team="MIN", amount=0.0004, user_id=1, bet_taken=True, taken_by=2, taken_username="Nhilson")
   
    # profile2.bets_created += 1
    # profile2.bets_taken += 1
    # profile3.bets_taken += 1
    # bet4 = NFLSideBet(id=4, bet_key=4, game_key=201610420, game_date=parse_date("10/3/2016 8:30:00 PM"), away_team="NYG", home_team="MIN", vs="NYG vs @MIN", ps=3.5, team="NYG", amount=0.0004, user_id=1, bet_taken=True, taken_by=2,taken_username="j3ff_")
    
    # profile6.bets_created += 1
    # profile6.bets_taken += 1
    # profile2.bets_taken += 1
    # bet5 = NFLSideBet(id=5, bet_key=5, game_key=201610420, game_date=parse_date("10/3/2016 8:30:00 PM"), away_team="NYG", home_team="MIN", vs="NYG vs @MIN", ps=3.5, team="MIN", amount=0.0004, user_id=1, bet_taken=True, taken_by=2, taken_username="Greg")
    # profile4.bets_created += 1
    # profile4.bets_taken += 1
    # profile5.bets_taken += 1

    bet6 = NFLSideBet(id=6, bet_key=6, game_key=201610512, game_date=parse_date("10/9/2016 8:30:00 PM"), away_team="NYG", home_team="GB", vs="NYG vs @GB", ps=-7, team="GB", amount=0.004, user_id=2, bet_taken=True, taken_by=3, taken_username="Nhilson")
    user2.profile.bets_created += 1
    user2.profile.bets_taken += 1
    user2.profile.pending -= (bet6.amount + network_fees)
    user3.profile.bets_taken += 1
    user3.profile.pending -= (bet6.amount + network_fees) 

    db.session.add_all([bet1, bet2, bet6, user2, user3])
    db.session.commit()

if __name__ == "__main__":
    db.drop_all()
    print "Just Dropped all tables"
    db.create_all()
    create_users()
    # create_wallets()
    # update_profiles_bitcoin()
    # print "users created"
    # create_bet()
    print "bets created"
    
    