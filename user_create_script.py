from app.users.models import Users, Role, UserRoles,Profile
from app.nfl.models import NflBet
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
        user2 = user_datastore.create_user(id=2, username="ken", email="ken@gmail.com", password=encrypt_password("password"))
        user3 = user_datastore.create_user(id=3, username="Mike", email="mike@gmail.com", password=encrypt_password("password"))
        user4 = user_datastore.create_user(id=4, username="Greg", email="greg@gmail.com", password=encrypt_password("password"))
        user5 = user_datastore.create_user(id=5, username="Rob", email="rob@gmail.com", password=encrypt_password("password"))
        db.session.commit()
        # user 1
        u1 = UserRoles(user_id=user1.id, role_id=role1.id)
        u2 = UserRoles(user_id=user1.id, role_id=role2.id)
        u3 = UserRoles(user_id=user1.id, role_id=role3.id)
        profile1 = Profile(id=1,avatar="jeff.jpg",user_id=1)
        #user 2
        u4 = UserRoles(user_id=user2.id, role_id=role2.id)
        u5 = UserRoles(user_id=user2.id, role_id=role3.id)
        profile2 = Profile(id=2,avatar="ken.jpg",user_id=2)
        # user 3
        u6 = UserRoles(user_id=user3.id, role_id=role2.id)
        u7 = UserRoles(user_id=user3.id, role_id=role3.id)
        profile3 = Profile(id=3,avatar="mike.jpg",user_id=3)
        # user 4
        u8 = UserRoles(user_id=user4.id, role_id=role2.id)
        u9 = UserRoles(user_id=user4.id, role_id=role3.id)
        profile4 = Profile(id=4,avatar="greg.jpg",user_id=4)
        # user 5
        u10 = UserRoles(user_id=user5.id, role_id=role2.id)
        u11 = UserRoles(user_id=user5.id, role_id=role3.id)
        profile5 = Profile(id=5,avatar="rob.jpg",user_id=5)

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
    bet1 = NflBet(game_key="201610321", home_team="NE", home_ps="1.0", amount="20", user_id=1)
    db.session.add(bet1)
    db.session.commit()


if __name__ == "__main__":
    db.drop_all()
    print "Just Dropped all tables"
    db.create_all()
    create_users()
    print "users created"
    create_bet()
    print "bets created"