import os 
from dateutil.parser import parse as parse_date 
from datetime import datetime
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy  

app = Flask(__name__) 
app.config.from_object(os.environ['APP_SETTINGS']) 
db = SQLAlchemy(app) 

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

from app import models 
# from models import *