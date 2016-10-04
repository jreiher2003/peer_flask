from dateutil.parser import parse as parse_date
from app.users.models import Users, Role, UserRoles,Profile
from app.nfl.models import NFLcreateBet, NFLtakeBet
from app import app, db, user_datastore 
from flask_security.utils import encrypt_password
# bcrypt.generate_password_hash
def create_users():
    with app.app_context():
        role1 = Role(id=1,name="admin", description="Admin of site")
        role2 = Role(id=2,name="users", description="basic user of site")
        role3 = Role(id=3,name="gold", description="More privileges then basic user")
        db.session.add(role1)
        db.session.add(role2)
        db.session.add(role3)
        db.session.commit() 

        user1 = user_datastore.create_user(id=1,username="j3ff_", email="jeffreiher@gmail.com", password=encrypt_password("password"))
        user2 = user_datastore.create_user(id=2, username="nhilson", email="ken@gmail.com", password=encrypt_password("password"))
        user3 = user_datastore.create_user(id=3, username="Mike", email="mike@gmail.com", password=encrypt_password("password"))
        user4 = user_datastore.create_user(id=4, username="Greg", email="greg@gmail.com", password=encrypt_password("password"))
        user5 = user_datastore.create_user(id=5, username="Rob", email="rob@gmail.com", password=encrypt_password("password"))
        db.session.commit()
        # user 1
        u1 = UserRoles(user_id=user1.id, role_id=role1.id)
        u2 = UserRoles(user_id=user1.id, role_id=role2.id)
        u3 = UserRoles(user_id=user1.id, role_id=role3.id)
        profile1 = Profile(id=1,avatar="https://avatars1.githubusercontent.com/u/5870557?v=3&s=466",user_id=1)
        #user 2
        u4 = UserRoles(user_id=user2.id, role_id=role2.id)
        u5 = UserRoles(user_id=user2.id, role_id=role3.id)
        profile2 = Profile(id=2,avatar="https://scontent-mia1-1.xx.fbcdn.net/v/t1.0-1/p32x32/1510596_10154079196053217_4801038040181059076_n.jpg?oh=d94fc7e8d5fc148a2a814088cf368e2e&oe=5860EFC1",user_id=2)
        # user 3
        u6 = UserRoles(user_id=user3.id, role_id=role2.id)
        u7 = UserRoles(user_id=user3.id, role_id=role3.id)
        profile3 = Profile(id=3,avatar="https://scontent-mia1-1.xx.fbcdn.net/v/t1.0-1/p32x32/14079700_10154336208935390_728646401192678292_n.jpg?oh=0077ed288133a959614232bd6ac3a46b&oe=58773E81",user_id=3)
        # user 4
        u8 = UserRoles(user_id=user4.id, role_id=role2.id)
        u9 = UserRoles(user_id=user4.id, role_id=role3.id)
        profile4 = Profile(id=4,avatar="https://scontent-mia1-1.xx.fbcdn.net/v/t1.0-1/c0.5.32.32/p32x32/14291626_1175568729171260_960106491493786709_n.jpg?oh=f1c5d44a89ea8ea0e5e73a490ce3ac6e&oe=586FBED1",user_id=4)
        # user 5
        u10 = UserRoles(user_id=user5.id, role_id=role2.id)
        u11 = UserRoles(user_id=user5.id, role_id=role3.id)
        profile5 = Profile(id=5,avatar="https://scontent-mia1-1.xx.fbcdn.net/v/t1.0-1/p32x32/13342960_10209784965251295_4841832740377934677_n.jpg?oh=71ef1aaf572dce4ac995ff0b0b4ff3e5&oe=58785BBE",user_id=5)

        # db.session.add(user1)
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(profile1)

        # db.session.add(user2)
        db.session.add(u4)
        db.session.add(u5)
        db.session.add(profile2)

        # db.session.add(user3)
        db.session.add(u6)
        db.session.add(u7)
        db.session.add(profile3)

        # db.session.add(user4)
        db.session.add(u8)
        db.session.add(u9)
        db.session.add(profile4)

        # db.session.add(user5)
        db.session.add(u10)
        db.session.add(u11)
        db.session.add(profile5)
        
        db.session.commit()

def create_bet():
    bet1 = NFLcreateBet(bet_key=1, game_key=201610531, game_date=parse_date("10/6/2016 8:25:00 PM"), away_team="ARI", home_team="SF", over_under="o", vs="ARI vs @SF", total=42.5, amount=20, user_id=1, bet_taken=False)
    bet4 = NFLcreateBet(bet_key=4, game_key=201610508, game_date=parse_date("10/9/2016 1:00:00 PM"), away_team="NE", home_team="CLE", over_under="u", vs="NE vs @CLE", total=46.5, amount=10, user_id=2, bet_taken=False)
    bet2 = NFLcreateBet(bet_key=2, game_key=201610511, game_date=parse_date("10/9/2016 1:00:00 PM"), away_team="PHI", home_team="DET", team="DET", vs="PHI vs @DET",ps=3,amount=40,user_id=3, bet_taken=False)
    bet3 = NFLcreateBet(bet_key=3, game_key=201610514, game_date=parse_date("10/9/2016 1:00:00 PM"), away_team="CHI", home_team="IND", team="CHI", vs="CHI vs @IND", ps=-4.5, amount=20,user_id=4, bet_taken=False)
    bet4 = NFLcreateBet(bet_key=5, game_key=201610519, game_date=parse_date("10/9/2016 1:00:00 PM"), away_team="TEN", home_team="MIA", team="MIA", vs="TEN vs @MIA", ps=-3.5, amount=20, user_id=1, bet_taken=False)
    # take1 = NFLtakeBet(id=1, nfl_create_bet_id=1, user_id=2)
    # take2 = NFLtakeBet(id=2, nfl_create_bet_id=5, user_id=2)
    
    db.session.add(bet1)
    db.session.add(bet2)
    db.session.add(bet3)
    db.session.add(bet4)
    # db.session.add(take1)
    db.session.commit()


if __name__ == "__main__":
    db.drop_all()
    print "Just Dropped all tables"
    db.create_all()
    create_users()
    print "users created"
   
    create_bet()
    print "bets created"