import os 
from dateutil.parser import parse as parse_date 
from datetime import datetime
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
# from dateify import dateify 

app = Flask(__name__) 
app.config.from_object(os.environ['APP_SETTINGS']) 
db = SQLAlchemy(app) 

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

from app import views, models 
# from models import *