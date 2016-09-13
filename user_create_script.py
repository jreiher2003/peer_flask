from app.users.models import Users, Role, UserRoles,Profile
from app import app, db, bcrypt 


def create_users():
    user1 = Users(id=1,username="j3ff_", email="jeffreiher@gmail.com", password=bcrypt.generate_password_hash("password"))
    role1 = Role(id=1,name="admin")
    role2 = Role(id=2,name="seller")
    # Bind user to two roles
    u1 = UserRoles(user_id=user1.id, role_id=role1.id)
    u2 = UserRoles(user_id=user1.id, role_id=role2.id)
    profile1 = Profile(id=1,avatar="jeff.jpg",user_id=1)

    user2 = Users(id=2, username="ken", email="ken@gmail.com", password=bcrypt.generate_password_hash("password"))
    role3 = Role(id=3,name="player")
    u3 = UserRoles(user_id=user2.id, role_id=role3.id)
    profile2 = Profile(id=2,avatar="ken.jpg",user_id=2)

    user3 = Users(id=3, username="Mike", email="mike@gmail.com", password=bcrypt.generate_password_hash("password"))
    role4 = Role(id=4,name="player")
    u4 = UserRoles(user_id=user3.id, role_id=role4.id)
    profile3 = Profile(id=3,avatar="mike.jpg",user_id=3)

    user4 = Users(id=4, username="Greg", email="greg@gmail.com", password=bcrypt.generate_password_hash("password"))
    role5 = Role(id=5,name="staff")
    u5 = UserRoles(user_id=user4.id, role_id=role5.id)
    profile4 = Profile(id=4,avatar="greg.jpg",user_id=4)

    user5 = Users(id=5, username="Rob", email="rob@gmail.com", password=bcrypt.generate_password_hash("password"))
    role6 = Role(id=6,name="staff")
    u6 = UserRoles(user_id=user5.id, role_id=role6.id) 
    profile5 = Profile(id=5,avatar="rob.jpg",user_id=5)

    db.session.add(user1)
    db.session.add(role1)
    db.session.add(role2)
    db.session.add(u1)
    db.session.add(u2)
    db.session.add(profile1)
    db.session.add(user2)
    db.session.add(role3)
    db.session.add(u3)
    db.session.add(profile2)
    db.session.add(user3)
    db.session.add(role4)
    db.session.add(u4)
    db.session.add(profile3)
    db.session.add(user4)
    db.session.add(role5)
    db.session.add(u5)
    db.session.add(profile4)
    db.session.add(user5)
    db.session.add(role6)
    db.session.add(u6)
    db.session.add(profile5)
    db.session.commit()

if __name__ == "__main__":
    db.drop_all()
    print "Just Dropped all tables"
    db.create_all()
    create_users()
    print "users created"