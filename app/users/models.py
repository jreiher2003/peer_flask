import datetime
from app import db
# from app.nfl.models import NflBet
from flask_security import UserMixin, RoleMixin 


class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    active = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime())
    date_created = db.Column(db.DateTime(),  default=datetime.datetime.now())
    date_modified = db.Column(db.DateTime,  default=datetime.datetime.now(),
                                       onupdate=datetime.datetime.now())
    last_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(45))
    current_login_at = db.Column(db.DateTime())
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)
    #profile = db.relationship("Profile")
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))
    
    def __repr__(self):
        return "<username-{}".format(self.username)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def has_role(self, role):
        return True

    def get_id(self):
        return unicode(self.id)

# Define the Role DataModel
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role %r>' % self.name

class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


class Profile(db.Model):
    __tablename__ = "profile"

    id = db.Column(db.Integer(), primary_key=True)
    avatar = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete='CASCADE'))
    users = db.relationship("Users")
