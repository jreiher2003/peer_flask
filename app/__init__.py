import os 
from flask import Flask
from flask_mail import Mail
from flask_script import Manager 
from flask_caching import Cache 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager 
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView
from block_io import BlockIo

app = Flask(__name__) 
app.config.from_object(os.environ['APP_SETTINGS']) 
mail = Mail(app)  # Initialize Flask-Mail
db = SQLAlchemy(app) # Initialize Flask-SQLAlchemy
bcrypt = Bcrypt(app)
cache = Cache(app)
manager = Manager(app) 
version = 2
block_io = BlockIo("ef62-6d12-8127-566c", "finn7797", version)
login_manager = LoginManager(app) 

admin = Admin(app, name="Peer 2 Peer", template_mode="bootstrap3")
 

from app.users.views import users_blueprint
app.register_blueprint(users_blueprint) 
from app.home.views import home_blueprint
app.register_blueprint(home_blueprint) 
from app.nfl.views import nfl_blueprint
app.register_blueprint(nfl_blueprint) 
# from app.admin.views import admin_blueprint
# app.register_blueprint(admin_blueprint)

from temp_filters import dateify, datetimefilter, urlify, datetimefilter_f, game_time, game_date, game_day
app.jinja_env.filters["dateify"] = dateify
app.jinja_env.filters["datetimefilter"] = datetimefilter
app.jinja_env.filters["urlify"] = urlify
app.jinja_env.filters["datetimefilter_f"] = datetimefilter_f
app.jinja_env.filters["game_time"] = game_time
app.jinja_env.filters["game_date"] = game_date
app.jinja_env.filters["game_day"] = game_day

from app.users.models import Users, Role, UserRoles, Profile, BitcoinWallet
from app.nfl.models import Base, NFLOverUnderBet, NFLSideBet, NFLMLBet, NFLBetGraded
user_datastore = SQLAlchemyUserDatastore(db, Users, Role)
security = Security(app, user_datastore)

# ModelView(model, session, name=None, category=None, endpoint=None, url=None, static_folder=None, menu_class_name=None, menu_icon_type=None, menu_icon_value=None)
# from app.admin.models import UserAdmin
# admin.add_view(UserAdmin(Users, db.session))

admin.add_view(ModelView(Users, db.session, endpoint="users_"))
admin.add_view(ModelView(Profile, db.session))
admin.add_view(ModelView(BitcoinWallet, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(UserRoles, db.session))
admin.add_view(ModelView(Base, db.session))
admin.add_view(ModelView(NFLOverUnderBet, db.session, name="NFL OU"))
admin.add_view(ModelView(NFLSideBet, db.session, name="NFL SB"))
admin.add_view(ModelView(NFLMLBet, db.session, name="NFL ML"))
admin.add_view(ModelView(NFLBetGraded, db.session, name="nflGraded"))


login_manager.login_view = "users.login"
login_manager.login_message = "You need to login first before you can continue."
login_manager.login_message_category = "info"

@login_manager.user_loader 
def load_user(user_id):
    return Users.query.filter_by(id=int(user_id)).one_or_none()


