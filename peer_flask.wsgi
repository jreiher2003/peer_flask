#!/usr/bin/python
import os
import sys
import logging

activate_this = '/var/www/peer_flask/peer_flask/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/peer_flask/peer_flask")


os.environ['APP_SETTINGS'] = 'config.ProductionConfig'
os.environ['SECRET_KEY'] = 'AabB33ddfye474384fdsjtyGG0e3dafinbB12'
os.environ['DATABASE_URL'] = 'postgresql://finn_db:finn7797@localhost:5432/peer_pro'

os.environ['MAIL_SERVER']="smtp.gmail.com"
os.environ['MAIL_PORT']=465
os.environ['MAIL_USERNAME']="jeffreiher@gmail.com"
os.environ['MAIL_PASSWORD']="j3ff_7797"
os.environ['MAIL_USE_TLS']=False
os.environ['MAIL_USE_SSL']=True
os.environ['BLOCK_IO_API']="ef62-6d12-8127-566c"
os.environ['BLOCK_IO_PASSWD']="finn7797"
os.environ['FD_URL']="https://fantasydata.com/members/download-file.aspx?product=4885cd1b-6fd1-4db8-8c0a-47160973ca68"



from app import app as application

