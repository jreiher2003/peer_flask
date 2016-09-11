import os 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
import dateify 

app = Flask(__name__) 
app.config.from_object(os.environ['APP_SETTINGS']) 
db = SQLAlchemy(app) 

app.jinja_env.filters["dateify"] = dateify.dateify

from app import views, models 
# from models import *