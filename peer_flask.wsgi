#!/usr/bin/python
import os
import sys
import logging

activate_this = '/var/www/peer_flask/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/peer_flask/")


from app import app as application
application.config.from_object(os.environ['APP_SETTINGS']) 
application.secret_key = os.environ["SECRET_KEY"] 

