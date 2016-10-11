from dateutil.parser import parse as parse_date
from app.users.models import Users, Role, UserRoles, Profile, Admin
from app.nfl.models import NFLBetGraded, NFLOverUnderBet, NFLSideBet,NFLMLBet
from app.nfl_stats.models import NFLScore
from app import app, db, user_datastore 
from flask_security.utils import encrypt_password

def create_users():
    with app.app_context():
        role1 = Role(id=1,name="admin", description="Admin of site")
        role2 = Role(id=2,name="player", description="basic user of site")
        role3 = Role(id=3,name="bookie", description="More privileges then basic user")
        db.session.add_all([role1,role2,role3])
        db.session.commit() 
        user1 = user_datastore.create_user(id=1,username="admin", email="jreiher2003@yahoo.com", password=encrypt_password("password"))
        user2 = user_datastore.create_user(id=2,username="j3ff_", email="jeffreiher@gmail.com", password=encrypt_password("password"))
        user3 = user_datastore.create_user(id=3, username="Nhilson", email="ken@gmail.com", password=encrypt_password("password"))
        user4 = user_datastore.create_user(id=4, username="Mike", email="mike@gmail.com", password=encrypt_password("password"))
        user5 = user_datastore.create_user(id=5, username="Greg", email="greg@gmail.com", password=encrypt_password("password"))
        user6 = user_datastore.create_user(id=6, username="Rob", email="rob@gmail.com", password=encrypt_password("password"))
        db.session.commit()

        u1 = UserRoles(user_id=user1.id, role_id=role1.id)
        u11 = UserRoles(user_id=user1.id, role_id=role2.id)
        u12 = UserRoles(user_id=user1.id, role_id=role3.id)
        admin = Admin(id=1, avatar="https://scontent-mia1-1.xx.fbcdn.net/v/t1.0-1/p40x40/12208487_10153305128458380_4762134821855593042_n.jpg?oh=46fb02bcf716c4fafa4c0e8d6a5b4ac7&oe=587158D8", user_id=1)
        profile1 = Profile(id=1,avatar="https://avatars1.githubusercontent.com/u/5870557?v=3&s=466",user_id=1, d_amount=100)
        # user 2
        u2 = UserRoles(user_id=user2.id, role_id=role2.id)
        u3 = UserRoles(user_id=user2.id, role_id=role3.id)
        profile2 = Profile(id=2,avatar="https://avatars1.githubusercontent.com/u/5870557?v=3&s=466",user_id=2, d_amount=100)
        #user 3
        u4 = UserRoles(user_id=user3.id, role_id=role2.id)
        u5 = UserRoles(user_id=user3.id, role_id=role3.id)
        profile3 = Profile(id=3,avatar="https://scontent-mia1-1.xx.fbcdn.net/v/t1.0-1/p32x32/1510596_10154079196053217_4801038040181059076_n.jpg?oh=d94fc7e8d5fc148a2a814088cf368e2e&oe=5860EFC1",user_id=3, d_amount=100)
        # user 4
        u6 = UserRoles(user_id=user4.id, role_id=role2.id)
        u7 = UserRoles(user_id=user4.id, role_id=role3.id)
        profile4 = Profile(id=4,avatar="https://scontent-mia1-1.xx.fbcdn.net/v/t1.0-1/p32x32/14079700_10154336208935390_728646401192678292_n.jpg?oh=0077ed288133a959614232bd6ac3a46b&oe=58773E81",user_id=4, d_amount=100)
        # user 5
        u8 = UserRoles(user_id=user5.id, role_id=role2.id)
        u9 = UserRoles(user_id=user5.id, role_id=role3.id)
        profile5 = Profile(id=5,avatar="https://scontent-mia1-1.xx.fbcdn.net/v/t1.0-1/c0.5.32.32/p32x32/14291626_1175568729171260_960106491493786709_n.jpg?oh=f1c5d44a89ea8ea0e5e73a490ce3ac6e&oe=586FBED1",user_id=5, d_amount=100)
        # user 6
        u10 = UserRoles(user_id=user6.id, role_id=role2.id)
        u11 = UserRoles(user_id=user6.id, role_id=role3.id)
        profile6 = Profile(id=6,avatar="https://scontent-mia1-1.xx.fbcdn.net/v/t1.0-1/p32x32/13342960_10209784965251295_4841832740377934677_n.jpg?oh=71ef1aaf572dce4ac995ff0b0b4ff3e5&oe=58785BBE",user_id=6, d_amount=100)
        db.session.add_all([u1,admin,u11,u12,profile1,u2,u3,profile2,u4,u5,profile3,u6,u7,profile4,u8,u9,profile5,u10,u11,profile6])
        db.session.commit()

def create_bet():
    profile1 = Profile.query.filter_by(user_id=1).one()
    profile2 = Profile.query.filter_by(user_id=2).one()
    profile3 = Profile.query.filter_by(user_id=3).one()
    profile4 = Profile.query.filter_by(user_id=4).one()
    profile5 = Profile.query.filter_by(user_id=5).one()
    profile6 = Profile.query.filter_by(user_id=6).one()
    bet1 = NFLOverUnderBet(id=1, bet_key=1, game_key=201610420, game_date=parse_date("10/3/2016 8:30:00 PM"), away_team="NYG", home_team="MIN", over_under="u", vs="NYG vs @MIN", total=42.5, amount=20, user_id=2, bet_taken=True, taken_by=3, taken_username="Nhilson")
    # admin.bets_created += 1
    # admin.bets_taken += 1
    profile2.bets_created += 1
    profile2.bets_taken += 1
    profile3.bets_taken += 1
    bet2 = NFLSideBet(id=2, bet_key=2, game_key=201610420, game_date=parse_date("10/3/2016 8:30:00 PM"), away_team="NYG", home_team="MIN", vs="NYG vs @MIN", ps=3.5, team="NYG", amount=10, user_id=3, bet_taken=True, taken_by=4, taken_username="Mike")
    # admin.bets_created += 1
    # admin.bets_taken += 1
    profile3.bets_created += 1
    profile3.bets_taken += 1
    profile4.bets_taken += 1
    bet3 = NFLMLBet(id=3,bet_key=3, game_key=201610420, game_date=parse_date("10/3/2016 8:30:00 PM"), away_team="NYG", home_team="MIN", vs="NYG vs @MIN", ml=-125, team="MIN", amount=10, user_id=2, bet_taken=True, taken_by=3, taken_username="Nhilson")
    # admin.bets_created += 1
    # admin.bets_taken += 1
    profile2.bets_created += 1
    profile2.bets_taken += 1
    profile3.bets_taken += 1
    bet4 = NFLSideBet(id=4, bet_key=4, game_key=201610420, game_date=parse_date("10/3/2016 8:30:00 PM"), away_team="NYG", home_team="MIN", vs="NYG vs @MIN", ps=3.5, team="NYG", amount=10, user_id=6, bet_taken=True, taken_by=2,taken_username="j3ff_")
    # admin.bets_created += 1
    # admin.bets_taken += 1
    profile6.bets_created += 1
    profile6.bets_taken += 1
    profile2.bets_taken += 1
    bet5 = NFLSideBet(id=5, bet_key=5, game_key=201610420, game_date=parse_date("10/3/2016 8:30:00 PM"), away_team="NYG", home_team="MIN", vs="NYG vs @MIN", ps=3.5, team="MIN", amount=10, user_id=4, bet_taken=True, taken_by=5, taken_username="Greg")
    # admin.bets_created += 1
    # admin.bets_taken += 1
    profile4.bets_created += 1
    profile4.bets_taken += 1
    profile5.bets_taken += 1
    bet6 = NFLSideBet(id=6, bet_key=6, game_key=201610512, game_date=parse_date("10/9/2016 8:30:00 PM"), away_team="NYG", home_team="GB", vs="NYG vs @GB", ps=-7, team="GB", amount=10, user_id=2, bet_taken=True, taken_by=3, taken_username="Nhilson")
    # admin.bets_created += 1
    # admin.bets_taken += 1
    profile2.bets_created += 1
    profile2.bets_taken += 1
    profile3.bets_taken += 1
    db.session.add_all([bet1,bet2,bet3,bet4,bet5,bet6,profile2,profile3,profile4,profile5,profile6])
    db.session.commit()

if __name__ == "__main__":
    db.drop_all()
    print "Just Dropped all tables"
    db.create_all()
    create_users()
    print "users created"
    create_bet()
    print "bets created"
    
    