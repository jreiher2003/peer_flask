import os 
from dateutil.parser import parse as parse_date 
from datetime import datetime
from flask import Flask
from flask_mail import Mail
from flask_script import Manager 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager 

app = Flask(__name__) 
app.config.from_object(os.environ['APP_SETTINGS']) 
mail = Mail(app)  # Initialize Flask-Mail
db = SQLAlchemy(app) # Initialize Flask-SQLAlchemy
manager = Manager(app) 
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

from app.users.views import users_blueprint
app.register_blueprint(users_blueprint) 
from app.home.views import home_blueprint
app.register_blueprint(home_blueprint) 
from app.nfl.views import nfl_blueprint
app.register_blueprint(nfl_blueprint) 

@app.template_filter()
def dateify(value):
    return parse_date(value)

@app.template_filter()
def datetimefilter(value):
    """convert a datetime to a different format."""
    tt = datetime.strptime(value, '%m/%d/%Y %H:%M:%f %p')
    return tt.strftime('%b %d - %H:%M EST')

app.jinja_env.filters["dateify"] = dateify
app.jinja_env.filters['datetimefilter'] = datetimefilter

from app.users.models import Users, Role, UserRoles, Profile
login_manager.login_view = "users.login"
login_manager.login_message = "You need to login first!"
login_manager.login_message_category = "info"

# loads users info from db and stores it in a session
@login_manager.user_loader 
def load_user(user_id):
    return Users.query.filter(Users.id == int(user_id)).first()

