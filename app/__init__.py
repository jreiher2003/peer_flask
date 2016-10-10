import os 
from flask import Flask
from flask_mail import Mail
from flask_script import Manager 
from flask_caching import Cache 
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore

app = Flask(__name__) 
app.config.from_object(os.environ['APP_SETTINGS']) 
mail = Mail(app)  # Initialize Flask-Mail
db = SQLAlchemy(app) # Initialize Flask-SQLAlchemy
cache = Cache(app)
manager = Manager(app) 

from app.users.views import users_blueprint
app.register_blueprint(users_blueprint) 
from app.home.views import home_blueprint
app.register_blueprint(home_blueprint) 
from app.nfl.views import nfl_blueprint
app.register_blueprint(nfl_blueprint) 

from temp_filters import dateify, datetimefilter, urlify, datetimefilter_f, game_time, game_date, game_day
app.jinja_env.filters["dateify"] = dateify
app.jinja_env.filters["datetimefilter"] = datetimefilter
app.jinja_env.filters["urlify"] = urlify
app.jinja_env.filters["datetimefilter_f"] = datetimefilter_f
app.jinja_env.filters["game_time"] = game_time
app.jinja_env.filters["game_date"] = game_date
app.jinja_env.filters["game_day"] = game_day

from app.users.models import Users, Role, UserRoles, Profile
# Setup Flask-Security
#https://pythonhosted.org/Flask-Security/api.html user_datastore api docs ie create_role, create_user
from app.users.forms import ExtendedConfirmRegisterForm

user_datastore = SQLAlchemyUserDatastore(db, Users, Role)
security = Security(app, user_datastore, register_form=ExtendedConfirmRegisterForm)


